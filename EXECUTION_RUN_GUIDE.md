# NewsNexus Execution and Run Guide

## 1. Project Runtime Architecture

### 1.1 What this project actually is

NewsNexus is a local-first Python AI application built around Streamlit, LangGraph, LangChain, Ollama, and embedded Chroma vector stores.

It is not a split frontend/backend web stack.

What exists:

- Streamlit UI and controller: `src/streamlit_app.py`
- LangGraph orchestration center: `src/orchestrator.py`
- Agent node definitions: `src/agents.py`
- RAG ingestion pipeline: `src/ingestion.py`
- Retrieval layer: `src/retrieval.py`
- Unified vector store layer: `src/vector_store.py`
- Tool layer for RAG, web search, and RSS search: `src/tools.py`
- Long-term archive memory: `src/memory_store.py`
- Local vector storage: `data/chroma_db/`, `data/archive_memory/`
- Raw document corpus: `data/raw_pdfs/`

What does not exist in the current workspace:

- No React/Vite/Next.js frontend
- No FastAPI, Flask, or Django backend
- No REST API router
- No background worker queue
- No scheduler or cron job
- No Dockerfile or docker-compose.yml
- No package.json / npm scripts
- No Makefile / Procfile
- No CI/CD startup logic in-repo
- No .env loading in code, even though `python-dotenv` is listed in `requirements.txt`

### 1.2 Real runtime topology

User in browser
-> Streamlit UI (`streamlit_app.py`)
-> LangGraph app (`agents.py`)
-> Tool execution (`tools.py`)
-> One or more of:
   - Local RAG retrieval (`retrieval.py` -> Chroma in `data/chroma_db/`)
   - Live DuckDuckGo search
   - RSS feed aggregation
-> Ollama LLM (`llama3.2`) for reasoning, analysis, and writing
-> Ollama embeddings (`nomic-embed-text`) for ingestion and retrieval
-> Newsletter HTML response
-> Streamlit review UI
-> Optional archive write to `data/archive_memory/`

### 1.3 Startup entry points

Primary application entry point:

- `python -m streamlit run src/streamlit_app.py`

Secondary runnable modules:

- `python src/ingestion.py` to build the main vector store from PDFs
- `python src/retrieval.py` to test retrieval against the existing vector store
- `python src/tools.py` to test tool binding with Ollama
- `python src/memory_store.py` to test archive memory save/retrieve behavior

## 2. File-Level Execution Flow

### 2.1 Main Streamlit runtime

`src/streamlit_app.py` starts first when running the UI.

It performs these roles:

1. Builds the Streamlit page and sidebar.
2. Detects uploaded PDFs in `data/raw_pdfs/`.
3. Optionally triggers `ingest_documents()` if the main vector DB is missing.
4. Creates a session-scoped thread ID for LangGraph state continuity.
5. On user action, checks long-term archive memory through `MemoryStore.check_memory()`.
6. Streams the graph in `orchestrator.app`.
7. Displays research results, chart JSON, and generated HTML draft.
8. On approval, archives the final draft through `MemoryStore.save_memory()`.

### 2.2 Agent pipeline trigger chain

Triggered from Streamlit button click or CLI execution:

1. `orchestrator.app.stream(...)`
2. `Researcher` node
3. `Analyst` node
4. `Writer` node
5. Optional human review loop
6. Optional archive save

### 2.3 Researcher node behavior

`src/agents.py` binds three tools from `src/tools.py`:

- `lookup_policy_docs`
- `web_search_stub`
- `rss_feed_search`

The researcher asks Ollama which tools to call, then executes the tool calls in Python.

### 2.4 RAG flow

RAG path for internal PDFs:

1. `src/ingestion.py`
2. `PyPDFDirectoryLoader` loads PDFs from `data/raw_pdfs/`
3. `RecursiveCharacterTextSplitter` chunks the content
4. `OllamaEmbeddings(model="nomic-embed-text")` creates embeddings
5. `Chroma(... persist_directory=data/chroma_db)` stores vectors locally

Retrieval path during runtime:

1. `lookup_policy_docs()` in `src/tools.py`
2. `retrieve_documents()` in `src/retrieval.py`
3. Chroma similarity search against `data/chroma_db/`
4. Results returned as source-grounded snippets and file links

### 2.5 Archive memory flow

Archive path:

1. `MemoryStore.check_memory(query)` runs before research
2. If a close topic exists, the app surfaces a duplicate warning
3. After approval, `MemoryStore.save_memory(topic, content)` writes the final HTML into `data/archive_memory/`

