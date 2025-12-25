"""
File Controller for File-Architect-Pro.
Handles all file system operations.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class FileOperationError(Exception):
    """Custom exception for file operations."""
    pass


class FileType(Enum):
    """File type enumeration."""
    FILE = "file"
    DIRECTORY = "directory"
    UNKNOWN = "unknown"


@dataclass
class FileInfo:
    """Data class for file information."""
    path: Path
    name: str
    file_type: FileType
    size: int
    extension: str
    created: float
    modified: float
    is_hidden: bool
    
    @classmethod
    def from_path(cls, path: Path) -> 'FileInfo':
        """Create FileInfo from a Path object."""
        try:
            stat = path.stat()
            return cls(
                path=path,
                name=path.name,
                file_type=FileType.DIRECTORY if path.is_dir() else FileType.FILE,
                size=stat.st_size if path.is_file() else 0,
                extension=path.suffix.lower() if path.is_file() else "",
                created=stat.st_ctime,
                modified=stat.st_mtime,
                is_hidden=path.name.startswith('.') or cls._is_windows_hidden(path)
            )
        except (PermissionError, OSError) as e:
            raise FileOperationError(f"Cannot access file info: {e}")
    
    @staticmethod
    def _is_windows_hidden(path: Path) -> bool:
        """Check if file has hidden attribute on Windows."""
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            return attrs != -1 and bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN = 2
        except Exception:
            return False


class FileController:
    """
    Controller for file system operations.
    Provides methods for navigating, filtering, and manipulating files.
    """
    
    def __init__(self) -> None:
        self._current_directory: Optional[Path] = None
        self._selected_files: List[Path] = []
    
    # === Navigation ===
    
    def set_current_directory(self, path: str) -> bool:
        """Set the current working directory."""
        try:
            dir_path = Path(path)
            if dir_path.exists() and dir_path.is_dir():
                self._current_directory = dir_path
                return True
            return False
        except (PermissionError, OSError) as e:
            raise FileOperationError(f"Cannot access directory: {e}")
    
    def get_current_directory(self) -> Optional[Path]:
        """Get the current working directory."""
        return self._current_directory
    
    def list_directory(self, path: Optional[str] = None) -> List[FileInfo]:
        """List contents of directory."""
        target = Path(path) if path else self._current_directory
        
        if not target or not target.exists():
            return []
        
        try:
            items = []
            for item in target.iterdir():
                try:
                    items.append(FileInfo.from_path(item))
                except FileOperationError:
                    continue  # Skip inaccessible items
            return sorted(items, key=lambda x: (x.file_type != FileType.DIRECTORY, x.name.lower()))
        except PermissionError as e:
            raise FileOperationError(f"Permission denied: {e}")
    
    # === Selection ===
    
    def select_file(self, path: str) -> None:
        """Add file to selection."""
        file_path = Path(path)
        if file_path.exists() and file_path not in self._selected_files:
            self._selected_files.append(file_path)
    
    def deselect_file(self, path: str) -> None:
        """Remove file from selection."""
        file_path = Path(path)
        if file_path in self._selected_files:
            self._selected_files.remove(file_path)
    
    def clear_selection(self) -> None:
        """Clear all selected files."""
        self._selected_files.clear()
    
    def get_selected_files(self) -> List[Path]:
        """Get list of selected files."""
        return self._selected_files.copy()
    
    # === File Operations ===
    
    def delete_item(self, path: str, secure: bool = False) -> bool:
        """
        Delete a file or directory using EAFP pattern (no TOCTOU vulnerability).
        
        Args:
            path: Path to item to delete
            secure: If True, overwrite file before deletion (for files only)
        
        Returns:
            True if deletion was successful
        """
        item_path = Path(path)
        
        try:
            # EAFP: Direkt işlemi dene, hata olursa yakala (TOCTOU riski yok)
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                if secure:
                    self._secure_delete_file(item_path)
                else:
                    item_path.unlink()
            return True
            
        except FileNotFoundError:
            raise FileOperationError(f"Item does not exist: {path}")
        except PermissionError:
            raise FileOperationError(f"Permission denied: {path}")
        except OSError as e:
            raise FileOperationError(f"Delete failed: {e}")
    
    def _secure_delete_file(self, path: Path) -> None:
        """Securely delete file by overwriting with random data."""
        try:
            size = path.stat().st_size
            with open(path, 'wb') as f:
                # Overwrite 3 times with random data
                for _ in range(3):
                    f.seek(0)
                    f.write(os.urandom(size))
                    f.flush()
                    os.fsync(f.fileno())
            path.unlink()
        except Exception as e:
            raise FileOperationError(f"Secure delete failed: {e}")
    
    def copy_item(self, source: str, destination: str) -> bool:
        """Copy file or directory."""
        try:
            src_path = Path(source)
            dst_path = Path(destination)
            
            if not src_path.exists():
                raise FileOperationError(f"Source does not exist: {source}")
            
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
            else:
                shutil.copytree(src_path, dst_path)
            
            return True
            
        except PermissionError:
            raise FileOperationError(f"Permission denied")
        except OSError as e:
            raise FileOperationError(f"Copy failed: {e}")
    
    def rename_item(self, old_path: str, new_name: str) -> bool:
        """Rename a file or directory."""
        try:
            old = Path(old_path)
            new = old.parent / new_name
            
            if not old.exists():
                raise FileOperationError(f"Item does not exist: {old_path}")
            
            if new.exists():
                raise FileOperationError(f"Target already exists: {new}")
            
            old.rename(new)
            return True
            
        except PermissionError:
            raise FileOperationError("Permission denied")
        except OSError as e:
            raise FileOperationError(f"Rename failed: {e}")
    
    def get_file_info(self, path: str) -> Optional[FileInfo]:
        """Get detailed file information."""
        try:
            return FileInfo.from_path(Path(path))
        except FileOperationError:
            return None
    
    # === Filtering Helpers ===
    
    def filter_by_extension(self, files: List[FileInfo], extensions: List[str]) -> List[FileInfo]:
        """Filter files by extension."""
        ext_set = {ext.lower().lstrip('.') for ext in extensions}
        return [f for f in files if f.extension.lstrip('.') in ext_set]
    
    def filter_by_size(self, files: List[FileInfo], min_size: int = 0, max_size: int = float('inf')) -> List[FileInfo]:
        """Filter files by size range."""
        return [f for f in files if min_size <= f.size <= max_size]
    
    def filter_empty_files(self, files: List[FileInfo]) -> List[FileInfo]:
        """Filter to only empty files."""
        return [f for f in files if f.size == 0 and f.file_type == FileType.FILE]
    
    def filter_hidden(self, files: List[FileInfo]) -> List[FileInfo]:
        """Filter to only hidden files."""
        return [f for f in files if f.is_hidden]
