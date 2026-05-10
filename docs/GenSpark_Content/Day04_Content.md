# Day 4 Content - Embeddings & Semantic Search

## Learning Objectives
- Understand keyword vs semantic search
- Design chunking strategy for efficient embedding
- Implement hybrid search (semantic + keyword boost)
- Measure retrieval quality

## Skeleton 4 (Day 4 - Retrieval Layer)
```
src/
├── ingestion.py  # Chunking + embedding
└── retrieval.py  # Semantic search + keyword boost
```

## The 4 Stages of Day 4
1. **Stage A:** Keyword search limitations vs semantic capabilities
2. **Stage B:** Chunking strategy and tradeoffs
3. **Stage C:** Embedding and vector storage
4. **Stage D:** Hybrid search with keyword boosting

## Chunking Strategy (EXACT CODE from src/ingestion.py:20)
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)
chunks = text_splitter.split_documents(raw_documents)
```
- **Why chunk_size=500?** Trade-off: enough context (~100 words) vs efficient embedding
- **Why overlap=50?** Preserve context at chunk boundaries
- **Without chunks:** Embed entire 100-page PDF = expensive, slow
- **With chunks:** Embed small sections = fast, granular retrieval

## Why Chunking Matters
- Chunk too small (< 100 chars) = broken context
- Chunk too large (> 2000 chars) = expensive embeddings
- 500 chars + 50 overlap = NewsNexus sweet spot

## Semantic Retrieval (EXACT CODE from src/retrieval.py:31)
```python
results = vector_store.similarity_search_with_score(query, k=k+2)
```
- Score is distance in vector space (lower = more similar)
- Fetch k+2 for hybrid search filtering

## Hybrid Search with Keyword Boost (EXACT CODE from src/retrieval.py:37)
```python
for doc, score in results:
    content = doc.page_content.lower()
    term_matches = sum(1 for term in query_terms if term in content)
    boosted_score = score - (term_matches * 0.05)  # Boost exact matches
```
- **Example:** Query "climate policy" + exact keyword match in doc = lower score = ranked higher
- **Algorithm:** For each doc, count matching terms, apply artificial boost

## Embedding Process
- **Input:** One chunk of text
- **Process:** nomic-embed-text model processes text → outputs 768-dimensional vector
- **Output:** Vector stored in ChromaDB with metadata (source, page number)

## Vector Space Visualization
- Each embedding is a point in 768-dimensional space (visualize as 2D for humans)
- Semantically similar documents cluster near each other
- "climate change" and "global warming" are close in vector space

## Performance Optimization
- Batch embeddings: Embed 100 chunks at once vs 1 at a time
- Use GPU if available: Ollama can offload to GPU
- Cache embeddings: Don't re-embed on every query

## Why This Day Matters
- Semantic search finds relevant docs before LLM
- Better retrieval = better grounded responses from LLM
- Vector similarity is the foundation of RAG (Day 5)

## 6-Hour Teaching Script

**Hour 1: Search Comparison (60 min)**
- Keyword search (old): "Find documents with word 'climate'" = brittle
- Semantic search (modern): "Find documents ABOUT climate change" = flexible
- Draw: Keyword vs semantic space
- Examples: Synonyms that keyword search misses

**Hour 2: Chunking Strategy (60 min)**
- Why chunk? Efficiency + granularity
- Show: RecursiveCharacterTextSplitter parameters
- Discuss: chunk_size vs overlap tradeoffs
- Hands-on: Chunk a sample document, observe boundaries

**Hour 3: Embedding Fundamentals (60 min)**
- Input text → 768-dimensional vector
- Vectors represent semantic meaning
- Similar meanings = nearby vectors
- Cosine similarity metric

**Hour 4: Hands-on: Index Documents (60 min)**
- Load PDF
- Chunk it
- Embed chunks
- Store in ChromaDB
- Observe: data/chroma_db directory created

**Hour 5: Hands-on: Retrieve Documents (60 min)**
- Query: "What is the climate policy?"
- Embed query
- Find nearest vectors
- Return top 3 docs
- Inspect: Similarity scores

**Hour 6: Debug & Optimization (60 min)**
- Why is wrong document ranked #1? Check boosting logic
- Measure: P@3 (precision at 3), Recall
- Optimize: Adjust chunk_size, try different queries
- Batch embeddings: Measure latency improvement

## Assessment Checkpoint
By end of Day 4, students should:
- ✓ Explain tradeoffs in chunking strategy
- ✓ Understand vector similarity
- ✓ Implement hybrid search with keyword boost
- ✓ Measure retrieval precision/recall
