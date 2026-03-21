# dev1: Python Coding Agent

## Summary

This RFC proposes a repo-aware coding assistant for Python Git codebases that can ingest a repository and its accompanying technical documentation, then support users through a chat-based interface. The assistant is intended to answer repository-specific questions based on the current codebase and docs, helping users understand project structure and behavior, locate relevant components (including likely sources of bugs), and suggest relevant fixes when appropriate. To support this, the system should combine a language model with retrieval over the active repository and documentation, so that responses remain tied to the actual project rather than relying only on generic pretrained knowledge. The proposed solution should also support ingestion of new repositories and include a lightweight human feedback loop, such as like/dislike feedback on responses.

## Goals

- **Project-specific technical assistance (rather than general chat)** \
Keep the assistant focused on the currently selected Python project, with emphasis on practical repository navigation and code-related guidance.

- **Chat-based user interface** \
Provide a clear chat interface through which users can load a Python Git repository and its technical documentation, ask questions about the current project, and receive repository-specific answers and guidance.

- **Support ingestion of new codebases and documentation** \
Allow users to load new repositories in the app, as well as new documentation to already loaded repositories. 

- **Repository-grounded answers through retrieval (RAG)** \
Ensure that the assistant answers questions by relying on the currently ingested codebase and docs, so that responses rely on more than prior knowledge.

- **Fine-tuned small language model (SLM)** \
Use a fine-tuned SLM as the core language model so the system is better adapted to repository-specific technical Q&A, code understanding, and fix suggestion.

- **Human feedback loop (RLHF)** \
Incorporate a feedback mechanism, such as choosing between two candidate responses, so the system can gather user preferences and improve answer quality.

- **Evaluation pipeline for system quality** \
Include a clear evaluation process for measuring how well the assistant answers queries.

- **Limit hallucinations** \
Reduce unsupported or invented claims by keeping answers anchored in the ingested repository and documentation.

## Proposed solution

The system will be implemented as a modular monolith with specialized services. The implementation consists of: **(1)** a Next.js/React web client for repository selection, chat, and user feedback; **(2)** a FastAPI backend exposing REST endpoints for repository management and WebSocket endpoints for streamed answers; will aditionally serve as storage for the uploaded repository files; **(3)** PostgreSQL database for metadata and application state; **(4)** Qdrant for vectors and retrieval;  **(5)** a dedicated vLLM model-serving process exposing an OpenAI-compatible API for the fine-tuned SLM. FastAPI is a strong fit here because it is a high-performance Python API framework and supports both background tasks and WebSocket-based streaming. vLLM is a good serving choice because it already exposes an OpenAI-compatible HTTP server, which lets the rest of the application talk to the SLM through a stable interface.

### Repository ingestion and indexing pipeline

When a user adds a repository, the backend should create a new repository entry and save the uploaded files on disk. Each ingested repository should be tied to a specific snapshot, identified by a repository id and preferably  a commit SHA. This is important because the assistant must answer questions about a fixed version of the codebase rather than about files that may later change.

The ingestion workflow should run in the background after the repository is uploaded or cloned. In the initial version, this can be implemented with FastAPI background tasks. The workflow should perform the following steps: save the repository files, scan the directory tree, extract supported files, parse Python source files, split code and documentation into chunks, generate embeddings for those chunks, and insert the resulting vectors and metadata into Qdrant. If the repository comes from Git, the system should record the current commit SHA so that answers can later mention the exact indexed version.

Since the target domain is Python repositories, indexing should be aware of source-code structure. For Python files, the system should use Python’s built-in `ast` module to detect high-level symbols such as modules, classes, and functions. This allows the assistant to index code in meaningful units instead of splitting source files into arbitrary fixed-size blocks. In a first version, this is enough; more advanced parsers are optional and can be added later.

Chunking should depend on the content type. For code, chunks should usually be created around functions, methods, and classes, because these units are more meaningful than arbitrary fixed-size windows. A function chunk should contain the function signature, body, docstring if present, file path, and line range. A class chunk should contain the class definition and, when useful, its main methods or method signatures. For documentation files such as README files or markdown documentation, chunks should be created by section headings so that retrieved passages still preserve their context.

