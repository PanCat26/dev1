import asyncio
import json
import re
import uuid
from typing import Any, AsyncGenerator

import language_model.client as llm_client
import retrieval.service as retrieval_service
from orchestration.prompts import assemble_evidence_package, build_system_prompt
from orchestration.tools import TOOLS_SCHEMA, execute_tool_call
from repository.storage import LocalRepositoryStorage

MAX_AGENT_STEPS = 10


async def answer_query(
    repo_id: str,
    commit_sha: str,
    snapshot_path: str,
    user_query: str,
    history_messages: list[dict[str, str]] | None = None,
) -> AsyncGenerator[str, None]:
    """Retrieve context, run bounded tool-calling loop, stream JSON events."""
    yield json.dumps({"type": "status", "message": "Retrieving semantic context..."})

    storage = LocalRepositoryStorage(snapshot_path)

    evidence_pkg = await asyncio.to_thread(
        retrieval_service.retrieve_for_query,
        query=user_query,
        repo_id=repo_id,
        commit_sha=commit_sha,
    )
    evidence_pkg_str = assemble_evidence_package(evidence_pkg)
    system_prompt = build_system_prompt(evidence_pkg_str)

    prior_turns = history_messages if history_messages else [
        {"role": "user", "content": user_query},
    ]
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        *prior_turns,
    ]

    for step in range(MAX_AGENT_STEPS):
        yield json.dumps({"type": "status", "message": f"Agent step {step + 1}/{MAX_AGENT_STEPS}..."})

        tool_calls: list[dict[str, Any]] = []
        assistant_content = ""

        async for event in llm_client.generate(messages, tools=TOOLS_SCHEMA):
            if event["type"] == "content":
                assistant_content += event["content"]
                yield json.dumps({"type": "content", "delta": event["content"]})
            elif event["type"] == "tool_calls":
                tool_calls = event["tool_calls"]

        if not tool_calls and assistant_content:
            pattern = r'\{\s*"name"\s*:\s*"[^"]+"\s*,\s*"arguments"\s*:\s*\{.*?\}\s*\}'
            for m in re.finditer(pattern, assistant_content, re.DOTALL):
                try:
                    call_dict = json.loads(m.group(0))
                    if "name" in call_dict and "arguments" in call_dict:
                        tool_calls.append(
                            {
                                "id": f"call_{uuid.uuid4().hex[:8]}",
                                "type": "function",
                                "function": {
                                    "name": call_dict["name"],
                                    "arguments": json.dumps(call_dict["arguments"])
                                    if isinstance(call_dict["arguments"], dict)
                                    else str(call_dict["arguments"]),
                                },
                            }
                        )
                except (json.JSONDecodeError, TypeError, KeyError):
                    pass

        assistant_message: dict[str, Any] = {"role": "assistant"}
        if assistant_content:
            assistant_message["content"] = assistant_content

        if tool_calls:
            assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)

            for call in tool_calls:
                yield json.dumps(
                    {
                        "type": "tool_call",
                        "name": call.get("function", {}).get("name"),
                        "arguments": call.get("function", {}).get("arguments"),
                    }
                )
                tool_result = await execute_tool_call(storage, call)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.get("id"),
                        "name": call.get("function", {}).get("name"),
                        "content": tool_result,
                    }
                )
        else:
            messages.append(assistant_message)
            return

    yield json.dumps({"type": "status", "message": "Finalizing answer without tools..."})
    async for event in llm_client.generate(messages, tools=None):
        if event["type"] == "content":
            yield json.dumps({"type": "content", "delta": event["content"]})
