from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import config

from retrieval.types import RetrievedChunk


def search_chunks(
    client: QdrantClient,
    query_vector: list[float],
    repo_id: str,
    commit_sha: str | None = None,
    limit: int = 10,
) -> list[RetrievedChunk]:
    """Search Qdrant for chunks similar to the query vector.
    
    Performs semantic search restricted to a specific repository
    and optionally by commit version using Qdrant's filtering capabilities.
    
    Args:
        client: Qdrant client instance.
        query_vector: Embedding vector of the user query.
        repo_id: Repository ID to filter results by (required).
        commit_sha: Commit SHA to filter results by (optional).
        limit: Maximum number of chunks to return (default: 10).
        
    Returns:
        List of RetrievedChunk objects sorted by vector similarity score.
        
    Raises:
        ValueError: If repo_id is empty.
    """
    if not repo_id:
        raise ValueError("repo_id must not be empty")
    
    # Build filter conditions: repo_id is required, commit_sha is optional
    must_conditions = [
        FieldCondition(
            key="repo_id",
            match=MatchValue(value=repo_id),
        )
    ]
    
    if commit_sha:
        must_conditions.append(
            FieldCondition(
                key="commit_sha",
                match=MatchValue(value=commit_sha),
            )
        )
    
    search_filter = Filter(must=must_conditions)
    
    # Query Qdrant using the query_points API
    response = client.query_points(
        collection_name=config.QDRANT_COLLECTION_NAME,
        query=query_vector,
        query_filter=search_filter,
        limit=limit,
        with_payload=True,
    )
    
    # Extract the scored points from the response
    results = response.points
    
    # Convert Qdrant results to our RetrievedChunk format
    # Use .get() with defaults to handle missing or None payload fields
    chunks: list[RetrievedChunk] = []
    for scored_point in results:
        payload = scored_point.payload or {}
        chunk = RetrievedChunk(
            id=str(scored_point.id),
            repo_id=str(payload.get("repo_id", repo_id)),
            commit_sha=str(payload.get("commit_sha", commit_sha or "")),
            file_path=str(payload.get("file_path", "")),
            chunk_type=str(payload.get("chunk_type", "")),
            symbol_name=str(payload.get("symbol_name", "")),
            start_line=int(payload.get("start_line", 0)),
            end_line=int(payload.get("end_line", 0)),
            text=str(payload.get("text", "")),
            vector_score=float(scored_point.score),
            final_score=float(scored_point.score),  # Will be updated during reranking
        )
        chunks.append(chunk)
    
    return chunks
