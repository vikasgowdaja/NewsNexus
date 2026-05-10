# Day 3 - Working with Open Models (6 Hours)

## Skeleton 3 (Day 3)
Model wiring layer: generation model + embedding model + tool binding.

```text
src/
├── tools.py      # ChatOllama + tool binding
├── ingestion.py  # embedding while indexing
└── retrieval.py  # embedding while querying
```

## Stage-by-Stage Delivery
1. Stage A - Open model runtime concepts
2. Stage B - Chat model integration
3. Stage C - Embedding model integration
4. Stage D - Failure handling and model verification

## Code Breakdown
- Chat model setup: [src/tools.py](src/tools.py#L121)
- Tool binding to model: [src/tools.py](src/tools.py#L123)
- Embedding in indexing path: [src/ingestion.py](src/ingestion.py#L30)
- Embedding in retrieval path: [src/retrieval.py](src/retrieval.py#L20)
- Required models baseline: [run_all.py](run_all.py#L10)

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: Generation vs embedding model responsibilities.
- Hour 2: Model pull, model list, model selection strategy.
- Hour 3: Trace chat model invocation in tools and agents.
- Hour 4: Trace embedding usage in indexing and retrieval.
- Hour 5: Local performance constraints and batching rationale.
- Hour 6: Runtime failure recovery (404 model not found, daemon down).

## Assessment Checkpoint
- Student can map each model to exact code paths and runtime purpose.

