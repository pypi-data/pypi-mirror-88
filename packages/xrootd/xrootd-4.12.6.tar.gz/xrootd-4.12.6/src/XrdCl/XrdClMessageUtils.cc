//------------------------------------------------------------------------------
// Copyright (c) 2011-2014 by European Organization for Nuclear Research (CERN)
// Author: Lukasz Janyst <ljanyst@cern.ch>
//------------------------------------------------------------------------------
// This file is part of the XRootD software suite.
//
// XRootD is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// XRootD is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with XRootD.  If not, see <http://www.gnu.org/licenses/>.
//
// In applying this licence, CERN does not waive the privileges and immunities
// granted to it by virtue of its status as an Intergovernmental Organization
// or submit itself to any jurisdiction.
//------------------------------------------------------------------------------

#include "XrdCl/XrdClMessageUtils.hh"
#include "XrdCl/XrdClLog.hh"
#include "XrdCl/XrdClDefaultEnv.hh"
#include "XrdCl/XrdClConstants.hh"
#include "XrdCl/XrdClAnyObject.hh"
#include "XrdCl/XrdClSIDManager.hh"
#include "XrdCl/XrdClPostMaster.hh"
#include "XrdCl/XrdClXRootDTransport.hh"
#include "XrdCl/XrdClXRootDMsgHandler.hh"
#include "XrdClRedirectorRegistry.hh"

namespace XrdCl
{
  //----------------------------------------------------------------------------
  // Send a message
  //----------------------------------------------------------------------------
  Status MessageUtils::SendMessage( const URL               &url,
                                    Message                 *msg,
                                    ResponseHandler         *handler,
                                    const MessageSendParams &sendParams,
                                    LocalFileHandler        *lFileHandler )
  {
    //--------------------------------------------------------------------------
    // Get the stuff needed to send the message
    //--------------------------------------------------------------------------
    Log        *log        = DefaultEnv::GetLog();
    PostMaster *postMaster = DefaultEnv::GetPostMaster();
    Status      st;

    if( !postMaster )
      return Status( stError, errUninitialized );

    log->Dump( XRootDMsg, "[%s] Sending message %s",
               url.GetHostId().c_str(), msg->GetDescription().c_str() );

    //--------------------------------------------------------------------------
    // Get an instance of SID manager object
    //--------------------------------------------------------------------------
    std::shared_ptr<SIDManager> sidMgr( SIDMgrPool::Instance().GetSIDMgr( url ) );
    ClientRequestHdr *req = (ClientRequestHdr*)msg->GetBuffer();

    //--------------------------------------------------------------------------
    // Allocate the SID and marshall the message
    //--------------------------------------------------------------------------
    st = sidMgr->AllocateSID( req->streamid );
    if( !st.IsOK() )
    {
      log->Error( XRootDMsg, "[%s] Unable to allocate stream id",
                             url.GetHostId().c_str() );
      return st;
    }

    XRootDTransport::MarshallRequest( msg );

    //--------------------------------------------------------------------------
    // Create and set up the message handler
    //--------------------------------------------------------------------------
    XRootDMsgHandler *msgHandler;
    msgHandler = new XRootDMsgHandler( msg, handler, &url, sidMgr, lFileHandler );
    msgHandler->SetExpiration( sendParams.expires );
    msgHandler->SetRedirectAsAnswer( !sendParams.followRedirects );
    msgHandler->SetOksofarAsAnswer( sendParams.chunkedResponse );
    msgHandler->SetChunkList( sendParams.chunkList );
    msgHandler->SetRedirectCounter( sendParams.redirectLimit );
    msgHandler->SetStateful( sendParams.stateful );

    if( sendParams.loadBalancer.url.IsValid() )
      msgHandler->SetLoadBalancer( sendParams.loadBalancer );

    HostList *list = 0;
    list = new HostList();
    list->push_back( url );
    msgHandler->SetHostList( list );

    //--------------------------------------------------------------------------
    // Send the message
    //--------------------------------------------------------------------------
    st = postMaster->Send( url, msg, msgHandler, sendParams.stateful,
                           sendParams.expires );
    if( !st.IsOK() )
    {
      XRootDTransport::UnMarshallRequest( msg );
      log->Error( XRootDMsg, "[%s] Unable to send the message %s: %s",
                  url.GetHostId().c_str(), msg->GetDescription().c_str(),
                  st.ToString().c_str() );

      // we need to reassign req as its current value might have been
      // invalidated in the meanwhile due to a realloc
      req = (ClientRequestHdr*)msg->GetBuffer();
      // Release the SID as the request was never send
      sidMgr->ReleaseSID( req->streamid );
      delete msgHandler;
      delete list;
      return st;
    }
    return Status();
  }