### 2.6 Embedded services versus external services

Embedded/local services inside the Python process:

- Streamlit UI logic
- LangGraph graph execution
- Chroma persistence layer used as an embedded library

External services required at runtime:

- Ollama daemon/server
- Ollama model `llama3.2`
- Ollama embedding model `nomic-embed-text`
- Internet access for DuckDuckGo and RSS feeds

## 3. Environment Setup Guide

### 3.1 Verified environment in this workspace

- Python environment type: `venv`
- Verified Python version in current workspace: `3.13.1`

Important compatibility note:

- The workspace currently has Python 3.13 working.
- For recreating on another machine, Python 3.11 or 3.12 is the safer recommendation because some AI packages tend to lag behind newest Python releases.

### 3.2 Node.js requirement

Node.js is not required.

There is no Node frontend, npm usage, yarn usage, pnpm usage, or JavaScript build step in the current project.

### 3.3 Python dependency manager

The project uses `pip` with `requirements.txt`.

There is no `poetry.lock`, `pyproject.toml`, `Pipfile`, or Conda environment file in the repo root.

### 3.4 GPU / CUDA requirement

CUDA is optional, not mandatory.

- Chroma and the current Python app can run on CPU.
- Ollama can run on CPU, though slower.
- If Ollama is configured to use GPU, performance improves but the project code does not directly require CUDA.

### 3.5 Required non-Python dependency: Ollama

The code uses:

- `ChatOllama(model="llama3.2")`
- `OllamaEmbeddings(model="nomic-embed-text")`

You must install Ollama and pull both models.

Windows:

```powershell
winget install Ollama.Ollama
ollama pull llama3.2
ollama pull nomic-embed-text
```

macOS:

```bash
brew install ollama
ollama pull llama3.2
ollama pull nomic-embed-text
```

Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
ollama pull nomic-embed-text
```

Start the Ollama service if it is not already running:

```bash
ollama serve
```

### 3.6 Environment variables

Current code status:

- No `.env` file is required by the existing Python code path.
- `python-dotenv` is installed but not used.
- No OpenAI key is required.
- No HuggingFace token is required for the current default flow.

Optional environment variables you may still choose to set for runtime control:

- `OLLAMA_HOST` if your Ollama server is not local default
- `STREAMLIT_SERVER_PORT` if you want to externalize Streamlit config

These variables are not currently loaded by project code automatically.

### 3.7 Database setup

There is no SQL/NoSQL application database.

Data persistence is file-based:

- Main vector DB: `data/chroma_db/`
- Archive vector DB: `data/archive_memory/`
- Source documents: `data/raw_pdfs/`

### 3.8 Vector DB setup

The project uses Chroma in embedded mode.

There is no separate Chroma server to start.

Setup is done implicitly by running ingestion:

```bash
python src/ingestion.py
```

or by launching Streamlit and pressing `Build/Update Vector Index`.

### 3.9 Streamlit setup

Nothing beyond Python package installation is required.

Run:

```bash
python -m streamlit run src/streamlit_app.py
```

Default port:

- `8501`

### 3.10 FAISS setup

FAISS is not used in this repository.

You do not need to install or run FAISS unless you intentionally refactor the retrieval layer away from Chroma.

### 3.11 LangChain / LangGraph setup

Installed through `requirements.txt`.

No extra service startup is needed.

## 4. venv and Dependency Management

### 4.1 Create the virtual environment

Windows CMD:

```cmd
python -m venv .venv
```

PowerShell:

```powershell
python -m venv .venv
```

Linux/macOS:

```bash
python3 -m venv .venv
```

### 4.2 Activate the virtual environment

Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4.3 Deactivate the virtual environment

All platforms:

```bash
deactivate
```

### 4.4 Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4.5 Reinstall dependencies from scratch

Windows CMD:

```cmd
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Linux/macOS:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4.6 Upgrade dependencies

Upgrade installed packages in-place:

```bash
python -m pip install --upgrade -r requirements.txt
```

Upgrade a specific package:

```bash
python -m pip install --upgrade streamlit langchain langgraph chromadb
```

### 4.7 Freeze current environment

```bash
python -m pip freeze > requirements.lock.txt
```

### 4.8 Recreate environment from the freeze file

```bash
python -m pip install -r requirements.lock.txt
```

## 5. Runnable Modules

