import os
from pathlib import Path

SUPPORTED_EXTENSIONS = {".py", ".md"}

IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".eggs",
    "*.egg-info",
}


def _is_ignored_dir(name: str) -> bool:
    return name in IGNORED_DIRS or name.endswith(".egg-info")


def list_supported_files(snapshot_path: str) -> list[str]:
    """Recursively list all supported files under snapshot_path.

    Returns absolute paths for files matching SUPPORTED_EXTENSIONS,
    skipping directories in IGNORED_DIRS.
    """
    result: list[str] = []
    root = Path(snapshot_path)

    if not root.is_dir():
        print(f"Warning: snapshot path '{snapshot_path}' is not a directory.")
        return result

    for dirpath, dirnames, filenames in os.walk(root):
        # Remove ignored directories in place so os.walk won’t traverse them
        dirnames[:] = [d for d in dirnames if not _is_ignored_dir(d)]

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                result.append(os.path.join(dirpath, filename))

    return sorted(result)
