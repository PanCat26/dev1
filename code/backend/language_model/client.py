from collections.abc import AsyncIterator

from openai import AsyncOpenAI

import config


_MODEL_NAME = "qwen2.5-coder"

client = AsyncOpenAI(
    base_url=f"{config.LLAMA_SERVER_URL}/v1",
    api_key="not-needed",
)


async def generate(
    messages: list[dict],
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> AsyncIterator[str]:
    """Stream token deltas from the local llama-server.

    Usage:

        async for token in generate(messages):
            ....
    """
    stream = await client.chat.completions.create(
        model=_MODEL_NAME,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
