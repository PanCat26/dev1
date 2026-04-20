from qdrant.client import get_qdrant_client
from retrieval.embeddings import embed_query
from retrieval.search import search_chunks
from retrieval.ranking import rank_chunks
from retrieval.evidence import build_evidence_package
from retrieval.types import EvidencePackage


def retrieve_for_query(
    query: str,
    repo_id: str,
    commit_sha: str | None = None,
    num_candidates: int = 20,
    max_chunks_per_category_in_package: int = 3,
) -> EvidencePackage:
    """Execute the full retrieval pipeline for a user query.
    
    Performs all steps of the retrieval workflow:
    - Embeds the query using the indexing model
    - Searches Qdrant for semantically similar chunks
    - Applies metadata-based reranking (hybrid retrieval)
    - Groups chunks by role (primary, related, documentation)
    - Returns a structured evidence package
    
    Args:
        query: The user's natural language query.
        repo_id: ID of the repository to search (required).
        commit_sha: Commit SHA version of the repository (optional).
        num_candidates: Number of initial candidates to retrieve (default: 20).
        max_chunks_in_package: Max chunks per group in final package (default: 5).
        
    Returns:
        EvidencePackage with organized, ranked chunks ready for answer generation.
        
    Raises:
        ValueError: If query or repo_id are empty.
        Exception: If Qdrant connection fails or retrieval has issues.
    """
    # Validate required inputs
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    repo_id = repo_id.strip()
    if not repo_id:
        raise ValueError("repo_id must not be empty")
    
    # Step 1: Embed the query
    query_vector = embed_query(query)
    
    # Step 2: Search Qdrant
    client = get_qdrant_client()
    chunks = search_chunks(
        client=client,
        query_vector=query_vector,
        repo_id=repo_id,
        commit_sha=commit_sha,
        limit=num_candidates,
    )
    
    if not chunks:
        return EvidencePackage(
            repo_id=repo_id,
            commit_sha=commit_sha,
            query=query,
            groups=[],
            total_chunks=0,
        )
    
    # Step 3: Rerank using metadata signals
    ranked_chunks = rank_chunks(chunks, query)
    
    # Step 4: Group by role and build evidence package
    return build_evidence_package(
        chunks=ranked_chunks,
        query=query,
        repo_id=repo_id,
        commit_sha=commit_sha,
        max_chunks_per_category_in_group=max_chunks_per_category_in_package,
    )
