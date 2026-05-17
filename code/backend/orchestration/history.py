from typing import Any, Sequence

# Bounds for DB-backed chat history (user + assistant only).
MAX_HISTORY_MESSAGES = 10
MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_TOTAL_CHARS = 12000

_TRUNC = "\n...[truncated]"


def bounded_history_for_llm(messages: Sequence[Any]) -> list[dict[str, str]]:
    """Convert persisted messages to OpenAI-style role/content dicts with size caps."""
    allowed = {"user", "assistant"}
    filtered = [m for m in messages if getattr(m, "role", None) in allowed]
    tail = filtered[-MAX_HISTORY_MESSAGES:]

    entries: list[dict[str, str]] = []
    for m in tail:
        content = m.content or ""
        if len(content) > MAX_MESSAGE_CHARS:
            content = content[: MAX_MESSAGE_CHARS - len(_TRUNC)] + _TRUNC
        entries.append({"role": m.role, "content": content})

    total = sum(len(e["content"]) for e in entries)
    while entries and total > MAX_HISTORY_TOTAL_CHARS:
        removed = entries.pop(0)
        total -= len(removed["content"])

    return entries
