"""
Demo script: scan a directory and parse all Python files found.
Usage:  python scripts/run_scanning_demo.py <path-to-repo-snapshot>

If no path is given, it scans the code/backend/ directory itself as an example.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from indexing.scanner import list_supported_files
from indexing.parser import parse_python_file


def main():
    snapshot_path = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    print(f"Scanning: {os.path.abspath(snapshot_path)}\n")

    files = list_supported_files(snapshot_path)
    print(f"Found {len(files)} supported file(s):\n")
    for f in files:
        print(f"  {f}")

    print("\nPython symbols\n")
    for f in files:
        if not f.endswith(".py"):
            continue
        symbols = parse_python_file(f)
        if not symbols:
            continue
        for s in symbols:
            print(f"  [{s.symbol_type}] {s.symbol_name}  ({os.path.basename(s.file_path)}:{s.start_line}-{s.end_line})")


if __name__ == "__main__":
    main()
