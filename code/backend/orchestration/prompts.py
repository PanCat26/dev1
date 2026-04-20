from typing import List, Dict, Any
from retrieval.types import EvidencePackage

def assemble_evidence_package(evidence_pkg: EvidencePackage, tool_outputs: List[Dict[str, Any]]) -> str:
    """
    Format the evidence from vector search and the iterative agent tools into a strictly structured package for the generation prompt.
    """
    evidence_blocks = []
    
    if evidence_pkg.total_chunks > 0:
        for group in evidence_pkg.groups:
            if not group.chunks:
                continue
            evidence_blocks.append(f"### {group.description} ({group.role}) ###\n")
            for chunk in group.chunks:
                lines = f"[{chunk.start_line}-{chunk.end_line}]" if chunk.start_line else ""
                block = f"File: {chunk.file_path} {lines}\nContent:\n```\n{chunk.text}\n```\n"
                evidence_blocks.append(block)
            
    if tool_outputs:
        evidence_blocks.append("### Agent Inspection Results (Exact Evidence) ###\n")
        for output in tool_outputs:
            tool_name = output.get('tool')
            args = output.get('params')
            result = output.get('result')
            block = f"Tool Call: {tool_name}({args})\nOutput:\n```\n{result}\n```\n"
            evidence_blocks.append(block)
             
    if not evidence_blocks:
        return "No relevant evidence found in the repository."
        
    return "\n".join(evidence_blocks)

def build_system_prompt(evidence_package: str) -> str:
    """
    Constructs the system prompt that ensures the agent follows hallucination controls and uses the evidence strictly.
    """
    system_message = (
        "You are an expert Python coding assistant specifically designed to help users with the currently active repository.\n"
        "You have access to a set of repository inspection tools. If the initial retrieved evidence does not contain enough information to form a conclusive technical answer, you MUST use your tools to explore the codebase (for example, by listing files, opening files, or searching code).\n"
        "Only after you have exhausted your tools and still cannot find the answer should you return an explicit insufficient-evidence response.\n"
        "Do not hallucinate files, names, or code regions. Always cite the file path and line numbers when referring to code.\n\n"
        "The following initial evidence has been collected for the user's query:\n\n"
    )
    
    return system_message + evidence_package + "\n\nCRITICAL: Think step by step. Use your tools to find the answer if it's missing in the initial evidence."