Each chunk stored in Qdrant should include not only its embedding, but also metadata such as repository id, commit SHA, file path, chunk type, symbol name if applicable, and line numbers. This metadata is needed for filtering during retrieval and for showing the user where an answer came from. The original repository snapshot should also be kept on disk so that, after retrieval, the backend can reopen the corresponding source file and inspect the full code region if additional context is needed.

### Retrieval and repository-grounded answering

The assistant should answer repository questions through RAG rather than by relying only on the language model’s prior knowledge. Since the full repository cannot be sent to the model for every question, the system first needs to retrieve the most relevant code and documentation fragments and only then build the final prompt.

The retrieval layer should use Qdrant as the main storage and search component for indexed chunks. Each chunk should be converted into an embedding vector and stored together with its metadata. When a user asks a question, the system should embed the query and search Qdrant for the most relevant chunks. The retrieved chunks are then passed to the language model as supporting context.

Because repository questions often depend both on semantic meaning and on exact names, retrieval should combine vector search with lightweight exact-match signals. The backend should first retrieve the top chunks from Qdrant using embeddings, then rerank them by boosting chunks whose metadata matches file names or symbol names from the query.

The retrieved context should not be passed to the model as one unstructured block. Instead, the backend should organize it into a small evidence package, for example grouping together primary code evidence, related code evidence, and documentation evidence. This makes the model’s input cleaner and helps reduce hallucinations.

### Agentic orchestration

The system should include an agentic component, rather than using only a single retrieve-and-answer call. The goal is to build a repo-aware assistant that can take a few structured steps before answering. This is useful for questions that require inspecting more than one file or following references between symbols.

A practical design is to implement the assistant as a small workflow with several stages: query analysis, retrieval, optional tool use, answer generation, and answer verification. This can be implemented with a simple controller in the backend, or with a lightweight orchestration library if desired. The important point is that the workflow remains bounded and predictable.

The initial tool set should remain small and repository-specific. Useful tools include:

- `list_files(path_prefix=None)` to inspect the repository tree
- `open_file(file_path, start_line=None, end_line=None)` to read exact regions from the stored repository snapshot
- `search_code(query)` to search code text for exact names, strings, or identifiers
- `search_docs(query)` to search documentation text
- `symbol_lookup(name)` to locate a class or function definition in the repository
- `find_references(symbol_name)` to locate simple usages of a symbol across files
- `suggest_patch(target_file, instruction)` to draft a possible fix for a specific file

A typical workflow for a harder question should be: retrieve likely chunks from Qdrant, inspect the most relevant file or code region in the stored repository snapshot, optionally inspect one or two related files, and then compose the answer. For bug-related questions, the system can follow a more specific pattern: identify likely files, inspect the relevant definitions, inspect nearby usages or configuration, and only then explain the likely cause. If enough evidence is found, the assistant may also propose a draft fix.

To keep the system manageable, the first version should avoid unrestricted tool use. The agent should be limited to a small number of steps, for example two or three retrieval or inspection rounds before producing an answer. This keeps latency reasonable and makes the system easier to evaluate.

### Fine-tuned small language model

The core model should be a small code-capable language model in the 7B parameter range such as Qwen2.5-Coder-7B-Instruct, served through vLLM and exposed to the backend through an OpenAI-compatible API. The purpose of fine-tuning is not to teach the model programming from scratch, but to adapt it to the types of code understanding and code generation tasks required by the assistant.

The supervised fine-tuning stage should rely primarily on a small number of existing code datasets. The main supervised fine-tuning dataset should be **OpenCodeInstruct**, since it is an instruction-tuning dataset designed specifically for code LLMs and contains around 5 million coding question-answer pairs for supervised fine-tuning. To strengthen code understanding and code-search behavior, the model can be further trained or mixed with the **Python split of CodeSearchNet**, which contains large-scale natural-language and code pairs built from function-level comments and code. 

Since the assistant is focused on Python repositories, the fine-tuning setup should prioritize Python examples from the any used dataset.

To keep the project feasible, fine-tuning should use parameter-efficient methods rather than full-model training. A practical setup is to use Hugging Face Transformers together with PEFT and LoRA or QLoRA. This reduces hardware requirements while still allowing the base model to be adapted to the target task. After fine-tuning, the model can be deployed behind a vLLM server and called from the FastAPI backend through an OpenAI-compatible HTTP interface.

