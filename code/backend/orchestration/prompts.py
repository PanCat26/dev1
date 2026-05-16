from retrieval.types import EvidencePackage


def assemble_evidence_package(evidence_pkg: EvidencePackage) -> str:
    """Format vector-retrieval chunks into a single string for the system prompt."""
    evidence_blocks: list[str] = []

    if evidence_pkg.total_chunks > 0:
        for group in evidence_pkg.groups:
            if not group.chunks:
                continue
            evidence_blocks.append(f"### {group.description} ({group.role}) ###\n")
            for chunk in group.chunks:
                line_range = (
                    f"[{chunk.start_line}-{chunk.end_line}]" if chunk.start_line else ""
                )
                block = (
                    f"File: {chunk.file_path} {line_range}\nContent:\n```\n{chunk.text}\n```\n"
                )
                evidence_blocks.append(block)

    if not evidence_blocks:
        return "No relevant evidence found in the repository."

    return "\n".join(evidence_blocks)


def build_system_prompt(evidence_package: str) -> str:
    """Build system prompt with hallucination / tool-use instructions plus evidence."""
    system_message = (
        "You are an expert Python coding assistant specifically designed to help users with the currently active repository.\n"
        "You have access to a set of repository inspection tools. If the initial retrieved evidence does not contain enough information to form a conclusive technical answer, you MUST use your tools to explore the codebase (for example, by listing files, opening files, or searching code).\n"
        "Only after you have exhausted your tools and still cannot find the answer should you return an explicit insufficient-evidence response.\n"
        "Do not hallucinate files, names, or code regions. Always cite the file path and line numbers when referring to code.\n\n"
        "The following initial evidence has been collected for the user's query:\n\n"
    )

    return (
        system_message
        + evidence_package
        + "\n\nCRITICAL: Think step by step. Use your tools to find the answer if it's missing in the initial evidence."
    )
