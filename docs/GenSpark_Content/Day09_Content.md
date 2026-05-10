# Day 9 Content - Project Phase 1 (Memory & Persistence)

## Learning Objectives
- Understand long-term memory patterns in GenAI
- Implement archive strategies with vector similarity
- Inject memory context into prompts
- Evaluate memory retrieval quality

## Skeleton 9 (Day 9 - Memory Layer)
```
Memory Archive:
├── Separate ChromaDB collection
├── Topic similarity search (threshold 0.4)
├── Memory injection in researcher prompt
└── Archive save on human approval
```

## The 4 Stages of Day 9
1. **Stage A:** Memory patterns in GenAI (why persistence matters)
2. **Stage B:** Archive storage and retrieval
3. **Stage C:** Memory context injection
4. **Stage D:** Memory-aware reasoning

## Why Memory Matters
- **Day 1 Problem:** User asks about "Climate Policy" on Monday
- **Day 3 Problem:** User asks about "Environmental Regulations" on Wednesday (related topic)
- **Without memory:** Re-research everything (wasteful)
- **With memory:** "I recall similar analysis from Monday → reuse + adapt"

## Memory Architecture
- **Separate Collection:** data/archive_memory/ (different from ingestion ChromaDB)
- **Each Entry:** (topic_query, analysis_summary, timestamp)
- **Similarity Threshold:** 0.4 = "similar enough to use as context"

## Memory Check in Researcher (EXACT CODE from src/phase5_final.py:30)
```python
def researcher_with_memory_node(state: AgentState):
    last_message = state["messages"][0]
    user_topic = last_message.content
    
    memory_context = memory_store.check_memory(user_topic)
    
    system_prompt = f"""...
    CRITICAL MEMORY CONTEXT:
    {memory_context}
    ..."""
    
    response = llm_with_tools.invoke([
        SystemMessage(content=system_prompt), 
        last_message
    ])
```
- **Teaching Point:** Memory injected into researcher prompt before tool calls

## Memory Store API (EXACT CODE from src/memory_store.py:11)
```python
class MemoryStore:
    def save_memory(self, topic: str, summary: str):
        # Store (topic, summary) in archive ChromaDB
    
    def check_memory(self, topic: str) -> str:
        # Search archive: similar_search(topic, k=1)
        # if score < 0.4: return "No prior analysis"
        # else: return "I found a similar analysis from [date]: [summary]"
```

## Memory Workflow
1. Query enters Researcher
2. Researcher calls memory_store.check_memory()
3. If found: Inject past analysis into prompt
4. Researcher: "Use memory as context, gather any new facts"
5. On approval: Call memory_store.save_memory() to archive

## Archive Structure
- **Location:** data/archive_memory/chroma.sqlite3
- **Metadata:** topic, summary, timestamp, source docs
- **Persistence:** Survives app restarts

## Memory Update Workflow (Visual)
```text
Query 1: "Climate Policy" 
→ Researcher → Analyst → Writer 
→ User approves 
→ memory_store.save_memory("Climate Policy", analysis)

Query 2: "Environmental Rules" (similar to Query 1)
→ memory_store.check_memory() 
→ Finds Query 1 analysis with score 0.6 
→ Injects: "Prior analysis: [summary]" into Researcher prompt
→ Researcher builds on prior analysis
```

## Phase 1 Deliverables
- ✓ Memory store implemented and integrated
- ✓ Researcher reads from memory before researching
- ✓ Memory saves on human approval
- ✓ Archive grows over time

## Phase 1 Evaluation
- Test 1: Same query on day 1 and day 2 → should use memory
- Test 2: Related but different query → should find memory and adapt
- Test 3: Unrelated query → should report "No prior"
- Test 4: Restart app → memory persists

## Development Planning Checklist (Whiteboard Live)
- ✓ Problem statement: "Avoid re-researching similar topics"
- ✓ Data sources finalized: Internal archive
- ✓ Retrieval quality criteria: Similarity > 0.4 = reusable
- ✓ Agent output sections defined: Researcher memo format
- ✓ Review/approval workflow defined: Memory saves on approve

## Why This Day Matters
- Memory = efficiency boost + context awareness
- User sees: "I remember investigating this before"
- Foundation for Day 10 HITL approval gates

## 6-Hour Teaching Script

**Hour 1: Memory Patterns in GenAI (60 min)**
- Why persistence matters: Avoid re-work
- Memory patterns: Short-term (session) vs long-term (archive)
- ChromaDB as memory backend
- Use cases: Consulting systems, research assistants

**Hour 2: Archive Setup (60 min)**
- Create separate ChromaDB collection
- Store topic + summary + metadata
- Understand metadata structure
- Hands-on: Initialize archive

**Hour 3: Implement MemoryStore (60 min)**
- Write check_memory() function
- Implement similarity search
- Handle threshold (0.4)
- Test: Query → return prior analysis or "No prior"

**Hour 4: Memory Injection (60 min)**
- Modify researcher prompt to include memory context
- Show: CRITICAL MEMORY CONTEXT section
- Test: Query with memory vs without
- Observe: Researcher uses prior analysis

**Hour 5: Hands-on: Memory Flow (60 min)**
- Query 1: "Climate Policy" → approve → save to memory
- Query 2: "Environmental Rules" (similar) → memory injected
- Query 3: "Sports News" (unrelated) → no memory
- Verify: Memory persists across sessions

**Hour 6: Debug & Tune (60 min)**
- Why memory threshold is 0.4: Too low = wrong matches, too high = miss valid
- Adjust threshold, observe behavior
- Measure: How often is memory used?
- Identify: What queries should use memory?

## Assessment Checkpoint
By end of Day 9, students should:
- ✓ Explain long-term memory patterns
- ✓ Implement memory store with vector similarity
- ✓ Inject memory context into researcher prompt
- ✓ Tune similarity threshold for quality
