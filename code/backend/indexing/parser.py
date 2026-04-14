import ast
import textwrap

from indexing.types import ParsedSymbol


def _read_file_lines(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.readlines()


def _extract_source(lines: list[str], start: int, end: int) -> str:
    """Extract source text for lines[start-1 .. end-1] (1-indexed)."""
    return textwrap.dedent("".join(lines[start - 1 : end]))


def parse_python_file(path: str) -> list[ParsedSymbol]:
    """Parse a Python file and return top-level functions, classes, and methods.

    If the file cannot be parsed (syntax error, encoding issue, etc.),
    returns an empty list instead of crashing.
    """
    try:
        lines = _read_file_lines(path)
        source = "".join(lines)
        tree = ast.parse(source, filename=path)
    except (SyntaxError, ValueError, UnicodeDecodeError) as e:
        print(f"Warning: could not parse {path}: {e}")
        return []

    symbols: list[ParsedSymbol] = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            symbols.append(ParsedSymbol(
                file_path=path,
                symbol_name=node.name,
                symbol_type="function",
                start_line=node.lineno,
                end_line=node.end_lineno or node.lineno,
                source=_extract_source(lines, node.lineno, node.end_lineno or node.lineno),
            ))

        elif isinstance(node, ast.ClassDef):
            class_end = node.end_lineno or node.lineno
            symbols.append(ParsedSymbol(
                file_path=path,
                symbol_name=node.name,
                symbol_type="class",
                start_line=node.lineno,
                end_line=class_end,
                source=_extract_source(lines, node.lineno, class_end),
            ))

            # Extract methods inside the class
            for item in ast.iter_child_nodes(node):
                if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
                    symbols.append(ParsedSymbol(
                        file_path=path,
                        symbol_name=f"{node.name}.{item.name}",
                        symbol_type="method",
                        start_line=item.lineno,
                        end_line=item.end_lineno or item.lineno,
                        source=_extract_source(lines, item.lineno, item.end_lineno or item.lineno),
                    ))

    return symbols
