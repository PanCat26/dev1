import ast
import json
from typing import Any

from repository.storage import LocalRepositoryStorage

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Inspect the repository tree to find file paths matching an optional path prefix.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path_prefix": {
                        "type": "string",
                        "description": "Optional directory prefix using forward slashes (e.g. 'test/', 'src/'). Works on Windows and Unix.",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_file",
            "description": "Read exact regions from the repository given a file path and optional line limits. Useful to inspect definitions and code surrounding symbols. Each returned line is prefixed with its 1-based line number and a pipe (LINE|content).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative file path.",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "The first line to read (1-indexed).",
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "The last line to read (inclusive).",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search code text for exact names, strings, or identifiers. Prefer path_prefix when the user asked about a specific folder (e.g. tests under test/).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The exact string or identifier to search for.",
                    },
                    "path_prefix": {
                        "type": "string",
                        "description": "If set, only search files under this path (forward slashes, e.g. 'test/'). Omit to search the whole repo.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "symbol_lookup",
            "description": "Locate a class, module-level function, or class method by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Class name, top-level function name, bare method name, or ClassName.method.",
                    }
                },
                "required": ["name"],
            },
        },
    },
]


def _normalize_path_prefix(path_prefix: str | None) -> str | None:
    p = (path_prefix or "").replace("\\", "/").strip()
    return p or None


async def list_files(
    storage: LocalRepositoryStorage, path_prefix: str | None = None
) -> list[str]:
    files = await storage.list_files(_normalize_path_prefix(path_prefix))
    return files[:50]


async def open_file(
    storage: LocalRepositoryStorage,
    file_path: str,
    start_line: int | None = None,
    end_line: int | None = None,
) -> str:
    content = await storage.get_file_content(file_path)
    if content is None:
        return f"Error: File '{file_path}' not found or unreadable."

    lines = content.splitlines()
    if start_line is None:
        start_line = 1
    if end_line is None:
        end_line = len(lines)

    start_idx = max(0, start_line - 1)
    end_idx = min(len(lines), end_line)
    if start_idx >= len(lines) or start_idx >= end_idx:
        return f"Error: Invalid line range {start_line}-{end_line} (file has {len(lines)} lines)."

    numbered: list[str] = []
    for i in range(start_idx, end_idx):
        line_no = i + 1
        numbered.append(f"{line_no:5d}|{lines[i]}")
    return "\n".join(numbered)


async def search_code(
    storage: LocalRepositoryStorage,
    query: str,
    path_prefix: str | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    files = await storage.list_files(_normalize_path_prefix(path_prefix))

    for file_path in files:
        content = await storage.get_file_content(file_path)
        if not content:
            continue

        for idx, line in enumerate(content.splitlines()):
            if query in line:
                results.append(
                    {
                        "file_path": file_path,
                        "line_number": idx + 1,
                        "context": line.strip(),
                    }
                )
                if len(results) >= 20:
                    return results
    return results


async def symbol_lookup(storage: LocalRepositoryStorage, name: str) -> list[dict[str, Any]]:
    """Top-level defs and class methods (same idea as the indexer)."""
    results: list[dict[str, Any]] = []
    for file_path in [f for f in await storage.list_files() if f.endswith(".py")]:
        content = await storage.get_file_content(file_path)
        if not content:
            continue
        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError:
            continue
        if not isinstance(tree, ast.Module):
            continue

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                if node.name == name:
                    results.append(
                        {
                            "file_path": file_path,
                            "type": "class",
                            "start_line": node.lineno,
                            "end_line": getattr(node, "end_lineno", node.lineno + 1),
                        }
                    )
                    if len(results) >= 10:
                        return results
                for item in ast.iter_child_nodes(node):
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                        item.name == name or f"{node.name}.{item.name}" == name
                    ):
                        results.append(
                            {
                                "file_path": file_path,
                                "type": "method",
                                "start_line": item.lineno,
                                "end_line": getattr(item, "end_lineno", item.lineno + 1),
                                "class_name": node.name,
                            }
                        )
                        if len(results) >= 10:
                            return results
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                results.append(
                    {
                        "file_path": file_path,
                        "type": "function",
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno + 1),
                    }
                )
                if len(results) >= 10:
                    return results

    return results


_TOOL_HANDLERS = {
    "list_files": list_files,
    "open_file": open_file,
    "search_code": search_code,
    "symbol_lookup": symbol_lookup,
}


async def execute_tool_call(storage: LocalRepositoryStorage, call: dict[str, Any]) -> str:
    func_name = call.get("function", {}).get("name")
    raw = call.get("function", {}).get("arguments")
    if isinstance(raw, str):
        args_str = raw.strip() or "{}"
    elif raw is None:
        args_str = "{}"
    else:
        args_str = json.dumps(raw)

    try:
        kwargs = json.loads(args_str)
    except json.JSONDecodeError:
        return f"Error: Failed to parse tool arguments: {args_str}"

    handler = _TOOL_HANDLERS.get(func_name)
    if not handler:
        return f"Error: Tool '{func_name}' is not recognized."

    try:
        result = await handler(storage, **kwargs)
        return json.dumps(result, indent=2) if isinstance(result, (list, dict)) else str(result)
    except TypeError as e:
        return f"Error: invalid arguments for {func_name}: {e}"
    except Exception as e:
        return f"Error executing tool {func_name}: {str(e)}"
