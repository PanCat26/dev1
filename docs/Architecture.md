# dev1: Architecture

## Summary

This document presents the architecture of the **dev1** Python coding agent. The agent enables users to load a repository together with its technical documentation and interact with it through a chat-based interface. Its purpose is to support repository-specific tasks such as explaining project structure and behavior, locating relevant files or symbols, identifying likely sources of defects, and suggesting grounded fixes when sufficient evidence is available.

This document describes the system from an architectural perspective, focusing on its main components, services, data stores, interactions, and operational flows. It covers the overall system structure, repository ingestion mechanism, chunking and indexing strategy, vector database and model choice, and retrieval and generation pipeline.

## High-level architecture

The system follows the RFC’s proposed **modular monolith with specialized services**. At a high level, the architecture is composed of the following major parts:

1. **Frontend application** implemented with Next.js/React
2. **Backend application** implemented with FastAPI
3. **Repository snapshot storage** on disk
4. **PostgreSQL** for metadata and application state
5. **Qdrant** for vector storage and retrieval
6. **vLLM model-serving process** exposing an OpenAI-compatible API for the fine-tuned small language model

From an architecture-documentation perspective, these map naturally to the following layers:

- **Presentation layer:** web client
- **Application layer:** FastAPI endpoints, orchestration, ingestion and retrieval control, answer assembly, feedback handling
- **Model layer:** generation model
- **Data layer:** PostgreSQL, Qdrant, and repository snapshot storage

This structure is consistent with typical LLM application architecture.

> **Diagram placeholder:** diagrama mare gen ce mi-a aratat Teo

## System components

### 1. Frontend application

The frontend is a Next.js/React web client responsible for:

- repository upload or selection
- display of repository metadata and indexing status
- chat-based interaction with the active repository
- streamed display of model responses, which include repository-grounding evidence (file paths, line ranges)
- collection of user feedback (pairwise answer selection).

The frontend's role is to coordinate user interactions and render backend-provided results.

### 2. Backend application

The FastAPI backend acts as the central coordinator of the system. It exposes REST endpoints for repository and indexing operations and WebSocket endpoints for incremental answer streaming. Internally, the backend is organized into specialized components.

> **Diagram placeholder:** diagrama mai mica doar cu backend-ul

#### 2.1. Repository management service

This service is responsible for CRUD operations on repository records, including uploading repositories and associating them with a specific commit SHA. It is also responsible for managing active chats inside a specific repository. The service's main purpose is to configure the specific repository snapshot that downstream questions inside chats address.

It also manages repository lifecycle information such as indexing status, and repository-level metadata required by the rest of the system.

A specific functionality of this service is handling new commits for a specific repository. When a user triggers a repository sync, the service starts a reindexing job for the new snapshot, keeps the previous on-disk snapshot and Qdrant chunks available while queries continue to use the old active version, and switches to the new indexed version only after indexing completes successfully.

#### 2.2. Indexing service

The indexing service processes a repository after upload. The associated workflow runs as a background task managed from the FastAPI application.

Its responsibilities are:

- scanning the repository tree
- selecting supported code and documentation files
- parsing Python files with the built-in `ast` module
- extracting high-level symbols such as modules, classes, functions, and methods
- splitting code and documentation into retrieval chunks
- generating embeddings for chunks
- storing chunk vectors and metadata in Qdrant.

The chunking strategy is structure-aware and depends on content type:

- **Code chunking:** code is chunked around meaningful program units such as functions, methods, and classes rather than by arbitrary fixed-size windows. For example, a function chunk includes the function signature, body, docstring when present, file path, and line range. A class chunk includes the class definition and, when useful, major methods or method signatures.
- **Documentation chunking:** markdown and README-style documentation is chunked by section heading so that retrieved passages preserve local topic context.

This strategy is chosen because repository questions are often asked in terms of symbols, definitions, or localized behaviors. Structure-aware chunks therefore provide better retrieval granularity and better evidence for answer generation.

#### 2.3. Embedding and retrieval service

