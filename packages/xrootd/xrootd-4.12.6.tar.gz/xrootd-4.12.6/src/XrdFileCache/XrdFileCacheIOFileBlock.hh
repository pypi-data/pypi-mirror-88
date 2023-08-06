#ifndef __XRDFILECACHE_IO_FILE_BLOCK_HH__
#define __XRDFILECACHE_IO_FILE_BLOCK_HH__
//----------------------------------------------------------------------------------
// Copyright (c) 2014 by Board of Trustees of the Leland Stanford, Jr., University
// Author: Alja Mrak-Tadel, Matevz Tadel, Brian Bockelman
//----------------------------------------------------------------------------------
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
//----------------------------------------------------------------------------------
#include <map>
#include <string>

#include "XrdOuc/XrdOucCache2.hh"
#include "XrdSys/XrdSysPthread.hh"

#include "XrdFileCacheIO.hh"

class XrdSysError;
class XrdOssDF;

namespace XrdFileCache
{
//----------------------------------------------------------------------------
//! \brief Downloads original file into multiple files, chunked into
//! blocks. Only blocks that are asked for are downloaded.
//! Handles read requests as they come along.
//----------------------------------------------------------------------------
class IOFileBlock : public IO
{
public:
   //------------------------------------------------------------------------
   //! Constructor.
   //------------------------------------------------------------------------
   IOFileBlock(XrdOucCacheIO2 *io, XrdOucCacheStats &stats, Cache &cache);

   //------------------------------------------------------------------------
   //! Destructor.
   //------------------------------------------------------------------------
   ~IOFileBlock();

   //---------------------------------------------------------------------
   //! Detach from Cache. Note: this will delete the object.
   //!
   //! @return original source \ref XrdPosixFile
   //---------------------------------------------------------------------
   virtual XrdOucCacheIO *Detach();

   //---------------------------------------------------------------------
   //! Pass Read request to the corresponding File object.
   //---------------------------------------------------------------------
   using XrdOucCacheIO2::Read;

   virtual int Read(char *Buffer, long long Offset, int Length);

   //! \brief Virtual method of XrdOucCacheIO.
   //! Called to check if destruction needs to be done in a separate task.
   virtual bool ioActive();
   
   virtual int  Fstat(struct stat &sbuff);

   virtual long long FSize();

private:
   long long                  m_blocksize;       //!< size of file-block
   std::map<int, File*>       m_blocks;          //!< map of created blocks
   XrdSysMutex                m_mutex;           //!< map mutex
   struct stat               *m_localStat;
   Info                       m_info;
   XrdOssDF*                  m_infoFile;

   void  GetBlockSizeFromPath();
   int   initLocalStat();
   File* newBlockFile(long long off, int blocksize);
   void  CloseInfoFile();
};
}

#endif
