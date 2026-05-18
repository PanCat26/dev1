import asyncio
import json
import uuid
from typing import Any, AsyncGenerator

import language_model.client as llm_client
import retrieval.service as retrieval_service
from orchestration.prompts import assemble_evidence_package, build_system_prompt
from orchestration.tools import TOOLS_SCHEMA, execute_tool_call
from repository.storage import LocalRepositoryStorage

MAX_AGENT_STEPS = 10

_KNOWN_TOOL_NAMES = frozenset(
    t["function"]["name"] for t in TOOLS_SCHEMA if t.get("type") == "function"
)


def _tool_calls_from_assistant_text(content: str) -> list[dict[str, Any]]:
    """Parse tool-shaped JSON from assistant text when the stream omits delta.tool_calls."""
    dec = json.JSONDecoder()
    found: list[dict[str, Any]] = []
    n = len(content)
    i = 0

    def maybe_append(call_dict: dict[str, Any]) -> None:
        name = call_dict.get("name")
        if name not in _KNOWN_TOOL_NAMES or "arguments" not in call_dict:
            return
        raw_args = call_dict["arguments"]
        if isinstance(raw_args, dict):
            args_str = json.dumps(raw_args)
        elif isinstance(raw_args, str):
            args_str = raw_args
        else:
            args_str = json.dumps(raw_args)
        found.append(
            {
                "id": f"call_{uuid.uuid4().hex[:16]}",
                "type": "function",
                "function": {"name": name, "arguments": args_str},
            }
        )

    while i < n:
        if content[i] not in "{[":
            i += 1
            continue
        try:
            obj, end = dec.raw_decode(content, i)
        except json.JSONDecodeError:
            i += 1
            continue
        if isinstance(obj, dict):
            maybe_append(obj)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    maybe_append(item)
        i = end if end > i else i + 1
    return found


def _ensure_tool_call_ids(tool_calls: list[dict[str, Any]]) -> None:
    for call in tool_calls:
        if not call.get("id"):
            call["id"] = f"call_{uuid.uuid4().hex[:16]}"
        call.setdefault("type", "function")


async def answer_query(
    repo_id: str,
    commit_sha: str,
    snapshot_path: str,
    user_query: str,
    history_messages: list[dict[str, str]] | None = None,
) -> AsyncGenerator[str, None]:
    """Stream retrieval, tools, and model output."""
    user_query = user_query.strip()
    if not user_query:
        yield json.dumps({"type": "error", "message": "Empty message."})
        return

    yield json.dumps({"type": "status", "message": "Retrieving semantic context..."})

    storage = LocalRepositoryStorage(snapshot_path)

    try:
        evidence_pkg = await asyncio.to_thread(
            retrieval_service.retrieve_for_query,
            query=user_query,
            repo_id=repo_id,
            commit_sha=commit_sha,
        )
    except ValueError as e:
        yield json.dumps({"type": "error", "message": str(e)})
        return

    evidence_pkg_str = assemble_evidence_package(evidence_pkg)
    system_prompt = build_system_prompt(evidence_pkg_str)

    prior = list(history_messages or [])
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        *prior,
        {"role": "user", "content": user_query},
    ]

    for step in range(MAX_AGENT_STEPS):
        yield json.dumps({"type": "status", "message": f"Agent step {step + 1}/{MAX_AGENT_STEPS}..."})

        tool_calls: list[dict[str, Any]] = []
        assistant_content = ""
        
        import random
        from config import RLHF_PROBABILITY
        
        is_rlhf = random.random() < RLHF_PROBABILITY
        rlhf_started = False
        gen2_task = None
        gen2_queue = asyncio.Queue()
        assistant_content_alt = ""

        async def run_gen2():
            try:
                async for ev in llm_client.generate(messages, tools=None):
                    if ev["type"] == "content":
                        await gen2_queue.put(ev["content"])
            except Exception:
                pass
            finally:
                await gen2_queue.put(None)

        async for event in llm_client.generate(messages, tools=TOOLS_SCHEMA):
            if event["type"] == "content":
                if is_rlhf and not rlhf_started:
                    rlhf_started = True
                    yield json.dumps({"type": "rlhf_start"})
                    gen2_task = asyncio.create_task(run_gen2())
                    
                assistant_content += event["content"]
                yield json.dumps({"type": "content", "delta": event["content"]})
                
                while not gen2_queue.empty():
                    alt_delta = gen2_queue.get_nowait()
                    if alt_delta is not None:
                        assistant_content_alt += alt_delta
                        yield json.dumps({"type": "content_alt", "delta": alt_delta})
                        
            elif event["type"] == "tool_calls":
                tool_calls = event["tool_calls"]

        if not tool_calls and assistant_content:
            tool_calls = _tool_calls_from_assistant_text(assistant_content)

        assistant_message: dict[str, Any] = {"role": "assistant"}
        if assistant_content:
            assistant_message["content"] = assistant_content

        if tool_calls:
            if "content" not in assistant_message:
                assistant_message["content"] = None
            _ensure_tool_call_ids(tool_calls)
            assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)

            for call in tool_calls:
                yield json.dumps(
                    {
                        "type": "tool_call",
                        "id": call.get("id"),
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
            if assistant_content.strip():
                if rlhf_started:
                    while True:
                        try:
                            alt_delta = gen2_queue.get_nowait()
                            if alt_delta is None:
                                break
                            assistant_content_alt += alt_delta
                            yield json.dumps({"type": "content_alt", "delta": alt_delta})
                        except asyncio.QueueEmpty:
                            if gen2_task and gen2_task.done():
                                break
                            await asyncio.sleep(0.05)
                            
                    yield json.dumps({
                        "type": "rlhf_prompt", 
                        "prompt": json.dumps(messages)
                    })
                    
                messages.append(assistant_message)
                return
            yield json.dumps(
                {"type": "error", "message": "Model returned no text and no tool calls."}
            )
            return

    yield json.dumps(
        {
            "type": "status",
            "message": (
                f"Agent step limit ({MAX_AGENT_STEPS}) reached; answering without tools."
            ),
        }
    )
    async for event in llm_client.generate(messages, tools=None):
        if event["type"] == "content":
            yield json.dumps({"type": "content", "delta": event["content"]})
    return
