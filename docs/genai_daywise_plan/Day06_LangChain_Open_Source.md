# Day 6 - LangChain (Open Source) (6 Hours)

## Skeleton 6 (Day 6)
Orchestrated multi-node workflow skeleton.

```text
AgentState
	-> Researcher Node
	-> Analyst Node
	-> Writer Node
	-> END
```

## Stage-by-Stage Delivery
1. Stage A - LangChain tools and model binding
2. Stage B - LangGraph state schema and node contracts
3. Stage C - Edge wiring and execution graph
4. Stage D - Checkpoint memory and reproducible threading

## Code Breakdown
- Tool decorator pattern: [src/tools.py](src/tools.py#L8)
- Model + tools binding: [src/tools.py](src/tools.py#L123)
- Shared state schema: [src/agents.py](src/agents.py#L13)
- Node definitions: [src/agents.py](src/agents.py#L24), [src/agents.py](src/agents.py#L91), [src/agents.py](src/agents.py#L153)
- Graph registration: [src/agents.py](src/agents.py#L198)
- Flow edges: [src/agents.py](src/agents.py#L205)
- Checkpointer setup: [src/agents.py](src/agents.py#L210)

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: LangChain vs LangGraph responsibilities.
- Hour 2: Build and validate tool contracts.
- Hour 3: Explain `AgentState` and message accumulation behavior.
- Hour 4: Build graph edges and run stream output.
- Hour 5: Add/check checkpoint behavior with thread IDs.
- Hour 6: Graph debugging using node-level logs.

## Assessment Checkpoint
- Student can implement a new node and integrate it safely into the graph.

