from indexing.embeddings import embed_text


def embed_query(query: str) -> list[float]:
    """Convert a user query into an embedding vector.
    
    Args:
        query: The user's natural language query string.
        
    Returns:
        Embedding vector as a list of floats.
        
    Raises:
        ValueError: If query is empty or whitespace only.
    """
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    return embed_text(query)
