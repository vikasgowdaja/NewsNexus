# Day 4 - Embeddings & Semantic Search (6 Hours)

## Skeleton 4 (Day 4)
Data indexing and retrieval skeleton.

```text
data/
├── raw_pdfs/
└── chroma_db/

src/
├── ingestion.py
├── retrieval.py
└── memory_store.py
```

## Stage-by-Stage Delivery
1. Stage A - Text to vectors (embedding intuition)
2. Stage B - Chunking strategy and tradeoffs
3. Stage C - Semantic retrieval execution
4. Stage D - Ranking optimization (keyword boost)

## Code Breakdown
- Chunking config: [src/ingestion.py](src/ingestion.py#L20)
- Vector DB persistence: [src/ingestion.py](src/ingestion.py#L37)
- Similarity search API call: [src/retrieval.py](src/retrieval.py#L31)
- Hybrid keyword filter toggle: [src/retrieval.py](src/retrieval.py#L12), [src/retrieval.py](src/retrieval.py#L37)
- Boost formula line: [src/retrieval.py](src/retrieval.py#L46)
- Memory similarity pattern reuse: [src/memory_store.py](src/memory_store.py#L43)

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: Embedding vectors and semantic distance.
- Hour 2: Chunk size/overlap tuning workshop.
- Hour 3: Build index from PDFs and inspect DB folder.
- Hour 4: Retrieval query walkthrough and scoring.
- Hour 5: Turn keyword_filter on/off and compare relevance.
- Hour 6: Retrieval diagnostics and false-positive analysis.

## Assessment Checkpoint
- Student can explain how chunking and scoring affect final answer quality.

