import json
import asyncio
from typing import Dict, Any, AsyncGenerator

from orchestration.tools import RepositoryTools, TOOLS_SCHEMA
from orchestration.prompts import assemble_evidence_package, build_system_prompt
from repository.storage import LocalRepositoryStorage
import retrieval.service as retrieval_service
import language_model.client as llm_client

class OrchestrationService:
    """
    Implements the agentic bounded workflow for the coding assistant.
    Responsible for organizing the dialogue, tool calling, and retrieving context.
    """
    
    def __init__(self, repo_id: str, commit_sha: str, snapshot_path: str):
        self.repo_id = repo_id
        self.commit_sha = commit_sha
        self.repo_storage = LocalRepositoryStorage(snapshot_path)
        self.tools = RepositoryTools(self.repo_storage)
        self.max_steps = 10

    async def _execute_tool(self, call: Dict[str, Any]) -> str:
        """Dynamically dispatches tools securely by inspecting defined schemas."""
        func_name = call.get("function", {}).get("name")
        args_str = call.get("function", {}).get("arguments", "{}")
        
        try:
            kwargs = json.loads(args_str)
        except json.JSONDecodeError:
            return f"Error: Failed to parse tool arguments: {args_str}"
            
        tool_method = getattr(self.tools, func_name, None)
        if not tool_method:
            return f"Error: Tool '{func_name}' is not recognized."
            
        try:
            result = await tool_method(**kwargs)
            return json.dumps(result, indent=2) if isinstance(result, (list, dict)) else str(result)
        except Exception as e:
            return f"Error executing tool {func_name}: {str(e)}"

    async def answer_query(self, user_query: str) -> AsyncGenerator[str, None]:
        """
        Main pipeline: analyze -> semantic retrieve -> agent loop -> generation.
        Yields JSON strings mapping stream progression.
        """
        yield json.dumps({"type": "status", "message": "Retrieving semantic context..."})
        
        # 1. Broad retrieval
        evidence_pkg = await asyncio.to_thread(
            retrieval_service.retrieve_for_query,
            query=user_query,
            repo_id=self.repo_id,
            commit_sha=self.commit_sha
        )
        evidence_pkg_str = assemble_evidence_package(evidence_pkg, [])
        system_prompt = build_system_prompt(evidence_pkg_str)
        
        # 2. Agent Dialog Setup
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # 3. Agentic Loop (Bounded Tool Calling)
        for step in range(self.max_steps):
            yield json.dumps({"type": "status", "message": f"Agent step {step + 1}/{self.max_steps}..."})
            
            tool_calls = []
            assistant_content = ""
            
            async for event in llm_client.generate(messages, tools=TOOLS_SCHEMA):
                if event["type"] == "content":
                    assistant_content += event["content"]
                    yield json.dumps({"type": "content", "delta": event["content"]})
                elif event["type"] == "tool_calls":
                    tool_calls = event["tool_calls"]
                    
            if not tool_calls and assistant_content:
                import re, uuid
                pattern = r'\{\s*"name"\s*:\s*"[^"]+"\s*,\s*"arguments"\s*:\s*\{.*?\}\s*\}'
                for m in re.finditer(pattern, assistant_content, re.DOTALL):
                    try:
                        call_dict = json.loads(m.group(0))
                        if "name" in call_dict and "arguments" in call_dict:
                            # Convert to standard OpenAI tool_call schema
                            tool_calls.append({
                                "id": f"call_{uuid.uuid4().hex[:8]}",
                                "type": "function",
                                "function": {
                                    "name": call_dict["name"],
                                    "arguments": json.dumps(call_dict["arguments"]) if isinstance(call_dict["arguments"], dict) else str(call_dict["arguments"])
                                }
                            })
                    except Exception:
                        pass
                        
            assistant_message = {"role": "assistant"}
            if assistant_content:
                assistant_message["content"] = assistant_content
            
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
                messages.append(assistant_message)
                
                # Execute tools
                for call in tool_calls:
                    yield json.dumps({"type": "tool_call", "name": call.get("function", {}).get("name"), "arguments": call.get("function", {}).get("arguments")})
                    tool_result = await self._execute_tool(call)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.get("id"),
                        "name": call.get("function", {}).get("name"),
                        "content": tool_result
                    })
            else:
                messages.append(assistant_message)
                # Generation complete without requesting tools
                return
                
        # 4. If max_steps is reached, force final generation without tools to ensure closure
        yield json.dumps({"type": "status", "message": "Finalizing answer without tools..."})
        async for event in llm_client.generate(messages, tools=None):
            if event["type"] == "content":
                yield json.dumps({"type": "content", "delta": event["content"]})

