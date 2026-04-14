from dataclasses import dataclass


@dataclass
class ParsedSymbol:
    """A single symbol extracted from a source file."""
    file_path: str
    symbol_name: str
    symbol_type: str  # "function", "class", "method"
    start_line: int
    end_line: int
    source: str