| Module | File | Purpose | Run Command | Port | Dependencies | Triggered Services |
|---|---|---|---|---|---|---|
| Streamlit App | `src/streamlit_app.py` | Main user-facing UI and orchestrator | `python -m streamlit run src/streamlit_app.py` | 8501 | Streamlit, Ollama, LangGraph, Chroma, optional PDFs, internet | Research graph, retrieval, archive memory, PDF export |
| Ingestion Pipeline | `src/ingestion.py` | Build/update vector index from PDFs | `python src/ingestion.py` | N/A | PDFs in `data/raw_pdfs/`, Ollama embedding model, Chroma | Creates `data/chroma_db/` |
| Retrieval Smoke Test | `src/retrieval.py` | Test semantic retrieval against the vector DB | `python src/retrieval.py` | N/A | Existing `data/chroma_db/`, Ollama embedding model | Chroma similarity search |
| Orchestration Center | `src/orchestrator.py` | Unified workflow with approval routing and checkpointed state | Integrated via Streamlit runtime | N/A | Ollama, internet, optional Chroma DB | Research graph with approval loop |
| Tools Smoke Test | `src/tools.py` | Validate model tool binding | `python src/tools.py` | N/A | Ollama | Tool planning via LLM |
| Archive Memory Test | `src/memory_store.py` | Validate archive memory persistence | `python src/memory_store.py` | N/A | Ollama embedding model, Chroma | Archive save and similarity lookup |
| Single-Command Launcher | `run_all.py` | Prerequisite check plus Streamlit startup | `python run_all.py` | 8501 by default | Python env, Ollama CLI, models, Streamlit | Streamlit app launch |

## 6. Individual Execution Guide

### 6.1 `src/streamlit_app.py`

What it does:

- Starts the web UI
- Uploads PDFs
- Builds vector index
- Runs the research graph
- Shows chart data and HTML output
- Saves approved newsletters into archive memory

When to run:

- Normal usage
- Demo usage
- End-to-end validation of the whole system

What it triggers:

- `ingest_documents()` if the DB is missing and PDFs exist
- `MemoryStore.check_memory()` before research
- `agents.app.stream()` during research
- `MemoryStore.save_memory()` after approval

Does it need anything already running:

- Yes, Ollama should already be installed and reachable
- PDFs are optional
- Internet is required for web and RSS tools

Required environment variables:

- None in current code

Expected output:

- Browser UI on `http://localhost:8501`
- Research results, chart data, rendered newsletter HTML, downloadable HTML/PDF

Run command:

```bash
python -m streamlit run src/streamlit_app.py
```

Common runtime errors:

- Ollama not running
- Missing Ollama models
- Empty or corrupt `data/chroma_db/`
- No PDFs present for RAG mode
- Network failures from DuckDuckGo or RSS feeds

### 6.2 `src/ingestion.py`

What it does:

- Loads PDFs from `data/raw_pdfs/`
- Splits text into chunks
- Embeds them with `nomic-embed-text`
- Persists them to `data/chroma_db/`

When to run:

- First-time indexing
- After adding or replacing PDFs
- When rebuilding a broken vector DB

Expected output:

- Console logs with page count, chunk count, and batch progress
- Populated `data/chroma_db/`

Run command:

```bash
python src/ingestion.py
```

Common runtime errors:

- `No PDFs found`
- Ollama embedding model missing
- Locked/corrupted Chroma persistence files

### 6.3 `src/retrieval.py`

What it does:

- Connects to the main Chroma DB
- Embeds the query
- Runs similarity search with light keyword boosting

When to run:

- Retrieval debugging
- Validating the main vector DB after ingestion

Run command:

```bash
python src/retrieval.py
```

Expected output:

- Top-k matched snippets with source metadata and scores

### 6.4 `src/agents.py`

What it does:

- Defines shared state and the researcher, analyst, and writer node logic
- Provides reusable node behavior for the orchestration center

When to run:

- Imported by `src/orchestrator.py`

### 6.5 `src/orchestrator.py`

What it does:

- Central orchestration for researcher -> analyst -> writer
- Adds human-approval node and conditional routing
- Compiles graph with checkpointing and interrupt-before-approval behavior

When to run:

- Imported by Streamlit runtime
- Workflow-level debugging

### 6.6 `src/tools.py`

What it does:

- Tests Ollama model binding with tool definitions

When to run:

- Model/tool integration debugging

Run command:

```bash
python src/tools.py
```

### 6.7 `src/memory_store.py`

What it does:

- Saves and retrieves archive memory embeddings

When to run:

- Archive store debugging
- Duplicate detection validation

Run command:

```bash
python src/memory_store.py
```

## 7. Full System Startup Order

### 7.1 Correct startup order

