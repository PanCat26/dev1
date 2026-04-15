from typing import List, Dict, Any

class MockRetrievalService:
    """
    Mocked retrieval service returning dummy relevant chunks for testing the agentic workflow.
    """
    
    def __init__(self):
        pass
        
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Simulate a Qdrant vector search and metadata-aware reranking.
        Returns mocked chunk evidences.
        """
        return [
            {
                "file_path": "backend/indexing/parser.py",
                "start_line": 10,
                "end_line": 25,
                "content": "class PythonParser:\n    def parse(self, content):\n        pass",
                "score": 0.95,
                "type": "code"
            },
            {
                "file_path": "backend/indexing/chunking.py",
                "start_line": 5,
                "end_line": 15,
                "content": "def chunk_by_symbols(symbols):\n    pass",
                "score": 0.82,
                "type": "code"
            }
        ]
