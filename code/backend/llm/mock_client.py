from typing import List, Dict, Any, Optional

class MockLLMClient:
    """
    Mocked LLM client that acts as an OpenAI-compatible endpoint.
    Mainly used to build the orchestration tool-calling loop without hitting an actual vLLM server.
    """
    
    def __init__(self):
        pass

    def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Simulate a chat completion optionally requesting a tool call.
        """
        # For mock purposes, just return a dummy response
        last_msg = messages[-1]["content"] if messages else ""
        if tools and "list_files" in last_msg:
                return {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {
                                "name": "list_files",
                                "arguments": "{}"
                            }
                        }
                    ]
                }
             
        return {
            "role": "assistant",
            "content": f"Mock generated answer for: {last_msg[:20]}..."
        }
