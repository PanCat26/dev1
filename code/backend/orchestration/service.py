import json
from typing import List, Dict, Any, Optional
from backend.orchestration.tools import RepositoryTools, TOOLS_SCHEMA
from backend.orchestration.prompts import assemble_evidence_package, build_system_prompt
from backend.retrieval.mock_service import MockRetrievalService
from backend.llm.mock_client import MockLLMClient
from backend.repository.mock_storage import MockRepositoryStorage

class OrchestrationService:
    """
    Implements the agentic bounded workflow for the coding assistant.
    Responsible for organizing the dialogue, tool calling, and retrieving context.
    """
    
    def __init__(self, repo_storage: MockRepositoryStorage, retrieval_client: MockRetrievalService, llm_client: MockLLMClient):
        self.repo_storage = repo_storage
        self.retrieval_client = retrieval_client
        self.llm_client = llm_client
        self.tools = RepositoryTools(repo_storage)
        self.max_steps = 3

    def _execute_tool(self, call: Dict[str, Any]) -> str:
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
            result = tool_method(**kwargs)
            return json.dumps(result, indent=2) if isinstance(result, (list, dict)) else str(result)
        except Exception as e:
            return f"Error executing tool {func_name}: {str(e)}"

    def answer_query(self, user_query: str) -> str:
        """
        Main pipeline: analyze -> semantic retrieve -> agent loop -> hallucination-controlled generation.
        """
        # 1. Broad retrieval
        initial_chunks = self.retrieval_client.semantic_search(user_query)
        evidence_pkg = assemble_evidence_package(initial_chunks, [])
        system_prompt = build_system_prompt(evidence_pkg)
        
        # 2. Agent Dialog Setup
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # 3. Agentic Loop (Bounded Tool Calling)
        for step in range(self.max_steps):
            response = self.llm_client.generate(messages, tools=TOOLS_SCHEMA)
            
            tool_calls = response.get("tool_calls")
            
            # Append the assistant's intermediate thought
            messages.append(response)
            
            if not tool_calls:
                # Generation complete without requesting tools
                return response.get("content", "No answer generated.")
                
            # If there was a tool call, execute it and feed back
            for call in tool_calls:
                tool_result = self._execute_tool(call)
                # Append tool output backward sequentially
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.get("id"),
                    "name": call.get("function", {}).get("name"),
                    "content": tool_result
                })
                
        # 4. If max_steps is reached, force final generation without tools to ensure closure
        final_resp = self.llm_client.generate(messages, tools=None)
        return final_resp.get("content", "Agent hit maximum bounded steps and failed to conclude.")
