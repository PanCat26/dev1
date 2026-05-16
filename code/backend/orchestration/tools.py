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
                        "description": "The optional directory prefix (e.g., 'src/backend').",
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
            "description": "Read exact regions from the repository given a file path and optional line limits. Useful to inspect definitions and code surrounding symbols.",
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
            "description": "Search code text for exact names, strings, or identifiers across the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The exact string or identifier to search for.",
                    }
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


async def list_files(
    storage: LocalRepositoryStorage, path_prefix: str | None = None
) -> list[str]:
    files = await storage.list_files(path_prefix)
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
    return "\n".join(lines[start_idx:end_idx])


async def search_code(storage: LocalRepositoryStorage, query: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    files = await storage.list_files()

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


def _symbol_lookup_append(
    results: list[dict[str, Any]],
    file_path: str,
    sym_type: str,
    node: ast.AST,
    **extra: Any,
) -> bool:
    results.append(
        {
            "file_path": file_path,
            "type": sym_type,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno + 1),
            **extra,
        }
    )
    return len(results) >= 10


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
                if node.name == name and _symbol_lookup_append(results, file_path, "class", node):
                    return results[:10]
                for item in ast.iter_child_nodes(node):
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                        item.name == name or f"{node.name}.{item.name}" == name
                    ):
                        if _symbol_lookup_append(
                            results, file_path, "method", item, class_name=node.name
                        ):
                            return results[:10]
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                if _symbol_lookup_append(results, file_path, "function", node):
                    return results[:10]

    return results


_TOOL_HANDLERS = {
    "list_files": list_files,
    "open_file": open_file,
    "search_code": search_code,
    "symbol_lookup": symbol_lookup,
}


async def execute_tool_call(storage: LocalRepositoryStorage, call: dict[str, Any]) -> str:
    func_name = call.get("function", {}).get("name")
    args_str = call.get("function", {}).get("arguments", "{}")

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
