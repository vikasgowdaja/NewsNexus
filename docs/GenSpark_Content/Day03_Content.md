# Day 3 Content - Working with Open Models

## Learning Objectives
- Understand generation vs embedding model responsibilities
- Map each model to exact code paths
- Select appropriate models for local deployment
- Handle runtime failures gracefully

## Skeleton 3 (Day 3 - Model Wiring Layer)
```
src/
├── tools.py      # ChatOllama + tool binding
├── ingestion.py  # Embedding while indexing
└── retrieval.py  # Embedding while querying
```

## The 4 Stages of Day 3
1. **Stage A:** Open model runtime concepts
2. **Stage B:** Chat model integration
3. **Stage C:** Embedding model integration
4. **Stage D:** Failure handling and model verification

## Model Selection Strategy
- **llama3.2:** Good general-purpose model, ~2GB, ~4GB RAM to run
- **nomic-embed-text:** Lightweight embedder, ~274MB, ~1GB RAM to run
- **Constraint:** Local machine = model size + inference speed tradeoff

## Critical Code Blocks

### Block 1: Chat Model Setup (src/tools.py:121)
```python
def get_llm_with_tools():
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [lookup_policy_docs, web_search_stub, rss_feed_search]
    llm_with_tools = llm.bind_tools(tools)
    return llm, llm_with_tools, tools
```
- **Teaching Point:** temperature=0 = deterministic (good for production), not creative
- **Tool Binding:** bind_tools() tells model which functions it can call

### Block 2: Embedding Model in Indexing (src/ingestion.py:30)
```python
from langchain_ollama import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# Later in pipeline:
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="data/chroma_db"
)
```
- **Flow:** PDF → chunks → embed each chunk → store vectors in DB

### Block 3: Embedding Model in Retrieval (src/retrieval.py:20)
```python
# During search:
query_embedding = embedding_model.embed_query("user question")
similar_docs = vector_store.similarity_search_with_score(query, k=3)
```
- **Flow:** User query → embed query → find nearest vectors → return docs

## Model Verification Checklist
- ✓ ollama list (confirms models installed)
- ✓ First inference is slow (model loading into RAM)
- ✓ Subsequent calls are faster (cached in memory)

## Common Failures & Recovery
- ❌ "Model not found" → Run: `ollama pull llama3.2`
- ❌ "Connection refused" → Ollama daemon not running
- ❌ "Out of memory" → Need more RAM or smaller model
- ✅ Preflight check (Day 1) prevents these before app starts

## Why This Day Matters
- Open models = no API keys, no rate limits, full local control
- Embedding + generation together enable RAG (Day 5)
- Understanding model separation = better architecture

## 6-Hour Teaching Script

**Hour 1: Model Responsibilities (60 min)**
- Generation model: Takes text input → produces text output (answers)
- Embedding model: Takes text input → produces 768-dim vector (semantic meaning)
- Why separate? Different optimization objectives
- Draw flowchart: Query → embed → search → retrieve → generate → output

**Hour 2: Model Pull & Selection (60 min)**
- Show: `ollama pull llama3.2` (takes ~5 min)
- Show: `ollama pull nomic-embed-text` (takes ~2 min)
- Show: `ollama list` output
- Discuss: Model size tradeoffs, RAM requirements
- Compare: Other models available

**Hour 3: Chat Model Invocation (60 min)**
- Trace: get_llm_with_tools() function
- Show: ChatOllama(model="llama3.2", temperature=0)
- Explain: temperature parameter (0 = deterministic)
- Walk through: Tool binding process
- Ask: "What happens if you set temperature=1?"

**Hour 4: Embedding Usage in Indexing (60 min)**
- Show: OllamaEmbeddings initialization
- Trace: Embedding pipeline in ingestion.py
- Show: Chunk → embed → store in Chroma
- Discuss: Why batch embedding is faster
- Hands-on: Embed sample chunk manually

**Hour 5: Embedding Usage in Retrieval (60 min)**
- Trace: Query embedding in retrieval.py
- Show: Similarity search results
- Discuss: How vectors are compared (cosine similarity)
- Hands-on: Query and see retrieved docs
- Compare: Same query with different embedding

**Hour 6: Failure Recovery (60 min)**
- Simulate: Stop Ollama daemon
- See: "Connection refused" error
- Fix: Restart Ollama
- Simulate: Missing model
- See: Error message, run ollama pull
- Verify: Model now available

## Assessment Checkpoint
By end of Day 3, students should:
- ✓ Map each model to exact code paths and runtime purpose
- ✓ Explain generation vs embedding responsibilities
- ✓ Know model size vs RAM tradeoffs
- ✓ Troubleshoot common model failures
