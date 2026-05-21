from qdrant.client import get_qdrant_client
from retrieval.embeddings import embed_query
from retrieval.search import search_chunks
from retrieval.ranking import rank_chunks
from retrieval.evidence import build_evidence_package
from retrieval.types import EvidencePackage, RetrievedChunk


def retrieve_ranked_chunks(
    query: str,
    repo_id: str,
    commit_sha: str | None = None,
    num_candidates: int = 20,
) -> list[RetrievedChunk]:
    """Run retrieval through embedding → Qdrant search → rerank (no evidence grouping).

    The evidence package reorganizes chunks by role and truncates groups, which is not the
    same ordering as Recall@k / Top-1 over the global ranked list produced here.
    """

    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    repo_id = repo_id.strip()
    if not repo_id:
        raise ValueError("repo_id must not be empty")

    query_vector = embed_query(query)
    client = get_qdrant_client()
    chunks = search_chunks(
        client=client,
        query_vector=query_vector,
        repo_id=repo_id,
        commit_sha=commit_sha,
        limit=num_candidates,
    )
    if not chunks:
        return []
    return rank_chunks(chunks, query)


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
    ranked_chunks = retrieve_ranked_chunks(
        query=query,
        repo_id=repo_id,
        commit_sha=commit_sha,
        num_candidates=num_candidates,
    )
    if not ranked_chunks:
        return EvidencePackage(
            repo_id=repo_id.strip(),
            commit_sha=commit_sha,
            query=query.strip(),
            groups=[],
            total_chunks=0,
        )

    return build_evidence_package(
        chunks=ranked_chunks,
        query=query.strip(),
        repo_id=repo_id.strip(),
        commit_sha=commit_sha,
        max_chunks_per_category_in_group=max_chunks_per_category_in_package,
    )
