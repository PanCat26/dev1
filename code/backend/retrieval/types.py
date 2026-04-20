from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    """A chunk retrieved from Qdrant with its ranking scores."""
    id: str
    repo_id: str
    commit_sha: str
    file_path: str
    chunk_type: str  # "function", "class", "method", "doc_section"
    symbol_name: str
    start_line: int
    end_line: int
    text: str
    vector_score: float  # Similarity score from Qdrant
    final_score: float = 0.0  # Score after reranking with metadata signals


@dataclass
class EvidenceGroup:
    """A group of chunks organized by their role in the evidence."""
    role: str  # "primary_code", "related_code", "documentation"
    chunks: list[RetrievedChunk]
    description: str  # Short description of what this group represents


@dataclass
class EvidencePackage:
    """Final structured evidence assembled for answer generation."""
    repo_id: str
    commit_sha: str
    query: str
    groups: list[EvidenceGroup]
    total_chunks: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization/API response."""
        return {
            "repo_id": self.repo_id,
            "commit_sha": self.commit_sha,
            "query": self.query,
            "groups": [
                {
                    "role": g.role,
                    "description": g.description,
                    "chunks": [
                        {
                            "file_path": c.file_path,
                            "chunk_type": c.chunk_type,
                            "symbol_name": c.symbol_name,
                            "start_line": c.start_line,
                            "end_line": c.end_line,
                            "text": c.text,
                            "vector_score": round(c.vector_score, 3),
                            "final_score": round(c.final_score, 3),
                        }
                        for c in g.chunks
                    ]
                }
                for g in self.groups
            ],
            "total_chunks": self.total_chunks,
        }
