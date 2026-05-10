# Per-Day Live Coding Blocks (Day 1 to Day 10)

Use these blocks directly during teaching demos. All snippets are aligned to the current NewsNexus implementation.

## Day 1 - Intro to GenAI & Setup

### Block 1: Required model contract (startup safety)
Source: [run_all.py](run_all.py#L10)

```python
REQUIRED_MODELS = ("llama3.2", "nomic-embed-text")
```

### Block 2: Preflight check before app launch
Source: [run_all.py](run_all.py#L17)

```python
def check_ollama_available() -> tuple[bool, str]:
    if shutil.which("ollama") is None:
        return False, "Ollama CLI was not found on PATH. Install Ollama before starting NewsNexus."

    probe = run_command(["ollama", "list"])
    if probe.returncode != 0:
        stderr = probe.stderr.strip() or probe.stdout.strip() or "Unable to reach Ollama."
        return False, f"Ollama is installed but not reachable: {stderr}"

    installed_models = probe.stdout.lower()
    missing = [model for model in REQUIRED_MODELS if model.lower() not in installed_models]
    if missing:
        missing_list = ", ".join(missing)
        return False, f"Missing Ollama models: {missing_list}. Run `ollama pull` for each missing model."

    return True, "Ollama is reachable and required models are installed."
```

## Day 2 - Prompt Engineering

### Block 1: Researcher role prompt
Source: [src/agents.py](src/agents.py#L31)

```python
sys_msg = SystemMessage(content=f"""You are a data gatherer.
The current date is {datetime.now().strftime("%B %d, %Y")}.
Use tools to find facts about the user's topic.
Do not analyze, just report facts.

IMPORTANT QUERY RULES:
- If the user message contains an obvious typo or misspelling, infer the most likely intended topic and use the corrected topic in tool calls.
- Example: if the user types 'nauruto', search for 'Naruto'.
- Prefer the most likely mainstream entity/topic rather than a niche crossover result.
- Keep tool queries specific and aligned to the user's intended topic.

ALWAYS use 'lookup_policy_docs', 'web_search_stub', and 'rss_feed_search' to gather a mix of PDF, Web, and Industry news.""")
```

### Block 2: UI typo normalization guardrail
Source: [src/streamlit_app.py](src/streamlit_app.py#L221)

```python
def normalize_topic(raw_topic: str) -> str:
    """Normalize obvious user typos to the most likely intended topic."""
    cleaned = raw_topic.strip()
    lower_cleaned = cleaned.lower()

    typo_map = {
        "nauruto": "Naruto",
    }

    return typo_map.get(lower_cleaned, cleaned)
```

## Day 3 - Working with Open Models

### Block 1: Chat model + tools binding
Source: [src/tools.py](src/tools.py#L121)

```python
def get_llm_with_tools():
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [lookup_policy_docs, web_search_stub, rss_feed_search]
    llm_with_tools = llm.bind_tools(tools)
    return llm, llm_with_tools, tools
```

### Block 2: Embedding model in ingestion pipeline
Source: [src/ingestion.py](src/ingestion.py#L30)

```python
from langchain_ollama import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
```

## Day 4 - Embeddings & Semantic Search

### Block 1: Chunking strategy
Source: [src/ingestion.py](src/ingestion.py#L20)

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)
chunks = text_splitter.split_documents(raw_documents)
```

### Block 2: Semantic retrieval + keyword boost
Source: [src/retrieval.py](src/retrieval.py#L31)

```python
results = vector_store.similarity_search_with_score(query, k=k+2)

if keyword_filter:
    query_terms = set(query.lower().split())

    for doc, score in results:
        content = doc.page_content.lower()
        term_matches = sum(1 for term in query_terms if term in content)
        boosted_score = score - (term_matches * 0.05)
        final_results.append((doc, boosted_score))

    final_results.sort(key=lambda x: x[1])
    final_results = final_results[:k]
```

## Day 5 - RAG Pipeline

### Block 1: RAG tool contract
Source: [src/tools.py](src/tools.py#L9)

```python
@tool
def lookup_policy_docs(query: str) -> str:
    if isinstance(query, str) and "{" in query:
        query = query.replace("{", "").replace("}", "").replace("value:", "")

    docs = retrieve_documents(query, k=3)
    if not docs:
        return f"RAG: No relevant internal documents found for query: '{query}'."

    results = []
    for doc, score in docs:
        source_name = doc.metadata.get('source', 'Unknown PDF')
        basename = os.path.basename(source_name)
        safe_source_path = source_name.replace('\\', '/')
        results.append(f"Content: {doc.page_content}\nSource Link: [{basename}](file:///{safe_source_path})")

    return "\n\n".join(results)
```

## Day 6 - LangChain + LangGraph

### Block 1: Shared graph state
Source: [src/agents.py](src/agents.py#L13)

```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    research_data: List[str]
    chart_data: List[dict]
```

### Block 2: Graph construction
Source: [src/agents.py](src/agents.py#L193)

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

## Day 7 - GenAI Applications (Streamlit)

### Block 1: Trigger and start pipeline
Source: [src/streamlit_app.py](src/streamlit_app.py#L343)

```python
if st.button("🚀 Start Agents", disabled=st.session_state.current_step != "idle") and topic:
    interpreted_topic = normalize_topic(topic)
    st.session_state.topic = topic
    st.session_state.interpreted_topic = interpreted_topic
    st.session_state.current_step = "researching"
    st.session_state.messages = [HumanMessage(content=interpreted_topic)]
    st.session_state.research_data = []
```

### Block 2: Stream graph events into UI
Source: [src/streamlit_app.py](src/streamlit_app.py#L400)

```python
for event in agent_app.stream(inputs, config):
    if "Researcher" in event:
        research_output = event["Researcher"]
        st.session_state.research_data = research_output.get("research_data", [])

    if "Analyst" in event:
        analyst_output = event["Analyst"]
        st.session_state.chart_data = analyst_output.get("chart_data", [])

    if "Writer" in event:
        writer_output = event["Writer"]
        st.session_state.draft_content = writer_output["messages"][-1].content
```

## Day 8 - Optimization & Evaluation

### Block 1: Web search resilience fallback
Source: [src/tools.py](src/tools.py#L51)

```python
backend_errors = []
backends = ["lite", "html"]

for backend in backends:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(clean_query, max_results=10, backend=backend))
        if results:
            ...
    except Exception as e:
        backend_errors.append(f"{backend}: {e}")
```

### Block 2: Outage-safe return contract
Source: [src/tools.py](src/tools.py#L78)

```python
return (
    "WEB: Search temporarily unavailable. "
    "Treat this as a retrieval outage, not as factual evidence about the topic. "
    f"Debug detail: {' | '.join(backend_errors)}"
)
```

## Day 9 - Project Phase 1

### Block 1: Memory-aware research node skeleton
Source: [src/phase5_final.py](src/phase5_final.py#L30)

```python
def researcher_with_memory_node(state: AgentState):
    last_message = state["messages"][0]
    user_topic = last_message.content

    memory_context = memory_store.check_memory(user_topic)

    system_prompt = f"""...\nCRITICAL MEMORY CONTEXT:\n{memory_context}\n..."""
    response = llm_with_tools.invoke([SystemMessage(content=system_prompt), last_message])
```

### Block 2: Development planning checklist (instructor live whiteboard)
```text
- Problem statement finalized
- Data sources finalized
- Retrieval quality criteria defined
- Agent output sections defined
- Review/approval workflow defined
```

## Day 10 - Project Phase 2

### Block 1: HITL routing and approval
Source: [src/phase4_human_loop.py](src/phase4_human_loop.py#L30)

```python
def route_after_human(state: AgentState) -> Literal["Writer", "__end__"]:
    last_msg = state["messages"][-1].content.lower()

    if "approve" in last_msg:
        return "__end__"
    else:
        return "Writer"
```

### Block 2: Final archive write on publish
Source: [src/phase5_final.py](src/phase5_final.py#L151)

```python
if "approve" in feedback.lower():
    memory_store.save_memory(user_topic, draft)
    break
```

---

## Instructor Tip
Use one block at a time in class. For each block, cover:
1. Why this block exists
2. Input/output of the block
3. Failure modes
4. How this block connects to the previous and next block
