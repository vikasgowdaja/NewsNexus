# Day 1 Content - Intro to GenAI & Setup

## Learning Objectives
- Understand why setup happens before model logic
- Know the 4 stages of environment bootstrap
- Verify Ollama models are installed

## Stack Overview
- **Runtime:** Python 3.10+
- **Language Model:** Ollama llama3.2 (2.0GB)
- **Embedding Model:** Ollama nomic-embed-text (274MB)
- **Vector DB:** ChromaDB
- **Framework:** LangChain + LangGraph
- **UI:** Streamlit
- **Philosophy:** Local-first = privacy-first

## The 4 Stages of Day 1
1. **Stage A:** GenAI architecture orientation
2. **Stage B:** Environment and dependency setup (venv + pip install)
3. **Stage C:** Model/runtime preflight checks (ollama list)
4. **Stage D:** First successful app launch

## Skeleton 1 (Day 1 - Minimal Runnable)
```
NewsNexus/
├── requirements.txt
├── run_all.py
├── README.md
└── src/
    └── streamlit_app.py
```

## Critical Code Blocks

### Block 1: Model Contract (run_all.py:10)
```python
REQUIRED_MODELS = ("llama3.2", "nomic-embed-text")
```
- Why: Prevents starting app without required models
- Separation: Generation model separate from embedding model

### Block 2: Preflight Check (run_all.py:17)
```python
def check_ollama_available() -> tuple[bool, str]:
    if shutil.which("ollama") is None:
        return False, "Ollama CLI was not found on PATH. Install Ollama before starting NewsNexus."

    probe = run_command(["ollama", "list"])
    if probe.returncode != 0:
        stderr = probe.stderr.strip() or probe.stdout.strip() or "Unable to reach Ollama."
        return False, f"Ollama is installed but not reachable: {stderr}"

    installed_models = probe.stdout.lower()
    missing = [model for model in REQUIRED_MODELS if model.lower() not in installed_models]
    if missing:
        missing_list = ", ".join(missing)
        return False, f"Missing Ollama models: {missing_list}. Run `ollama pull` for each missing model."

    return True, "Ollama is reachable and required models are installed."
```
- Why: Prevents cryptic runtime errors later
- Teaching: "Fail early, fail explicitly"

### Block 3: App Bootstrap (src/streamlit_app.py:21)
```python
st.set_page_config(layout="wide", page_title="NewsNexus")
```
- Wide layout for side-by-side panels
- Entry point of user-facing UI

## Key Dependencies (from requirements.txt)
- langchain==1.2.10
- langchain-chroma==1.1.1
- langchain-ollama==0.1.1
- streamlit==1.57.0
- duckduckgo-search==6.1.4
- feedparser==6.0.10

## Why This Day Matters
- 80% of early GenAI project failures are setup/runtime, not model failures
- Students must understand system dependencies before discussing prompts, RAG, or agents
- Local-first design has privacy + cost implications worth understanding

## 6-Hour Teaching Script

**Hour 1: Concept Framing (60 min)**
- Draw architecture: UI → LLM → Embeddings → VectorDB → Memory
- Explain why each component exists
- Discuss privacy: local-first vs API-based

**Hour 2: Environment Lab (60 min)**
- Create virtual environment: `python -m venv .venv`
- Activate: `.venv\Scripts\activate` (Windows)
- Install: `pip install -r requirements.txt`
- Show: `pip list` to verify

**Hour 3: Model Lab (60 min)**
- Show `ollama pull llama3.2`
- Show `ollama pull nomic-embed-text`
- Show `ollama list` to confirm both installed
- Discuss model sizes: Why llama3.2 is 2GB, why nomic is 274MB

**Hour 4: Code Walkthrough (60 min)**
- Read run_all.py line by line
- Trace: check_ollama_available() logic
- Understand: REQUIRED_MODELS constant
- Ask: "What happens if llama3.2 is missing?"

**Hour 5: Execution Flow (60 min)**
- Run: `python run_all.py`
- Observe: Terminal output → Ollama loading → Streamlit server starting
- Open: http://localhost:8501 in browser
- Show: Streamlit UI comes up, ready for input

**Hour 6: Debug Clinic (60 min)**
- Simulate: Rename model file (break Ollama)
- See: Error from check_ollama_available()
- Fix: Restore model
- Show: `python -m streamlit` as safe fallback if launcher breaks

## Assessment Checkpoint
By end of Day 1, students should:
- ✓ Understand system components and why they exist
- ✓ Have working venv with all dependencies
- ✓ Have llama3.2 and nomic-embed-text installed
- ✓ Successfully launch Streamlit app
- ✓ Explain what happens during preflight check
