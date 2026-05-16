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
    """Stream token deltas and tool calls from the local llama-server.

    Yields dictionaries representing events:
        {"type": "content", "content": "..."}
        {"type": "tool_calls", "tool_calls": [{"id": "...", "type": "function", "function": {"name": "...", "arguments": "..."}}]}
    """
    kwargs = {
        "model": config.LLAMA_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    if tools:
        kwargs["tools"] = tools

    stream = await client.chat.completions.create(**kwargs)
    
    tool_calls_dict = {}

    async for chunk in stream:
        delta = chunk.choices[0].delta
        
        # Content
        if delta.content:
            yield {"type": "content", "content": delta.content}
            
        # Tool Calls (Streaming accumulation)
        if hasattr(delta, "tool_calls") and delta.tool_calls:
            for tc_delta in delta.tool_calls:
                idx = tc_delta.index
                if idx not in tool_calls_dict:
                    tool_calls_dict[idx] = {
                        "id": "",
                        "type": "function",
                        "function": {"name": "", "arguments": ""}
                    }
                
                if tc_delta.id:
                    tool_calls_dict[idx]["id"] = tc_delta.id
                if tc_delta.type:
                    tool_calls_dict[idx]["type"] = tc_delta.type
                if tc_delta.function:
                    if tc_delta.function.name:
                        tool_calls_dict[idx]["function"]["name"] += tc_delta.function.name
                    if tc_delta.function.arguments:
                        tool_calls_dict[idx]["function"]["arguments"] += tc_delta.function.arguments

    if tool_calls_dict:
        final_tool_calls = [tool_calls_dict[idx] for idx in sorted(tool_calls_dict.keys())]
        yield {"type": "tool_calls", "tool_calls": final_tool_calls}