Step 1: Install Ollama and pull models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Why first:

- The app cannot reason or embed without these models.

Step 2: Create and activate the Python virtual environment

Why second:

- Every Python command in this project depends on the installed packages.

Step 3: Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

Why third:

- Streamlit, LangChain, Chroma, and PDF tooling all come from pip.

Step 4: Start or verify Ollama service availability

```bash
ollama serve
```

Why fourth:

- Both generation and embeddings call Ollama at runtime.

Step 5: Optionally build the vector index

```bash
python src/ingestion.py
```

Why fifth:

- Without the vector DB, RAG lookups fail or return nothing.
- The app can still run in web-only mode, but internal PDF search will be unavailable.

Step 6: Start Streamlit

```bash
python -m streamlit run src/streamlit_app.py
```

Step 7: Open browser and use the UI

```text
http://localhost:8501
```

### 7.2 Why the order matters

- If Ollama is missing, all agent nodes that use the LLM fail.
- If `nomic-embed-text` is missing, ingestion and retrieval fail.
- If the Chroma DB is empty, PDF retrieval returns nothing.
- If the archive DB path is unavailable, duplicate memory check and archive save fail.

### 7.3 Race conditions and startup caveats

- Running ingestion while the app is actively using the same Chroma store can create lock/contention issues.
- The first model invocation may be slower because Ollama may need to warm up the model.
- If internet is unavailable, web search and RSS results will be empty or error out, but local RAG can still work.

## 8. Single-Command Execution Solution

### 8.1 What exists now

This repo did not include a single-command launcher.

### 8.2 Added solution

The following launchers are now provided:

- `run_all.py`
- `run_all.bat`
- `run_all.ps1`
- `start.sh`

These launchers:

1. Verify Python entry path and Streamlit script path.
2. Verify the `ollama` CLI is installed.
3. Verify Ollama is reachable.
4. Verify required models exist.
5. Launch the Streamlit app.

### 8.3 Single-command usage

Windows CMD:

```cmd
run_all.bat
```

PowerShell:

```powershell
.\run_all.ps1
```

Cross-platform Python:

```bash
python run_all.py
```

Linux/macOS:

```bash
chmod +x start.sh
./start.sh
```

### 8.4 Check-only mode

```bash
python run_all.py --check-only
```

This verifies prerequisites without starting Streamlit.

## 9. Frontend, Backend, and AI Flow Validation

### 9.1 Actual flow in this repository

Current runtime flow:

User action in Streamlit
-> Streamlit widget callback
-> Direct in-process Python function call
-> LangGraph nodes in `src/agents.py`
-> Tool functions in `src/tools.py`
-> Local retrieval and external searches
-> Ollama LLM response
-> Streamlit state update and render

### 9.2 Important architectural clarification

There is no separate HTTP frontend-to-backend API call.

That means:

- No API base URL to configure
- No CORS layer in the current design
- No proxy setup
- No token-based auth flow
- No frontend/backend port mismatch beyond the Streamlit server itself

### 9.3 Interaction map

UI path:

- Topic input -> `st.button("Start Agents")`
- `MemoryStore.check_memory()` runs
- `agent_app.stream(...)` runs
- Research findings rendered
- Chart JSON optionally rendered through Plotly
- HTML draft rendered in Streamlit
- Approval saves archive memory

### 9.4 Broken route / mismatch findings

Current validated findings:

- No broken HTTP routes were found because there is no HTTP API layer in the repo.
- A real runtime defect existed in hardcoded absolute data paths; this has been corrected to use project-relative paths.
- `.env` support is not wired even though `python-dotenv` is installed.
- The project is tightly coupled to local Ollama availability.

## 10. Common Errors and Fixes

### 10.1 `ModuleNotFoundError` or `ImportError`

Root cause:

- venv not activated
- dependencies not installed
- running from the wrong working directory

Diagnosis:

```bash
python -m pip list
python -c "import streamlit, langchain, chromadb"
```

Fix:

```bash
python -m pip install -r requirements.txt
```

Prevention:

- Always activate `.venv` before running project commands.

### 10.2 Streamlit startup failure

Root cause:

- `streamlit` not installed in active interpreter
- wrong interpreter selected

Diagnosis:

```bash
python -m streamlit --version
```

Fix:

```bash
python -m pip install streamlit
```

### 10.3 Ollama model not found

Root cause:

- `llama3.2` or `nomic-embed-text` was not pulled locally

Diagnosis:

```bash
ollama list
```

Fix:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 10.4 Ollama connection error

Root cause:

- Ollama server not running

