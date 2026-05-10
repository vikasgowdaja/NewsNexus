# Day 5 - RAG (Retrieval-Augmented Generation) (6 Hours)

## Skeleton 5 (Day 5)
Mini-RAG skeleton connected to agent tooling.

```text
User Query
 -> Researcher Node
 -> lookup_policy_docs Tool
 -> retrieve_documents
 -> Chroma top-k chunks
 -> LLM grounded synthesis
```

## Stage-by-Stage Delivery
1. Stage A - RAG motivation and trust model
2. Stage B - Retrieval tool implementation
3. Stage C - Evidence formatting and citation path
4. Stage D - Compare grounded vs ungrounded outputs

## Code Breakdown
- RAG tool contract: [src/tools.py](src/tools.py#L9)
- Retrieval invocation inside tool: [src/tools.py](src/tools.py#L17)
- Source link formatting: [src/tools.py](src/tools.py#L24)
- Tool execution loop from agent: [src/agents.py](src/agents.py#L50)

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: Hallucination discussion with business examples.
- Hour 2: Walk through `lookup_policy_docs` end-to-end.
- Hour 3: Trace retrieved chunk and metadata into response.
- Hour 4: Run same prompt with/without RAG and compare.
- Hour 5: Analyze edge cases (no documents, weak matches).
- Hour 6: Build groundedness rubric for student grading.

## Assessment Checkpoint
- Student can draw full RAG execution path and explain why each step exists.