The embedding and retrieval service is responsible for converting chunks and queries into vectors, running semantic search against Qdrant, and producing ranked evidence candidates for downstream answer generation.

Qdrant is used as the vector database because it stores embeddings together with structured payload metadata and supports efficient similarity search and metadata-aware filtering. Each indexed chunk should store, at minimum:

- repository id
- commit SHA
- file path
- chunk type
- start and end lines.

The retrieval strategy is hybrid rather than purely vector-based. Semantic retrieval is used to find conceptually relevant code or documentation fragments, while lightweight exact-match signals are used to improve precision when queries mention explicit symbol names, file names, strings, or other repository-specific identifiers. The service therefore supports a two-stage ranking process:

1. retrieve top candidates from Qdrant using embeddings
2. rerank or boost candidates whose metadata matches query terms such as symbol or file names.

The output of this service is not a single unstructured text block. Instead, the service should assemble a compact evidence package in which the most relevant chunks are grouped by role (e.g. primary code evidence, related code evidence, documentation evidence), while preserving file paths and line ranges. This structured context is then forwarded to the orchestration service, which incorporates it into the final prompt for grounded answer generation.

#### 2.4. Orchestration (answer) service

The orchestration service implements the bounded agentic behavior of the assistant. Instead of using only a single retrieve-and-answer call, it follows a short controlled workflow:

1. analyze the query;
2. retrieve likely evidence;
3. optionally inspect exact file regions from the stored repository snapshot;
4. assemble evidence for the model;
5. generate the answer;
6. verify that the response remains tied to retrieved evidence.

The first version should keep this workflow limited. The assistant should use an initial tool set of: 
- `list_files(path_prefix=None)`
- `open_file(file_path, start_line=None, end_line=None)`
- `search_code(query)`
- `symbol_lookup(name)`.

This service is where the main RAG strategy is enforced. The model must answer from retrieved repository evidence rather than from unsupported prior knowledge. If the evidence is weak or insufficient, the service should return an explicit insufficient-evidence response rather than a confident but ungrounded answer.

Additionally, the orchestration service should support a lightweight human preference feedback mechanism. For a subset of queries, the system will occasionally generate two candidate answers to the same prompt and present them to the user for pairwise selection. The selected preference will be stored as training data for later offline preference optimization through **DPO**.

In the first version, we will implement the service ourselves. If the workflow becomes more complex later on, we will introduce LangGraph as the orchestration framework.

#### 2.5. Evaluation service

For evaluation, we support both automatic retrieval evaluation and smaller manual end-to-end checks. The evaluation service handles the automatic evaluation.

The service should be implemented as a backend-executed batch workflow that can be triggered separately from normal user interaction. For each evaluation run, it operates on a held-out set of repositories, executes the same indexing and retrieval pipeline used by the main application, computes retrieval metrics from generated evaluation queries, and stores the resulting metrics and run metadata for later inspection and comparison.

To keep evaluation automatic, the service generates evaluation queries from held-out Python repositories. For each repository, it parses the source files with `ast`, extracts symbols such as functions and classes, and builds simple template-based questions, for example asking where a function is defined or in which file a class appears. Since the repository is parsed directly by the backend, the correct file path and, in many cases, the correct line range are already known and can be used as gold labels.

The reported metrics then are:

- **Top-1 accuracy**
- **Recall@3**
- **Recall@5**.

#### 2.6. Model serving integration

The model is served through a separate vLLM server, and the backend services will communicate with it using the corresponding OpenAI-compatible API. This keeps model execution isolated from the main application while preserving a simple request interface for generation.

The primary model choice is **Qwen2.5-Coder-7B-Instruct**, a small code-capable instruction model in the 7B range. This size is large enough to support code understanding and repository-aware answer synthesis, while still remaining feasible for fine-tuning and serving in a project setting.

