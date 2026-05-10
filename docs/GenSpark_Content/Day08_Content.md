# Day 8 Content - Optimization & Evaluation

## Learning Objectives
- Design resilient tool error handling
- Implement fallback backends for failed tools
- Measure retrieval and groundedness quality
- Optimize performance (batching, caching)

## Skeleton 8 (Day 8 - Reliability Layer)
```
Tool Resilience:
├── Web search fallback backends (lite → html → RSS)
├── Error handling contracts
└── Outage transparency (no hallucination)
```

## The 4 Stages of Day 8
1. **Stage A:** Reliability vs performance tradeoffs
2. **Stage B:** Tool resilience and fallback strategies
3. **Stage C:** Evaluation metrics and rubrics
4. **Stage D:** Performance optimization

## Reliability in GenAI Systems
- **Challenge:** Tools fail (network down, model timeout, no data found)
- **Production requirement:** Fail gracefully, don't hallucinate
- **Strategy:** Fallback backends, explicit error messages, outage transparency

## The Web Search Failure Problem
- ❌ **WRONG:** DuckDuckGo API returns 403 → Treat as "no results" → Make up facts
- ✅ **RIGHT:** DuckDuckGo API returns 403 → Report outage explicitly → Don't synthesize

## Web Search Resilience (EXACT CODE from src/tools.py:51)
```python
backend_errors = []
backends = ["lite", "html"]

for backend in backends:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(clean_query, max_results=10, backend=backend))
        if results:
            # Process results
            return formatted_results
    except Exception as e:
        backend_errors.append(f"{backend}: {e}")
```
- **Teaching Point:** Try multiple backends, don't fail on first error

## Outage-Safe Return (EXACT CODE from src/tools.py:78)
```python
return (
    "WEB: Search temporarily unavailable. "
    "Treat this as a retrieval outage, not as factual evidence about the topic. "
    f"Debug detail: {' | '.join(backend_errors)}"
)
```
- **Teaching Point:** Explicit message prevents analyst from fabricating analysis

## Tool Error Handling Philosophy
- **Contract:** Each tool returns a message, never throws uncaught exception
- **Analyst reads message:** "No documents found" vs "Search unavailable" = different handling
- **Writer includes status:** Outage status in final output if needed

## Evaluation Metrics (What to Measure)

### Retrieval Quality
- **Precision:** Of top 3 retrieved docs, how many are relevant?
- **Recall:** Of all relevant docs in database, did we retrieve any?
- **Trade-off:** Low k = high precision, high k = high recall
- **NewsNexus choice:** k=3 for balance

### LLM Groundedness
- Read final output
- Highlight facts → find source
- Score: % of facts that are in retrieved documents
- **Target:** 90%+ grounded facts

### Response Coherence
- Is output structured and readable?
- Pass/Fail on formatting requirements

### User Satisfaction
- Did the answer help the user?
- Feedback form after each query

## Groundedness Scoring Rubric
- ✓ Every claim has cited source in retrieved documents
- ✓ No facts introduced that aren't in sources
- ✓ Direct quotes marked with quotation marks
- ✓ Synthesis is stated as "derived from" not "is stated in"

## Performance Optimization
- Batch embeddings: Embed 100 docs at once (faster than 1 at a time)
- Cache embeddings: Don't re-embed documents
- Use GPU: Ollama can offload embedding to NVIDIA GPU
- Monitor: Track inference time per node

## Monitoring in Production
- Log every tool call: Success? Failure? Response time?
- Alert on: Tool failures > 5% of calls, P95 latency > 10s
- Dashboard: Show reliability metrics over time

## Why This Day Matters
- Systems fail gracefully, don't hallucinate
- Evaluation metrics = confidence in production deployments
- This makes GenAI suitable for enterprise use

## 6-Hour Teaching Script

**Hour 1: Reliability Tradeoffs (60 min)**
- Performance vs reliability: Always online vs occasionally down
- Why graceful failure matters: Medical/legal/finance domains
- Examples: Wrong medical advice costs lives

**Hour 2: Walk Through Web Search Fallback (60 min)**
- Show: DuckDuckGo backend options (lite, html, news)
- Show: try/except loop logic
- Show: Error accumulation
- Trace: What happens when lite fails, html succeeds

**Hour 3: Hands-on: Break & Fix Web Search (60 min)**
- Simulate: Block internet access
- See: All backends fail
- Verify: Outage message returned (no hallucination)
- Fix: Restore internet, test again

**Hour 4: Build Evaluation Rubric (60 min)**
- Create groundedness checklist
- Score 5 real outputs using rubric
- Rate 1-5 for groundedness
- Identify patterns in weak answers

**Hour 5: Measure Retrieval Quality (60 min)**
- Sample 10 queries
- For each query: Top 3 docs relevant?
- Calculate: Precision, Recall
- Compare: Expected vs actual

**Hour 6: Optimize Performance (60 min)**
- Measure baseline latency per node
- Implement batch embeddings
- Re-measure latency
- Calculate: % improvement
- Identify: Slowest node

## Assessment Checkpoint
By end of Day 8, students should:
- ✓ Design fallback strategies for tool failures
- ✓ Score outputs using groundedness rubric
- ✓ Measure retrieval precision and recall
- ✓ Optimize system performance
