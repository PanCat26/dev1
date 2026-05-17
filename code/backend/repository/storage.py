import os
import asyncio
from pathlib import Path
from typing import List, Optional

_SKIP_WALK_DIRS = frozenset({".git", "__pycache__"})


class LocalRepositoryStorage:
    """
    Service for extracting files and regions directly from the on-disk repository snapshot.
    """
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self._base_dir_resolved = self.base_dir.resolve()

    def _list_files_sync(self, path_prefix: Optional[str] = None) -> List[str]:
        files = []
        prefix = (path_prefix or "").replace("\\", "/").strip()
        for root, dirnames, filenames in os.walk(self.base_dir):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_WALK_DIRS]
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), self.base_dir)
                rel_posix = rel_path.replace("\\", "/")
                if not prefix or rel_posix.startswith(prefix):
                    files.append(rel_posix)
        return sorted(files)

    async def list_files(self, path_prefix: Optional[str] = None) -> List[str]:
        """List files in the repository. Optionally filter by path_prefix."""
        return await asyncio.to_thread(self._list_files_sync, path_prefix)
        
    def _get_file_content_sync(self, file_path: str) -> Optional[str]:
        full_path = (self.base_dir / file_path.replace("\\", "/")).resolve()
        try:
            full_path.relative_to(self._base_dir_resolved)
        except ValueError:
            return None
        if not full_path.is_file():
            return None
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            return None

    async def get_file_content(self, file_path: str) -> Optional[str]:
        """Read the full content of a file from the repository snapshot."""
        return await asyncio.to_thread(self._get_file_content_sync, file_path)
