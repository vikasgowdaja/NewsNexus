# Day 8 - Optimization & Evaluation (6 Hours)

## Skeleton 8 (Day 8)
Quality-control and reliability skeleton.

```text
Input Guardrail
 -> Tool Reliability Fallback
 -> Output Quality Constraints
 -> Evaluation Rubric
```

## Stage-by-Stage Delivery
1. Stage A - Define quality metrics
2. Stage B - Add lightweight guardrails
3. Stage C - Add reliability fallbacks
4. Stage D - Evaluate before/after improvements

## Code Breakdown
- Typo/intent normalization guardrail: [src/streamlit_app.py](src/streamlit_app.py#L221)
- DuckDuckGo backend fallback sequence: [src/tools.py](src/tools.py#L51)
- RSS fallback when web search unavailable: [src/tools.py](src/tools.py#L74)
- Outage-not-evidence safety message: [src/tools.py](src/tools.py#L78)
- Structured output extraction for charting: [src/agents.py](src/agents.py#L141)
- Retrieval tuning knob: [src/retrieval.py](src/retrieval.py#L46)

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: Build an evaluation rubric (factuality/relevance/structure).
- Hour 2: Prompt and output schema tuning.
- Hour 3: Retrieval parameter tuning and tradeoff discussion.
- Hour 4: Reliability engineering for external tool failures.
- Hour 5: Comparative runs with documented scores.
- Hour 6: Produce optimization report and next-step backlog.

## Assessment Checkpoint
- Student can distinguish model failure vs tool outage and handle both safely.

