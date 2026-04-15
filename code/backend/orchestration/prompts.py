from typing import List, Dict, Any

def assemble_evidence_package(retrieved_chunks: List[Dict[str, Any]], tool_outputs: List[Dict[str, Any]]) -> str:
    """
    Format the evidence from vector search and the iterative agent tools into a strictly structured package for the generation prompt.
    """
    evidence_blocks = []
    
    if retrieved_chunks:
        evidence_blocks.append("### Initial Retrieved Evidence (Semantic Search) ###\\n")
        for chunk in retrieved_chunks:
            lines = f"[{chunk.get('start_line')}-{chunk.get('end_line')}]" if chunk.get('start_line') else ""
            block = f"File: {chunk.get('file_path')} {lines}\\nContent:\\n```\\n{chunk.get('content')}\\n```\\n"
            evidence_blocks.append(block)
            
    if tool_outputs:
         evidence_blocks.append("### Agent Inspection Results (Exact Evidence) ###\\n")
         for output in tool_outputs:
             tool_name = output.get('tool')
             args = output.get('params')
             result = output.get('result')
             block = f"Tool Call: {tool_name}({args})\\nOutput:\\n```\\n{result}\\n```\\n"
             evidence_blocks.append(block)
             
    if not evidence_blocks:
        return "No relevant evidence found in the repository."
        
    return "\\n".join(evidence_blocks)

def build_system_prompt(evidence_package: str) -> str:
    """
    Constructs the system prompt that ensures the agent follows hallucination controls and uses the evidence strictly.
    """
    system_message = (
        "You are an expert Python coding assistant specifically designed to help users with the currently active repository.\\n"
        "You must answer user questions based ONLY on the evidence provided. If the retrieved evidence or your tool calls "
        "do not contain enough information to form a conclusive technical answer, you must return an explicit "
        "insufficient-evidence response (e.g. 'I do not have sufficient evidence to answer this from the repository.') \\n"
        "Do not hallucinate files, names, or code regions. Always cite the file path and line numbers when referring to code.\\n\\n"
        "The following evidence package has been collected for the user's query:\\n\\n"
    )
    
    return system_message + evidence_package + "\\n\\nPlease use the provided tool suite if you require further context or inspection."
