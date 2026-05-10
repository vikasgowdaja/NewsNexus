# Day 1 - Intro to GenAI & Setup (6 Hours)

## Skeleton 1 (Day 1)
Minimal runnable foundation before any model logic changes.

```text
NewsNexus/
├── requirements.txt
├── run_all.py
├── README.md
└── src/
		└── streamlit_app.py
```

## Stage-by-Stage Delivery
1. Stage A - GenAI architecture orientation
2. Stage B - Environment and dependency setup
3. Stage C - Model/runtime preflight checks
4. Stage D - First successful app launch

## Code Breakdown (What to Teach in Code)
- Launcher model contract: [run_all.py](run_all.py#L10)
- Runtime validation function: [run_all.py](run_all.py#L17)
- Command construction for Streamlit startup: [run_all.py](run_all.py#L50)
- App UI bootstrap point: [src/streamlit_app.py](src/streamlit_app.py#L21)
- Dependency list and package intent: [requirements.txt](requirements.txt)

## Why This Day Matters
- Students must understand system dependencies before discussing prompts, RAG, or agents.
- Most early failures in GenAI projects are setup/runtime failures, not model failures.

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1 (Concept framing):
	- Explain components: UI, tools, LLM, embeddings, vector DB, memory.
	- Explain local-first design and privacy implications.
- Hour 2 (Environment lab):
	- Create venv, install requirements, verify interpreter path.
- Hour 3 (Model lab):
	- Pull `llama3.2` and `nomic-embed-text`.
	- Explain why generation and embedding models are separate.
- Hour 4 (Code walkthrough):
	- Read `run_all.py` start to finish.
	- Show how `check_ollama_available()` prevents runtime surprises.
- Hour 5 (Execution flow):
	- Launch using `python run_all.py`.
	- Trace terminal -> Streamlit -> browser lifecycle.
- Hour 6 (Debug clinic):
	- Simulate missing model and fix.
	- Simulate broken launcher and use `python -m streamlit` workaround.

## Hands-on Commands
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ollama pull llama3.2
ollama pull nomic-embed-text
python run_all.py --check-only
python -m streamlit run src/streamlit_app.py
```

## Assessment Checkpoint
- Student can explain each startup dependency and where it is validated in code.
- Student can recover from missing model/interpreter/runtime path issues.
