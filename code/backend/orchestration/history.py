"""Bounded conversation history for the LLM."""

from typing import Any, Sequence

# Last N rows from DB (user + assistant only), after filtering.
MAX_HISTORY_MESSAGES = 10
MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_TOTAL_CHARS = 12000

_TRUNC = "\n...[truncated]"


def bounded_history_for_llm(messages: Sequence[Any]) -> list[dict[str, str]]:
    """
    Turn persisted messages (ORM or any object with .role and .content) into
    OpenAI-style {"role","content"} dicts for the chat API.

    Policy: take the last MAX_HISTORY_MESSAGES entries whose role is user or
    assistant; truncate each body to MAX_MESSAGE_CHARS; if the combined
    length exceeds MAX_HISTORY_TOTAL_CHARS, drop from the oldest until under
    the cap (most recent turns kept).
    """
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