Diagnosis:

```bash
ollama list
```

Fix:

```bash
ollama serve
```

### 10.5 Chroma / vector DB not found

Root cause:

- Ingestion never ran
- vector DB directory deleted

Diagnosis:

```bash
python src/ingestion.py
```

Fix:

- Rebuild the index by running ingestion again.

### 10.6 PDF ingestion failure

Root cause:

- corrupt PDF
- empty `data/raw_pdfs/`
- embedding model unavailable

Diagnosis:

```bash
python src/ingestion.py
```

Fix:

- Remove bad PDFs, ensure models are present, rerun ingestion.

### 10.7 Port conflict on 8501

Root cause:

- Another Streamlit app already using the default port

Fix:

```bash
python -m streamlit run src/streamlit_app.py --server.port 8502
```

### 10.8 Dependency conflicts

Root cause:

- mixed global and local package installs
- stale venv

Fix:

- Recreate `.venv` from scratch using the commands in Section 4.5.

### 10.9 CUDA issues

Root cause:

- optional GPU runtime mismatch in Ollama or Torch stack

Fix:

- Run on CPU first to verify app correctness.
- Upgrade GPU drivers and Ollama separately if GPU acceleration is required.

### 10.10 HuggingFace download issues

Status in this repo:

- Current default runtime path does not require HuggingFace model downloads.
- `sentence-transformers` is installed but not the active embedding path in code.

### 10.11 CORS issues

Status in this repo:

- Not applicable in current architecture because the UI and orchestration run in the same Streamlit server process.

### 10.12 Frontend blank page

Root cause:

- Streamlit process failed before page render
- exceptions during startup

Diagnosis:

```bash
python -m streamlit run src/streamlit_app.py
```

Read the terminal output for the stack trace.

### 10.13 API timeout

Status in this repo:

- No HTTP API layer exists.
- The equivalent failure mode is long Ollama response time or external search latency.

## 11. Development vs Production

### 11.1 Development mode

Use:

```bash
python -m streamlit run src/streamlit_app.py --server.runOnSave true --server.headless false
```

Use this when:

- developing UI behavior
- iterating on prompts and tools
- testing ingestion locally

### 11.2 Production-like local mode

Use:

```bash
python -m streamlit run src/streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
```

Important limitation:

- This is only a local deployment shape, not a hardened production architecture.

### 11.3 Production gaps

Current blockers for serious production deployment:

- No Docker packaging
- No reverse proxy configuration
- No authentication
- No structured settings management
- No remote vector store
- No remote LLM provider fallback
- No centralized logging
- No automated health checks
- No API service boundary

## 12. Deployment Readiness Review

### 12.1 Docker support

- Not present
- Not deployment ready as-is

### 12.2 HuggingFace Spaces readiness

- Not suitable as-is because the app depends on a local Ollama runtime and local persistent directories

### 12.3 Streamlit Cloud readiness

- Not suitable as-is for the same reason: local Ollama dependency and filesystem persistence assumptions

### 12.4 Railway / Render readiness

- Not ready as-is
- Would require replacing local Ollama with a network-accessible model service and reworking persistence

### 12.5 Gunicorn / Uvicorn readiness

- Not applicable because the repo does not expose an ASGI or WSGI app

### 12.6 Static build readiness

- Not applicable because there is no JavaScript frontend build pipeline

## 13. Recommended Improvements

1. Add a `settings.py` or environment config module and wire `.env` loading explicitly.
2. Split orchestration from Streamlit so the AI runtime can be exposed through a proper API service later.
3. Add a real health-check command for Ollama, Chroma readiness, and model availability.
4. Add a Docker-based local dev environment if the project needs easier onboarding.
5. Add pinned dependency versions for reproducible builds.
6. Add tests for ingestion, retrieval, and tool orchestration.
7. Add a safe fallback path when web search or RSS feeds are unavailable.
8. Replace ad-hoc absolute links and persistence assumptions with configurable runtime settings.

## 14. Quick Start

### 14.1 Fastest path to run the whole system

1. Create and activate `.venv`
2. Install `requirements.txt`
3. Install Ollama
4. Pull `llama3.2` and `nomic-embed-text`
5. Put PDFs into `data/raw_pdfs/` if you want RAG
6. Run `python run_all.py`
7. Open `http://localhost:8501`

### 14.2 Minimal commands

```bash
python -m venv .venv
source-or-activate-the-venv
python -m pip install -r requirements.txt
ollama pull llama3.2
ollama pull nomic-embed-text
python run_all.py
```