  //----------------------------------------------------------------------------
  // Redirect a message
  //----------------------------------------------------------------------------
  Status MessageUtils::RedirectMessage( const URL         &url,
                                        Message           *msg,
                                        ResponseHandler   *handler,
                                        MessageSendParams &sendParams,
                                        LocalFileHandler  *lFileHandler )
  {
    //--------------------------------------------------------------------------
    // Register a new virtual redirector
    //--------------------------------------------------------------------------
    RedirectorRegistry& registry = RedirectorRegistry::Instance();
    Status st = registry.Register( url );
    if( !st.IsOK() )
      return st;

    //--------------------------------------------------------------------------
    // Get the stuff needed to send the message
    //--------------------------------------------------------------------------
    Log        *log        = DefaultEnv::GetLog();
    PostMaster *postMaster = DefaultEnv::GetPostMaster();

    if( !postMaster )
      return Status( stError, errUninitialized );

    log->Dump( XRootDMsg, "[%s] Redirecting message %s",
               url.GetHostId().c_str(), msg->GetDescription().c_str() );

    XRootDTransport::MarshallRequest( msg );

    //--------------------------------------------------------------------------
    // Create and set up the message handler
    //--------------------------------------------------------------------------
    XRootDMsgHandler *msgHandler;
    msgHandler = new XRootDMsgHandler( msg, handler, &url, std::shared_ptr<SIDManager>(), lFileHandler );
    msgHandler->SetExpiration( sendParams.expires );
    msgHandler->SetRedirectAsAnswer( !sendParams.followRedirects );
    msgHandler->SetOksofarAsAnswer( sendParams.chunkedResponse );
    msgHandler->SetChunkList( sendParams.chunkList );
    msgHandler->SetRedirectCounter( sendParams.redirectLimit );
    msgHandler->SetFollowMetalink( true );

    HostInfo info( url, true );
    info.flags = kXR_isManager | kXR_attrMeta | kXR_attrVirtRdr;
    sendParams.loadBalancer = info;
    msgHandler->SetLoadBalancer( info );

    HostList *list = 0;
    list = new HostList();
    list->push_back( info );
    msgHandler->SetHostList( list );

    //--------------------------------------------------------------------------
    // Redirect the message
    //--------------------------------------------------------------------------
    st = postMaster->Redirect( url, msg, msgHandler );
    if( !st.IsOK() )
    {
      XRootDTransport::UnMarshallRequest( msg );
      log->Error( XRootDMsg, "[%s] Unable to send the message %s: %s",
                  url.GetHostId().c_str(), msg->GetDescription().c_str(),
                  st.ToString().c_str() );
      delete msgHandler;
      delete list;
      return st;
    }
    return Status();
  }

  //----------------------------------------------------------------------------
  // Process sending params
  //----------------------------------------------------------------------------
  void MessageUtils::ProcessSendParams( MessageSendParams &sendParams )
  {
    //--------------------------------------------------------------------------
    // Timeout
    //--------------------------------------------------------------------------
    Env *env = DefaultEnv::GetEnv();
    if( sendParams.timeout == 0 )
    {
      int requestTimeout = DefaultRequestTimeout;
      env->GetInt( "RequestTimeout", requestTimeout );
      sendParams.timeout = requestTimeout;
    }

    if( sendParams.expires == 0 )
      sendParams.expires = ::time(0)+sendParams.timeout;

    //--------------------------------------------------------------------------
    // Redirect limit
    //--------------------------------------------------------------------------
    if( sendParams.redirectLimit == 0 )
    {
      int redirectLimit = DefaultRedirectLimit;
      env->GetInt( "RedirectLimit", redirectLimit );
      sendParams.redirectLimit = redirectLimit;
    }
  }

