import re

from indexing.types import Chunk, ParsedSymbol


def chunks_from_symbols(
    symbols: list[ParsedSymbol],
    repo_id: str,
    commit_sha: str,
) -> list[Chunk]:
    """Convert parsed symbols into Chunk objects."""
    return [
        Chunk(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=s.file_path,
            chunk_type=s.symbol_type,
            symbol_name=s.symbol_name,
            start_line=s.start_line,
            end_line=s.end_line,
            text=s.text,
        )
        for s in symbols
    ]


# Matches lines that start with one or more '#' (markdown headings)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)", re.MULTILINE)


def chunks_from_markdown(
    file_path: str,
    text: str,
    repo_id: str,
    commit_sha: str,
) -> list[Chunk]:
    """Split markdown text into chunks by top-level headings.

    Each heading and the body below it become one chunk.
    If the file has no headings, the entire text is one chunk.
    """
    headings = list(_HEADING_RE.finditer(text))

    if not headings:
        stripped = text.strip()
        if not stripped:
            return []
        return [Chunk(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=file_path,
            chunk_type="doc_section",
            symbol_name="(whole file)",
            start_line=1,
            end_line=text.count("\n") + 1,
            text=stripped,
        )]

    chunks: list[Chunk] = []

    # Text before the first heading (if any)
    preamble = text[: headings[0].start()].strip()
    if preamble:
        chunks.append(Chunk(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=file_path,
            chunk_type="doc_section",
            symbol_name="(preamble)",
            start_line=1,
            end_line=text[: headings[0].start()].count("\n") + 1,
            text=preamble,
        ))

    for i, match in enumerate(headings):
        section_start = match.start()
        section_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section_text = text[section_start:section_end].strip()
        if not section_text:
            continue

        start_line = text[:section_start].count("\n") + 1
        end_line = text[:section_end].count("\n") + 1

        chunks.append(Chunk(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=file_path,
            chunk_type="doc_section",
            symbol_name=match.group(2).strip(),
            start_line=start_line,
            end_line=end_line,
            text=section_text,
        ))

    return chunks
