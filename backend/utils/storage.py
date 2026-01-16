"""
Storage Utility - File storage operations
For local development and future cloud storage integration
"""

import os
import uuid
from datetime import datetime
from typing import Optional
import aiofiles
import aiofiles.os

# Storage settings
STORAGE_PATH = os.getenv("STORAGE_PATH", "./uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class StorageService:
    """
    Handle file storage operations.
    Currently uses local filesystem, can be extended for cloud storage.
    """
    
    def __init__(self, base_path: str = STORAGE_PATH):
        self.base_path = base_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure storage directory exists."""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    async def save_file(self, content: bytes, filename: str, user_id: Optional[str] = None) -> str:
        """
        Save a file to storage.
        
        Args:
            content: File content as bytes
            filename: Original filename
            user_id: Optional user ID for organizing files
            
        Returns:
            Storage path/key for the file
        """
        # Generate unique filename
        ext = filename.split(".")[-1] if "." in filename else ""
        unique_name = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if ext:
            unique_name += f".{ext}"
        
        # Create user subdirectory if user_id provided
        if user_id:
            user_path = os.path.join(self.base_path, user_id)
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            file_path = os.path.join(user_path, unique_name)
        else:
            file_path = os.path.join(self.base_path, unique_name)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return file_path
    
    async def get_file(self, file_path: str) -> Optional[bytes]:
        """
        Retrieve a file from storage.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content as bytes, or None if not found
        """
        if not os.path.exists(file_path):
            return None
        
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if deleted, False if not found
        """
        if not os.path.exists(file_path):
            return False
        
        await aiofiles.os.remove(file_path)
        return True
    
    async def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Get file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file info, or None if not found
        """
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
        }
    
    def get_storage_usage(self, user_id: Optional[str] = None) -> int:
        """
        Get total storage usage in bytes.
        
        Args:
            user_id: Optional user ID to check specific user's usage
            
        Returns:
            Total size in bytes
        """
        if user_id:
            path = os.path.join(self.base_path, user_id)
        else:
            path = self.base_path
        
        if not os.path.exists(path):
            return 0
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        
        return total_size


# Create default storage instance
storage = StorageService()
