import ast
from typing import List, Dict, Optional, Any
from repository.mock_storage import MockRepositoryStorage

class RepositoryTools:
    """Implementations for the four bounded agentic tools on a repository snapshot."""
    
    def __init__(self, repo_storage: MockRepositoryStorage):
        self.repo_storage = repo_storage
        
    def list_files(self, path_prefix: Optional[str] = None) -> List[str]:
        """Inspect the repository tree to find files matching path_prefix."""
        files = self.repo_storage.list_files(path_prefix)
        return files[:50]  # Bound the maximum files returned

    def open_file(self, file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        """Read an exact region of a repository file. If omitted, reads whole file."""
        content = self.repo_storage.get_file_content(file_path)
        if content is None:
            return f"Error: File '{file_path}' not found or unreadable."
            
        lines = content.splitlines()
        
        if start_line is None:
            start_line = 1
        if end_line is None:
            end_line = len(lines)
            
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        chunk_lines = lines[start_idx:end_idx]
        return "\\n".join(chunk_lines)

    def search_code(self, query: str) -> List[Dict[str, Any]]:
        """A simple exact-string match search across the local repository files."""
        results = []
        files = self.repo_storage.list_files()
        
        for file_path in files:
            content = self.repo_storage.get_file_content(file_path)
            if not content:
                continue
                
            lines = content.splitlines()
            for idx, line in enumerate(lines):
                if query in line:
                    results.append({
                        "file_path": file_path,
                        "line_number": idx + 1,
                        "context": line.strip()
                    })
                    if len(results) >= 20: # Limit matched results
                        return results
        return results

    def symbol_lookup(self, name: str) -> List[Dict[str, Any]]:
        """
        Locate a class or function definition in the repository by name using Python's `ast`.
        """
        results = []
        files = self.repo_storage.list_files()
        python_files = [f for f in files if f.endswith('.py')]
        
        for file_path in python_files:
            content = self.repo_storage.get_file_content(file_path)
            if not content:
                continue
                
            try:
                tree = ast.parse(content, filename=file_path)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if node.name == name:
                            # Try to find the docstring and endline
                            end_line = getattr(node, 'end_lineno', node.lineno + 1)
                            results.append({
                                "file_path": file_path,
                                "type": "class" if isinstance(node, ast.ClassDef) else "function",
                                "start_line": node.lineno,
                                "end_line": end_line,
                            })
                            if len(results) >= 10:
                                return results
            except SyntaxError:
                pass  # Ignore files that fail to parse
                
        return results

# Exposing OpenAI compatible tool function schemas
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
                        "description": "The optional directory prefix (e.g., 'src/backend')."
                    }
                },
                "required": []
            }
        }
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
                        "description": "The relative file path."
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "The first line to read (1-indexed)."
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "The last line to read (inclusive)."
                    }
                },
                "required": ["file_path"]
            }
        }
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
                        "description": "The exact string or identifier to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "symbol_lookup",
            "description": "Locate a class or function definition in the repository by its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The exact class or function name to locate."
                    }
                },
                "required": ["name"]
            }
        }
    }
]