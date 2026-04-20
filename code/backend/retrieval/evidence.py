from retrieval.types import RetrievedChunk, EvidenceGroup, EvidencePackage


def group_by_role(
    chunks: list[RetrievedChunk],
    primary_types: list[str] | None = None,
    doc_types: list[str] | None = None,
) -> list[EvidenceGroup]:
    """Group chunks by their role in the evidence.
    
    Classifies chunks as:
    - "primary_code": Functions, classes directly matching query intent
    - "related_code": Methods, helper functions related to primary
    - "documentation": Doc sections explaining concepts
    
    Args:
        chunks: Ranked list of retrieved chunks.
        primary_types: Chunk types to treat as primary (default: ["function", "class"]).
        doc_types: Chunk types to treat as documentation (default: ["doc_section"]).
        
    Returns:
        List of EvidenceGroup objects with organized chunks.
    """
    if primary_types is None:
        primary_types = ["function", "class"]
    if doc_types is None:
        doc_types = ["doc_section"]
    
    primary: list[RetrievedChunk] = []
    related: list[RetrievedChunk] = []
    docs: list[RetrievedChunk] = []
    
    for chunk in chunks:
        if chunk.chunk_type in doc_types:
            docs.append(chunk)
        elif chunk.chunk_type in primary_types:
            primary.append(chunk)
        else:
            # Methods, other code
            related.append(chunk)
    
    groups: list[EvidenceGroup] = []
    
    # Add groups in order of importance
    if primary:
        groups.append(EvidenceGroup(
            role="primary_code",
            chunks=primary,
            description=f"Primary code elements ({len(primary)} chunks)",
        ))
    
    if related:
        groups.append(EvidenceGroup(
            role="related_code",
            chunks=related,
            description=f"Related code ({len(related)} chunks)",
        ))
    
    if docs:
        groups.append(EvidenceGroup(
            role="documentation",
            chunks=docs,
            description=f"Documentation and explanations ({len(docs)} chunks)",
        ))
    
    return groups


def build_evidence_package(
    chunks: list[RetrievedChunk],
    query: str,
    repo_id: str,
    commit_sha: str,
    max_chunks_per_category_in_group: int = 3,
) -> EvidencePackage:
    """Build a structured evidence package for answer generation.
    
    Organizes chunks by role and limits each group to keep context concise.
    The resulting package preserves file paths and line ranges for citations.
    
    Args:
        chunks: Ranked list of retrieved chunks.
        query: The original user query.
        repo_id: Repository ID.
        commit_sha: Commit SHA being queried.
        max_chunks_per_group: Maximum chunks per group (default: 5).
        
    Returns:
        EvidencePackage with organized chunks ready for generation.
    """
    # Group chunks by role
    groups = group_by_role(chunks)
    
    # Limit chunks per group to keep context manageable
    limited_groups = [
        EvidenceGroup(
            role=group.role,
            chunks=group.chunks[:max_chunks_per_category_in_group],
            description=group.description.replace(
                f"({len(group.chunks)} chunks)", 
                f"({len(group.chunks[:max_chunks_per_category_in_group])} chunks)"
            ),
        )
        for group in groups
    ]
    
    # Count total chunks in package
    total_chunks = sum(len(group.chunks) for group in limited_groups)
    
    # Build final package
    return EvidencePackage(
        repo_id=repo_id,
        commit_sha=commit_sha,
        query=query,
        groups=limited_groups,
        total_chunks=total_chunks,
    )