The human feedback objective should also be implemented in a lightweight way. Instead of a full online RLHF pipeline, the system can collect user feedback during normal usage and periodically turn that feedback into a preference dataset. That dataset will later be used for an additional preference-optimization stage, for example with DPO.

### Human feedback loop

The human feedback mechanism will be based on **pairwise answer selection** in order to support later preference tuning with DPO. For selected queries, the system will generate two candidate answers to the same question and ask the user to choose the better one. This feedback format is sufficient for the preference-optimization stage, since DPO is trained on triples consisting of a prompt, a preferred response, and a rejected response.

### Evaluation pipeline

The evaluation should be kept lightweight and should focus primarily on whether the system can retrieve the correct repository evidence. The main quantitative evaluation will be based on automatically generated questions from held-out Python repositories. This keeps the evaluation feasible while still measuring an important part of the assistant: its ability to find the right file or code region before generating an answer.

The automatic evaluation set should be created from repositories that are not used during supervised fine-tuning. For each held-out repository, the backend should parse Python files using the `ast` module and extract symbols such as functions and classes, and optionally selected identifiers or constants. From these extracted elements, the system should generate simple template-based questions such as “Where is `FUNCTION_NAME` defined?”, “In which file is `CLASS_NAME` defined?”, or “Where is `IDENTIFIER` used?”. Since the correct file path, and in many cases the correct line range, are already known from parsing, the gold answers can be generated automatically.

The main quantitative metrics should be **Top-1 accuracy**, **Recall@3**, and **Recall@5**. Top-1 accuracy measures whether the correct file or chunk is the first retrieved result. Recall@3 and Recall@5 measure whether the correct result appears anywhere within the top 3 or top 5 retrieved results.

This automatic evaluation should be complemented by a much smaller manual end-to-end check. A small set of broader repository questions, for example 10 to 20 questions in total, should be prepared and run through the full system. These questions can cover tasks such as explaining how a component works, locating a likely bug source, or suggesting a plausible draft fix. For these questions, it is sufficient to manually assess whether the answer is correct and whether it is grounded in the cited repository evidence.

### Hallucination control and answer policy

Hallucination control will be enforced through retrieval and answer-generation rules rather than through prompting alone. For every user query, the backend will first retrieve the most relevant chunks from Qdrant and, when needed, reopen the corresponding files from the stored repository snapshot for additional context. Only this retrieved evidence will be passed to the model. If the retrieved context is too weak, too limited, or irrelevant to the question, the system should return an explicit insufficient-evidence response instead of generating a confident answer.

Each answer should be linked to its supporting evidence. The backend should attach the file path and, when available, the start and end lines of the chunks used in the final context. The model should then generate the response from that context, and the UI should display the corresponding references. This makes the answer verifiable and keeps the system grounded in the indexed repository snapshot.

### Development

Development should proceed in three stages. First, an MVP should be built and tested locally: the Next.js frontend, FastAPI backend, PostgreSQL, Qdrant, and the repository-storage directory can run together in a simple development environment, while the fine-tuned model is served separately through vLLM’s OpenAI-compatible server. Second, once ingestion, retrieval, and chat are stable, the system should be tested on a small set of held-out Python repositories and the pairwise-feedback flow should be enabled so preference data can start being collected for later DPO tuning. Third, the project should be deployed in a simple cloud setup so that it can be accessed from any browser. A practical deployment stack for this stage is to host the Next.js frontend on Vercel, run the FastAPI backend on a small cloud VM or container service, use managed PostgreSQL and managed Qdrant, and host the vLLM server on a GPU-enabled machine.

### References

1. **FastAPI** — [link](https://fastapi.tiangolo.com/)
2. **vLLM** — [link](https://docs.vllm.ai/en/stable/)
3. **Qdrant** — [link](https://qdrant.tech/documentation/)
4. **PEFT (Parameter-Efficient Fine-Tuning)** — [link](https://huggingface.co/docs/peft)
5. **OpenCodeInstruct** — [link](https://huggingface.co/datasets/nvidia/OpenCodeInstruct)
