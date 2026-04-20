

from retrieval.types import EvidencePackage, RetrievedChunk, EvidenceGroup


def retrieve_for_query(*args, **kwargs):
    """Execute the full retrieval pipeline for a user query.
    
    Lazy imports service to keep module initialization lightweight.
    See retrieval.service.retrieve_for_query for full documentation.
    """
    from retrieval.service import retrieve_for_query as _retrieve_for_query
    return _retrieve_for_query(*args, **kwargs)


__all__ = [
    "retrieve_for_query",
    "EvidencePackage",
    "RetrievedChunk",
    "EvidenceGroup",
]
