from dataclasses import dataclass


@dataclass
class ParsedSymbol:
    """A single symbol extracted from a source file."""
    file_path: str
    symbol_name: str
    symbol_type: str  # "function", "class", "method"
    start_line: int
    end_line: int
    text: str


@dataclass
class Chunk:
    """A text chunk ready for embedding and storage."""
    repo_id: str
    commit_sha: str
    file_path: str
    chunk_type: str  # "function", "class", "method", "doc_section"
    symbol_name: str
    start_line: int
    end_line: int
    text: str