  //----------------------------------------------------------------------------
  //! Append cgi to the one already present in the message
  //----------------------------------------------------------------------------
  void MessageUtils::RewriteCGIAndPath( Message              *msg,
                                        const URL::ParamsMap &newCgi,
                                        bool                  replace,
                                        const std::string    &newPath )
  {
    ClientRequest  *req = (ClientRequest *)msg->GetBuffer();
    switch( req->header.requestid )
    {
      case kXR_chmod:
      case kXR_mkdir:
      case kXR_mv:
      case kXR_open:
      case kXR_rm:
      case kXR_rmdir:
      case kXR_stat:
      case kXR_truncate:
      {
        //----------------------------------------------------------------------
        // Get the pointer to the appropriate path
        //----------------------------------------------------------------------
        char *path = msg->GetBuffer( 24 );
        size_t length = req->header.dlen;
        if( req->header.requestid == kXR_mv )
        {
          for( int i = 0; i < req->header.dlen; ++i, ++path, --length )
            if( *path == ' ' )
              break;
          ++path;
          --length;
        }

        //----------------------------------------------------------------------
        // Create a fake URL from an existing CGI
        //----------------------------------------------------------------------
        char *pathWithNull = new char[length+1];
        memcpy( pathWithNull, path, length );
        pathWithNull[length] = 0;
        std::ostringstream o;
        o << "fake://fake:111/" << pathWithNull;
        delete [] pathWithNull;

        URL currentPath( o.str() );
        URL::ParamsMap currentCgi = currentPath.GetParams();
        MergeCGI( currentCgi, newCgi, replace );
        currentPath.SetParams( currentCgi );
        if( !newPath.empty() )
          currentPath.SetPath( newPath );
        std::string newPathWitParams = currentPath.GetPathWithParams();

        //----------------------------------------------------------------------
        // Write the path with the new cgi appended to the message
        //----------------------------------------------------------------------
        uint32_t newDlen = req->header.dlen - length + newPathWitParams.size();
        msg->ReAllocate( 24+newDlen );
        req  = (ClientRequest *)msg->GetBuffer();
        path = msg->GetBuffer( 24 );
        if( req->header.requestid == kXR_mv )
        {
          for( int i = 0; i < req->header.dlen; ++i, ++path )
            if( *path == ' ' )
              break;
          ++path;
        }
        memcpy( path, newPathWitParams.c_str(), newPathWitParams.size() );
        req->header.dlen = newDlen;
        break;
      }
      case kXR_locate:
      {
        Env *env = DefaultEnv::GetEnv();
        int preserveLocateTried = DefaultPreserveLocateTried;
        env->GetInt( "PreserveLocateTried", preserveLocateTried );

        if( !preserveLocateTried ) break;

        //----------------------------------------------------------------------
        // In case of locate we only want to preserve tried/triedrc CGI info
        //----------------------------------------------------------------------
        URL::ParamsMap triedCgi;
        URL::ParamsMap::const_iterator itr = newCgi.find( "triedrc" );
        if( itr != newCgi.end() )
          triedCgi[itr->first] = itr->second;
        itr = newCgi.find( "tried" );
        if( itr != newCgi.end() )
          triedCgi[itr->first] = itr->second;

        //----------------------------------------------------------------------
        // Is there anything to do?
        //----------------------------------------------------------------------
        if( triedCgi.empty() ) break;

        //----------------------------------------------------------------------
        // Get the pointer to the appropriate path
        //----------------------------------------------------------------------
        char *path = msg->GetBuffer( 24 );
        size_t length = req->header.dlen;

        //----------------------------------------------------------------------
        // Create a fake URL from an existing CGI
        //----------------------------------------------------------------------
        std::string strpath( path, length );
        std::ostringstream o;
        o << "fake://fake:111/" << strpath;

        URL currentPath( o.str() );
        URL::ParamsMap currentCgi = currentPath.GetParams();
        MergeCGI( currentCgi, triedCgi, replace );
        currentPath.SetParams( currentCgi );
        std::string pathWitParams = currentPath.GetPathWithParams();

        //----------------------------------------------------------------------
        // Write the path with the new cgi appended to the message
        //----------------------------------------------------------------------
        uint32_t newDlen = pathWitParams.size();
        msg->ReAllocate( 24+newDlen );
        req  = (ClientRequest *)msg->GetBuffer();
        path = msg->GetBuffer( 24 );
        memcpy( path, pathWitParams.c_str(), pathWitParams.size() );
        req->header.dlen = newDlen;
        break;
      }
    }
    XRootDTransport::SetDescription( msg );
  }

  //------------------------------------------------------------------------
  //! Merge cgi2 into cgi1
  //------------------------------------------------------------------------
  void MessageUtils::MergeCGI( URL::ParamsMap       &cgi1,
                               const URL::ParamsMap &cgi2,
                               bool                  replace )
  {
    URL::ParamsMap::const_iterator it;
    for( it = cgi2.begin(); it != cgi2.end(); ++it )
    {
      if( replace || cgi1.find( it->first ) == cgi1.end() )
        cgi1[it->first] = it->second;
      else
      {
        std::string &v = cgi1[it->first];
        if( v.empty() )
          v = it->second;
        else
        {
          v += ',';
          v += it->second;
        }
      }
    }
  }
}
