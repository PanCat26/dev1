from collections.abc import AsyncIterator

from openai import AsyncOpenAI

import config

client = AsyncOpenAI(
    base_url=f"{config.LLAMA_SERVER_URL}/v1",
    api_key="not-needed",
)


async def generate(
    messages: list[dict],
    temperature: float = 0.2,
    max_tokens: int = 2048,
    tools: list[dict] | None = None,
) -> AsyncIterator[dict]:
    """Yield ``{type, content}`` chunks, then ``{type, tool_calls}`` once at end if needed."""
    kwargs: dict = {
        "model": config.LLAMA_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    if tools:
        kwargs["tools"] = tools

    stream = await client.chat.completions.create(**kwargs)
    tool_parts: dict[int, dict] = {}

    async for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if delta is None:
            continue

        if delta.content:
            yield {"type": "content", "content": delta.content}

        for tc in getattr(delta, "tool_calls", None) or []:
            idx = getattr(tc, "index", 0) or 0
            if idx not in tool_parts:
                tool_parts[idx] = {
                    "id": "",
                    "type": "function",
                    "function": {"name": "", "arguments": ""},
                }
            slot = tool_parts[idx]
            if tc.id:
                slot["id"] = tc.id
            if tc.type:
                slot["type"] = tc.type
            if tc.function:
                if tc.function.name:
                    slot["function"]["name"] += tc.function.name
                if tc.function.arguments:
                    slot["function"]["arguments"] += tc.function.arguments

    if tool_parts:
        merged = [tool_parts[i] for i in sorted(tool_parts)]
        yield {"type": "tool_calls", "tool_calls": merged}
