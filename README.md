# 📰 NewsNexus: Autonomous Corporate Intelligence Agent
### Capstone Project | Student Development Program (SDP)

NewsNexus is a local, privacy-first Agentic AI system that:
- reads internal PDFs,
- searches live web + RSS sources,
- analyzes findings,
- drafts professional HTML newsletters,
- keeps a human in the loop for approval.

---

## 🏗️ Architecture Overview

Built in 5 phases from basic RAG to full multi-agent workflow.

### CPU-friendly tech stack
- LLM engine: Ollama (`llama3.2`)
- Orchestration: LangGraph
- Vector store: ChromaDB (local persistent)
- Embeddings: Ollama (`nomic-embed-text`)
- Language: Python 3.10+
- UI: Streamlit

---

## 🚀 Quick Setup (Simple)

### 1. Prerequisites
- Python installed
- Ollama installed and running

### 2. Environment setup

```bash
# from project root
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Pull required models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 4. Run app

```bash
python -m streamlit run src/streamlit_app.py
```

Open: http://localhost:8501

---

## 📚 Phase-by-Phase Guide

### 🔹 Phase 1: Knowledge Base (RAG)

Goal: Build internal memory from PDFs.

- [src/ingestion.py](src/ingestion.py): PDF -> chunks -> embeddings -> [data/chroma_db](data/chroma_db)
- [src/retrieval.py](src/retrieval.py): semantic retrieval

Run:

```bash
python src/ingestion.py
```

> Put PDFs inside [data/raw_pdfs](data/raw_pdfs) first.

### 🔹 Phase 2: Tool Definition (Function Calling)

Goal: Give LLM callable tools.

Tools in [src/tools.py](src/tools.py):
1. `lookup_policy_docs` (RAG search)
2. `web_search_stub` (DuckDuckGo live search)
3. `rss_feed_search` (industry feed lookup)

Run:

```bash
python src/tools.py
```

### 🔹 Phase 3: Multi-Agent Orchestration

Goal: Build a team of specialized agents with LangGraph.

Team flow:
Researcher -> Analyst -> Writer

Key file: [src/agents.py](src/agents.py)

Run:

```bash
python src/agents.py
```

### 🔹 Phase 4: Human-in-the-Loop (HITL)

Goal: Pause before final publish and allow revision.

Key file: [src/phase4_human_loop.py](src/phase4_human_loop.py)

Run:

```bash
python src/phase4_human_loop.py
```

### 🔹 Phase 5: Memory & Persistence (Final)

Goal: Avoid repeating recently covered topics.

- [src/memory_store.py](src/memory_store.py): archive save/retrieve
- [src/phase5_final.py](src/phase5_final.py): full CLI flow

Run:

```bash
python src/phase5_final.py
```

---

## 🖥️ Recommended Runtime Modes

### Main UI mode (best for demos)

```bash
python -m streamlit run src/streamlit_app.py
```

### One-command launcher

```bash
python run_all.py
```

---

## 📂 Project Structure

```text
NewsNexus/
├── data/
│   ├── raw_pdfs/
│   ├── chroma_db/
│   └── archive_memory/
├── src/
│   ├── agents.py
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── tools.py
│   ├── memory_store.py
│   ├── phase4_human_loop.py
│   ├── phase5_final.py
│   └── streamlit_app.py
├── run_all.py
├── requirements.txt
└── README.md
```

---

## ⚠️ Troubleshooting

### 1) Model/tool issues
- Cause: wrong model or model not pulled
- Fix:

```bash
ollama list
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 2) App fails to start with `streamlit run ...`
- Cause: broken launcher path in moved venv
- Fix (safe command):

```bash
python -m streamlit run src/streamlit_app.py
```

### 3) No document-based answers
- Cause: no PDFs indexed
- Fix:

```bash
python src/ingestion.py
```

### 4) Chroma errors
- Cause: lock/corruption mismatch
- Fix: delete [data/chroma_db](data/chroma_db) and rerun ingestion.

---

## 🎓 Learning Outcome

This project demonstrates progression from:
- basic RAG,
- to tool use,
- to multi-agent orchestration,
- to human-in-the-loop,
- to long-term memory and persistence.

A complete practical blueprint for modern local Agentic AI systems.