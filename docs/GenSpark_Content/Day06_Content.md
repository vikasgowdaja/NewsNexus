# Day 6 Content - LangChain & LangGraph

## Learning Objectives
- Understand graph-based orchestration vs sequential scripts
- Design shared state for multi-agent workflows
- Build workflows with nodes, edges, and state flow
- Implement checkpointing for interrupts (HITL prep)

## Skeleton 6 (Day 6 - Orchestration Layer)
```
Graph: Researcher → Analyst → Writer
State: messages, research_data, chart_data
Checkpointer: MemorySaver for persistence
```

## The 4 Stages of Day 6
1. **Stage A:** Graph concepts (nodes, edges, state, entry, exit)
2. **Stage B:** Shared state design and accumulation
3. **Stage C:** Graph construction and compilation
4. **Stage D:** Debugging graph execution

## From Sequential to Graph
- **Before:** Script calls model → processes result → calls model again
- **After:** Graph with nodes and edges → state flows through + persists
- **Why graph?** Enables checkpointing, interrupts, conditional routing, parallel execution

## Shared State (EXACT CODE from src/agents.py:13)
```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    research_data: List[str]
    chart_data: List[dict]
```
- **messages:** List of all conversation turns (accumulates with operator.add)
- **research_data:** Facts gathered by Researcher node
- **chart_data:** Structured data for Plotly from Analyst node

## Node Functions
- **Researcher Node:** Calls tools, updates messages with tool results
- **Analyst Node:** Reads messages, performs reasoning, outputs 6-section analysis
- **Writer Node:** Reads analysis, formats as detailed HTML

## Graph Construction (EXACT CODE from src/agents.py:193)
```python
workflow = StateGraph(AgentState)
workflow.add_node("Researcher", researcher_node)
workflow.add_node("Analyst", analyst_node)
workflow.add_node("Writer", writer_node)

workflow.set_entry_point("Researcher")
workflow.add_edge("Researcher", "Analyst")
workflow.add_edge("Analyst", "Writer")
workflow.add_edge("Writer", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```
- **Teaching Point:** Graph is declarative (nodes + edges), execution is compiled

## Execution Flow
1. Entry: User query enters Researcher node
2. Node 1: Researcher processes state, calls tools, appends to messages
3. Edge 1→2: State flows to Analyst
4. Node 2: Analyst reads all messages, processes analysis, appends
5. Edge 2→3: State flows to Writer
6. Node 3: Writer reads all messages, formats HTML, appends
7. Exit: Final state is checkpointed to memory

## State Accumulation Pattern
- **operator.add on messages list** means: don't replace, append
- Researcher appends tool calls: "I found 3 documents"
- Analyst appends analysis: "Executive summary: ..."
- Writer appends HTML: "<article>...</article>"
- Final state has full conversation thread for auditing

## Checkpointing (Interrupts for Day 10 HITL)
- **Compile with:** app.compile(checkpointer=memory)
- **Enables:** Pause before approval node, collect human feedback, resume with revised output
- **Foundation:** For Day 10 human-in-the-loop feature

## Why This Day Matters
- Graph composes stateless functions into workflows
- LangGraph = production-grade workflow engine
- Enables complex multi-agent systems with reliability

## 6-Hour Teaching Script

**Hour 1: Graph Concepts (60 min)**
- Nodes: Functions that process state
- Edges: Connections between nodes
- State: Shared data structure flowing through graph
- Entry/Exit: Where graph starts and ends
- Draw: Simple 3-node graph on whiteboard

**Hour 2: Build Minimal 2-Node Graph (60 min)**
- Researcher → Writer (skip Analyst)
- Implement StateGraph
- Add two nodes
- Add edge
- Compile and test

**Hour 3: Add Analyst Node (60 min)**
- Expand to full 3-node workflow
- Add Analyst between Researcher and Writer
- Trace state evolution at each node
- Observe: State accumulation through pipeline

**Hour 4: Conditional Edges (60 min)**
- If analyst confidence < 0.5, route back to Researcher
- Implement conditional_edge() function
- Test: See routing behavior
- Add multiple paths through graph

**Hour 5: Checkpointing & Interrupts (60 min)**
- Compile with checkpointer
- See state persisted after execution
- Inspect: data/archive_memory/ directory
- Teaser: Day 10 uses this for HITL

**Hour 6: Debug Graph Execution (60 min)**
- Print state after each node: print(app.get_state(config))
- Inspect messages list: How many tool calls? What was synthesized?
- Trace edge: Did it route to expected next node?
- Troubleshoot: Why did Analyst not output chart_data?

## Assessment Checkpoint
By end of Day 6, students should:
- ✓ Explain nodes, edges, state, entry, exit
- ✓ Design shared state structure for multi-agent systems
- ✓ Build 3-node workflow from scratch
- ✓ Implement conditional routing
- ✓ Understand checkpointing for persistence
