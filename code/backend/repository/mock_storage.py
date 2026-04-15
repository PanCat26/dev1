import os
from pathlib import Path
from typing import List, Optional

class MockRepositoryStorage:
    """
    Mocked service for extracting files and regions directly from the on-disk repository snapshot.
    """
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        
    def list_files(self, path_prefix: Optional[str] = None) -> List[str]:
        """List files in the repository. Optionally filter by path_prefix."""
        files = []
        for root, _, filenames in os.walk(self.base_dir):
            for filename in filenames:
                # Exclude hidden files / common unnecessary dirs
                if '.git' in root or '__pycache__' in root:
                    continue
                
                rel_path = os.path.relpath(os.path.join(root, filename), self.base_dir)
                if not path_prefix or rel_path.startswith(path_prefix):
                    files.append(rel_path)
        return sorted(files)
        
    def get_file_content(self, file_path: str) -> Optional[str]:
        """Read the full content of a file from the repository snapshot."""
        full_path = self.base_dir / file_path
        if not full_path.is_file():
            return None
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            return None # Ignore binary files
