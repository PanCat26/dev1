import os
import re
from retrieval.types import RetrievedChunk

# Stopwords to filter out from query term extraction (common words, not identifiers)
STOPWORDS = {
    "where", "what", "which", "how", "is", "the", "a", "an", "in", "on", "of", 
    "for", "to", "from", "and", "or", "defined", "function", "class", "method", 
    "file", "show", "find", "with", "by"
}


def _normalize_identifier(value: str) -> str:
    """Normalize an identifier by removing non-alphanumeric chars and lowercasing."""
    if not value:
        return ""
    return re.sub(r"[^a-zA-Z0-9_]", "", value).lower()


def extract_query_terms(query: str) -> dict:
    """Extract potential symbol names and file names from query.
    
    Looks for patterns like:
    - CamelCase identifiers (class names)
    - snake_case identifiers (function/variable names)  
    - quoted strings
    - file paths with .py extension
    
    Filters out common stopwords to avoid false positive matches.
    
    Args:
        query: The user's query string.
        
    Returns:
        Dictionary with 'symbols' and 'files' lists.
    """
    symbols = set()
    files = set()
    
    # Extract CamelCase words (class names)
    camel_case = re.findall(r'\b[A-Z][a-zA-Z0-9]*\b', query)
    for term in camel_case:
        if term.lower() not in STOPWORDS:
            symbols.add(term.lower())
    
    # Extract snake_case words (function/variable names) - filter stopwords
    snake_case = re.findall(r'\b[a-z_][a-z0-9_]*\b', query)
    for term in snake_case:
        if term.lower() not in STOPWORDS:
            symbols.add(term.lower())
    
    # Extract quoted strings - keep as is
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', query)
    for match in quoted:
        term = match[0] or match[1]
        symbols.add(term.lower())
    
    # Extract file paths (.py files)
    file_paths = re.findall(r'[\w/.-]+\.py\b', query)
    files.update(f.lower() for f in file_paths)
    
    return {
        "symbols": list(symbols),
        "files": list(files),
    }


def boost_by_metadata(
    chunk: RetrievedChunk,
    query_terms: dict,
    symbol_boost: float = 0.2,
    file_boost: float = 0.15,
) -> float:
    """Calculate a small boost score based on metadata exact matches.
    
    Only boosts on exact or precise matches to avoid false positives.
    
    Args:
        chunk: The retrieved chunk to score.
        query_terms: Dictionary with 'symbols' and 'files' extracted from query.
        symbol_boost: Score boost if symbol name matches (default: 0.2).
        file_boost: Score boost if file path matches (default: 0.15).
        
    Returns:
        Boost score to add to vector similarity score.
    """
    boost = 0.0
    
    # Boost if symbol name is mentioned in query (exact match on normalized identifier)
    chunk_symbol = _normalize_identifier(chunk.symbol_name)
    if chunk_symbol and chunk_symbol in query_terms["symbols"]:
        boost += symbol_boost
    
    # Boost if file path is mentioned in query (full path or basename)
    chunk_file_path = chunk.file_path.lower()
    chunk_file_name = os.path.basename(chunk_file_path)
    if (
        chunk_file_path in query_terms["files"]
        or chunk_file_name in query_terms["files"]
    ):
        boost += file_boost
    
    return boost


def rank_chunks(
    chunks: list[RetrievedChunk],
    query: str,
    symbol_boost: float = 0.2,
    file_boost: float = 0.15,
) -> list[RetrievedChunk]:
    """Rerank chunks using vector score plus small metadata boosts.
    
    Combines semantic similarity from vector search with exact-match signals
    from query terms to produce a final ranking. Boosts are small to preserve
    vector search quality while improving precision on explicit matches.
    
    Args:
        chunks: List of retrieved chunks with vector_score.
        query: The original user query.
        symbol_boost: Score boost for symbol matches (default: 0.2).
        file_boost: Score boost for file matches (default: 0.15).
        
    Returns:
        Reranked list of chunks sorted by final_score (descending).
    """
    query_terms = extract_query_terms(query)
    
    # Calculate final score for each chunk
    for chunk in chunks:
        boost = boost_by_metadata(
            chunk,
            query_terms,
            symbol_boost=symbol_boost,
            file_boost=file_boost,
        )
        chunk.final_score = chunk.vector_score * (1 + boost)
    
    # Sort by final score (descending)
    chunks.sort(key=lambda c: c.final_score, reverse=True)
    
    return chunks