Model adaptation is performed offline. The main supervised dataset is **OpenCodeInstruct**, which is appropriate for code-focused instruction tuning. If needed to improve code-text alignment, the training mix can include the **Python split of CodeSearchNet**. Because the system is specifically designed for Python repositories, Python examples should be prioritized in any training mix.

To reduce compute requirements, fine-tuning will use **PEFT** (**QLoRA**), rather than full-model training. After adaptation, the resulting model is deployed behind the vLLM server and used as the final generator over retrieved repository evidence.

### 3. Data stores

The system uses complementary data stores, each chosen for a distinct persistence concern.

> **Diagram placeholder:** diagrama mica cu data store-urile (maybe)

#### 3.1. PostgreSQL

PostgreSQL stores structured application state and metadata. It acts as the main relational persistence layer for the system.

Typical stored data includes:

- repository records, with current commit and metadata
- indexing job status
- user sessions and chat records
- feedback records
- evaluation metadata and experiment tracking.

PostgreSQL is used for the operational state, while Qdrant is used specifically for retrieval over chunk embeddings.

#### 3.2. Qdrant

Qdrant stores the vectorized representation of repository code and documentation chunks. It is the main retrieval store used during question answering.

Each record in Qdrant should contain:

- the embedding vector for the chunk
- repository id
- commit SHA
- file path
- chunk type
- start and end lines;
- any additional metadata needed for filtering or reranking.

Qdrant is selected as the vector database because it supports semantic vector retrieval together with metadata-based filtering, which is needed to restrict retrieval to repository-specific chunks, commit versions, file paths, symbols, and line ranges.

#### 3.3. Repository snapshot storage

The original repository snapshot will be stored persistently on disk. This storage is required even after indexing, because retrieval alone is not always sufficient for grounded answers. The stored snapshot will be tied to a repository identifier and a commit SHA.

The orchestrator may need to reopen the exact file and inspect a larger code region than the original chunk. Persistent repository snapshots therefore serve as the source of truth for exact code inspection and answer citation.

#### 3.4. Training artifact storage

Training artifacts are stored persistently on disk. These include the fine-tuning configuration and the resulting saved adapters or merged checkpoint, which can later be loaded by the vLLM serving process.

## Example system flows

### 1. Repository ingestion and indexing flow

When a user adds a repository, the backend creates a repository record, stores the uploaded snapshot, and schedules an ingestion job. The ingestion service scans the repository, parses Python files with `ast`, extracts symbols, creates structure-aware chunks for code and documentation, generates embeddings, and stores the resulting vectors and metadata in Qdrant. Repository metadata and indexing status are stored in PostgreSQL.

This flow establishes the repository snapshot that all future answers must reference.

> **Diagram placeholder:** diagrama ptr asta

### 2. Query answering flow

When a user asks a question, the web client sends the query to the backend. The orchestration service analyzes the query and invokes retrieval. The retrieval service embeds the query, searches Qdrant for relevant chunks, and reranks candidates using metadata-aware exact-match signals when useful. If needed, the orchestration service reopens exact files or line ranges from repository snapshot storage.

The backend then assembles a structured evidence package and sends it to the model through the vLLM server. The generated answer is returned to the client together with its supporting file paths and line references.

If the retrieved evidence is insufficient, the backend should return an explicit insufficient-evidence response instead of generating a speculative answer.

> **Diagram placeholder:** diagrama ptr asta

### 3. Evaluation flow

The automatic evaluation service runs on held-out repositories. It parses the repositories, extracts symbols, creates template-based evaluation questions, and evaluates whether retrieval returns the correct file or chunk in the top ranked results. Metrics such as Top-1 accuracy, Recall@3, and Recall@5 are then reported.

> **Diagram placeholder:** diagrama ptr asta

## Implementation plan

### Week 7
- Backend and repository ingestion

### Week 8
- Chunking, embeddings, and vector indexing

### Week 9
- Retrieval and answer orchestration
- vLLM integration

### Week 10
- Frontend integration
- Chat flow
- Preference feedback flow

### Week 11
- Evaluation and system checks

### Week 12
- Demo, presentation, and final validation
