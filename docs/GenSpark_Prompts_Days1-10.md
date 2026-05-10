# GenSpark AI Prompts for NewsNexus - 10-Day Curriculum
## Copy Each Day's Prompt Directly into GenSpark AI

---

## **DAY 1 PROMPT - Intro to GenAI & Setup**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Intro to GenAI & Setup"

PROJECT CONTEXT: NewsNexus is a local-first Generative AI application that combines RAG (Retrieval-Augmented Generation) with multi-agent orchestration. This Day 1 teaches the foundational system setup required before any model logic.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 1: Intro to GenAI & Setup"
2. Slide: System Architecture Overview
   - Show stack: Python 3.10+ | Ollama (llama3.2, nomic-embed-text) | LangChain | ChromaDB | Streamlit
   - Emphasis: Local-first = Privacy-first
3. Slide: The 4 Stages of Setup
   - Stage A: GenAI architecture orientation (why these components exist)
   - Stage B: Environment and dependency setup (venv + pip install)
   - Stage C: Model/runtime preflight checks (ollama list verification)
   - Stage D: First successful app launch (streamlit run src/streamlit_app.py)
4. Slide: Critical Dependencies (from requirements.txt)
   - Show: langchain, langchain-chroma, langchain-ollama, streamlit, duckduckgo_search, feedparser
5. Slide: Model Contract (EXACT CODE BLOCK)
   Code to show on slide:
   ```python
   # From: run_all.py line 10
   REQUIRED_MODELS = ("llama3.2", "nomic-embed-text")
   ```
   Explain: Generation model (llama3.2) vs Embedding model (nomic-embed-text)
6. Slide: Preflight Safety Check (EXACT CODE BLOCK)
   Code to show on slide:
   ```python
   # From: run_all.py line 17
   def check_ollama_available() -> tuple[bool, str]:
       if shutil.which("ollama") is None:
           return False, "Ollama CLI was not found on PATH..."
       # ... validate models exist
       return True, "Ollama is reachable and required models are installed."
   ```
   Teaching Point: Why preflight checks prevent production disasters
7. Slide: App Bootstrap Point (EXACT CODE)
   ```python
   # From: src/streamlit_app.py line 21
   st.set_page_config(layout="wide", page_title="NewsNexus")
   ```
8. Slide: The 6-Hour Teaching Timeline
   - Hour 1: Concept framing + component dependency graph
   - Hour 2: Environment lab (venv setup)
   - Hour 3: Model lab (ollama pull llama3.2, ollama pull nomic-embed-text)
   - Hour 4: Code walkthrough (run_all.py start to finish)
   - Hour 5: Execution flow (trace terminal → Streamlit → browser)
   - Hour 6: Debug clinic (simulate failures + recovery)
9. Summary Slide: Why This Matters
   - 80% of early GenAI project failures are setup/runtime failures, not model failures
   - Skeleton 1 (minimal runnable): requirements.txt → run_all.py → src/streamlit_app.py

VISUAL REQUIREMENTS:
- Use code highlighting (Python syntax)
- Include filesystem tree visualization for Skeleton 1 structure
- Add icons: 🚀 for launch, ✅ for checks, ⚠️ for error scenarios
- Color code: Green for "checks pass", Red for "missing model"

OUTPUT FORMAT: 10-15 slides maximum. Include speaker notes with timing (1 min per slide typical).
```

---

## **DAY 2 PROMPT - Prompt Engineering**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Prompt Engineering"

PROJECT CONTEXT: NewsNexus demonstrates real prompt engineering through three distinct agent roles (Researcher, Analyst, Writer). This Day 2 teaches how role-specific prompts eliminate noisy outputs and ensure structured, production-ready responses.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 2: Prompt Engineering"
2. Slide: The Prompt Anatomy (4 components)
   - Component 1: Role definition (What hat does the model wear?)
   - Component 2: Objective (What is the model's single job?)
   - Component 3: Constraints (What must/must-not happen?)
   - Component 4: Output schema (What exact format is expected?)
3. Slide: From Weak to Strong Prompts
   - ❌ WEAK: "Write about this topic"
   - ✅ STRONG: [Show researcher prompt from Day 2 code below]
4. Slide: The Researcher Role (EXACT CODE BLOCK)
   ```python
   # From: src/agents.py line 31
   sys_msg = SystemMessage(content=f"""You are a data gatherer.
   The current date is {datetime.now().strftime("%B %d, %Y")}.
   Use tools to find facts about the user's topic.
   Do not analyze, just report facts.
   
   IMPORTANT QUERY RULES:
   - If the user message contains an obvious typo or misspelling, 
     infer the most likely intended topic and use the corrected topic in tool calls.
   - Example: if the user types 'nauruto', search for 'Naruto'.
   - Prefer mainstream entity/topic rather than niche crossover result.
   - Keep tool queries specific and aligned to user's intended topic.
   
   ALWAYS use 'lookup_policy_docs', 'web_search_stub', and 'rss_feed_search'.""")
   ```
   Teaching Point: Notice the typo-correction rule built into the prompt itself
5. Slide: The Analyst Role (EXACT CODE BLOCK)
   Show truncated version of analyst prompt from src/agents.py line 100
   ```python
   # Expected output structure (from analyst_node):
   6 SECTIONS REQUIRED:
   1. Executive Summary
   2. Key Findings
   3. Trend Analysis
   4. Evidence (with source citations)
   5. Implications
   6. Visualization metadata (JSON for Plotly)
   ```
6. Slide: The Writer Role (EXACT CODE BLOCK)
   ```python
   # From: src/agents.py line 162
   # Writer prompt ensures output is detailed HTML with semantic tags
   # Input: Previous agent messages + analysis sections
   # Output: <article><h1> ... <section> ... </section> ... </article>
   ```
7. Slide: Query Normalization in Action (EXACT CODE)
   ```python
   # From: src/streamlit_app.py line 221
   def normalize_topic(raw_topic: str) -> str:
       cleaned = raw_topic.strip()
       lower_cleaned = cleaned.lower()
       typo_map = {
           "nauruto": "Naruto",
       }
       return typo_map.get(lower_cleaned, cleaned)
   ```
   Use Case: User types "nauruto" → Normalized to "Naruto" → Passed to agents
   UI Feedback: "Interpreted topic: Naruto" shown before pipeline starts
8. Slide: Multi-Role Workflow
   - Researcher (Output: raw facts + sources)
   - → Analyst (Output: structured 6-section analysis)
   - → Writer (Output: formatted HTML article)
9. Slide: Prompt Quality Evaluation Rubric
   - ✓ Is the role definition clear and unmistakable?
   - ✓ Is output format specified (JSON, HTML, structured text)?
   - ✓ Are constraints (don't do X) explicit?
   - ✓ Do examples show edge cases?
10. Slide: The 6-Hour Teaching Timeline
    - Hour 1: Prompt engineering theory with enterprise examples
    - Hour 2: Build a weak prompt, observe noisy output
    - Hour 3: Add role + output constraints, compare quality improvement
    - Hour 4: Deep dive into analyst prompt sections
    - Hour 5: Deep dive into writer prompt and HTML layout
    - Hour 6: Prompt review exercise (students critique each other's prompts)
11. Summary Slide: Why This Matters
    - Skeleton 2 (Prompt Layer): Prompt design directly controls output quality
    - Better prompts = less hallucination, better structure, fewer revisions

VISUAL REQUIREMENTS:
- Side-by-side comparison: Weak vs Strong prompt output
- Highlight key phrases in prompts (role, constraints, schema)
- Show typo-correction path with before/after arrows
- Color code: Gray for "weak", Green for "strong"

OUTPUT FORMAT: 12-15 slides maximum. Include speaker notes.
```

---

## **DAY 3 PROMPT - Working with Open Models**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Working with Open Models"

PROJECT CONTEXT: NewsNexus uses two Ollama models: llama3.2 (generation) and nomic-embed-text (embeddings). This Day 3 teaches model wiring—how to integrate open-source models into production workflows.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 3: Working with Open Models"
2. Slide: Generation vs Embedding Models
   - Generation Model (llama3.2): Takes text, outputs text (chat responses)
   - Embedding Model (nomic-embed-text): Takes text, outputs vectors (semantic search)
   - Why separate? Different optimization objectives
3. Slide: Model Selection Strategy
   - llama3.2: Good general-purpose model, ~2GB, ~4GB RAM to run
   - nomic-embed-text: Lightweight embedder, ~274MB, ~1GB RAM to run
   - Constraint: Local machine = model size + inference speed tradeoff
4. Slide: Chat Model Setup (EXACT CODE BLOCK)
   ```python
   # From: src/tools.py line 121
   def get_llm_with_tools():
       llm = ChatOllama(model="llama3.2", temperature=0)
       tools = [lookup_policy_docs, web_search_stub, rss_feed_search]
       llm_with_tools = llm.bind_tools(tools)
       return llm, llm_with_tools, tools
   ```
   Teaching Point: temperature=0 means deterministic (good for production), not creative
5. Slide: Tool Binding Concept
   - Model alone: "What do you think about climate?"
   - Model + tools: "Search for climate facts, analyze them, write report"
   - bind_tools() tells model which functions it can call
6. Slide: Embedding Model in Indexing (EXACT CODE BLOCK)
   ```python
   # From: src/ingestion.py line 30
   from langchain_ollama import OllamaEmbeddings
   embedding_model = OllamaEmbeddings(model="nomic-embed-text")
   
   # Later in pipeline:
   vector_store = Chroma.from_documents(
       documents=chunks,
       embedding=embedding_model,
       persist_directory="data/chroma_db"
   )
   ```
   Flow: PDF → chunks → embed each chunk → store vectors in DB
7. Slide: Embedding Model in Retrieval (EXACT CODE BLOCK)
   ```python
   # From: src/retrieval.py line 20
   # During search:
   query_embedding = embedding_model.embed_query("user question")
   similar_docs = vector_store.similarity_search_with_score(query, k=3)
   ```
   Flow: User query → embed query → find nearest vectors → return docs
8. Slide: Model Verification Checklist
   - ✓ ollama list (confirms models installed)
   - ✓ First inference is slow (model loading into RAM)
   - ✓ Subsequent calls are faster (cached in memory)
9. Slide: The 6-Hour Teaching Timeline
   - Hour 1: Generation vs embedding model responsibilities
   - Hour 2: Model pull demo, ollama list, selection strategy
   - Hour 3: Trace chat model invocation in tools and agents
   - Hour 4: Trace embedding usage in indexing and retrieval
   - Hour 5: Local performance constraints and batching rationale
   - Hour 6: Runtime failure recovery (missing model, daemon down)
10. Slide: Common Failures & Recovery
    - ❌ "Model not found" → Run: ollama pull llama3.2
    - ❌ "Connection refused" → Ollama daemon not running
    - ❌ "Out of memory" → Need more RAM or smaller model
    - ✅ Preflight check (Day 1) prevents these before app starts
11. Summary Slide: Why This Matters
    - Skeleton 3 (Model Wiring): Embedding + generation together enable RAG
    - Open models = no API keys, no rate limits, full local control

VISUAL REQUIREMENTS:
- Show embedding vector space diagram (2D visualization of semantic space)
- Model size comparison chart (llama3.2 vs nomic vs other options)
- Architecture diagram: Model → Tool → Response flow
- Color code: Purple for models, Blue for tools

OUTPUT FORMAT: 12-15 slides maximum. Include speaker notes.
```

---

## **DAY 4 PROMPT - Embeddings & Semantic Search**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Embeddings & Semantic Search"

PROJECT CONTEXT: NewsNexus uses vector similarity search to find relevant documents before passing them to the LLM. This Day 4 teaches the chunking → embedding → retrieval pipeline.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 4: Embeddings & Semantic Search"
2. Slide: From Keywords to Semantics
   - Keyword search (old): "Find documents with word 'climate'" = brittle, misses synonyms
   - Semantic search (modern): "Find documents ABOUT climate change" = flexible, understands meaning
3. Slide: The Chunking Strategy (EXACT CODE BLOCK)
   ```python
   # From: src/ingestion.py line 20
   text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=500,
       chunk_overlap=50,
       length_function=len,
       is_separator_regex=False,
   )
   chunks = text_splitter.split_documents(raw_documents)
   ```
   Why chunk_size=500? Trade-off: enough context (500 chars ≈ 100 words) vs efficient embedding
   Why overlap=50? Preserve context at chunk boundaries
4. Slide: Why Chunking Matters
   - Without chunks: Embed entire 100-page PDF = expensive, slow
   - With chunks: Embed small sections = fast, granular retrieval
   - Chunk size too small = loses context
   - Chunk size too large = expensive embeddings
5. Slide: Embedding Process
   - Input: One chunk of text
   - Process: nomic-embed-text model processes text → outputs 768-dimensional vector
   - Output: Vector stored in ChromaDB with metadata (source, page number)
6. Slide: Semantic Similarity Retrieval (EXACT CODE BLOCK)
   ```python
   # From: src/retrieval.py line 31
   results = vector_store.similarity_search_with_score(query, k=k+2)
   
   # The score is distance in vector space (lower = more similar)
   # k+2 means fetch extra results for hybrid search filtering
   ```
7. Slide: Hybrid Search with Keyword Boost (EXACT CODE BLOCK)
   ```python
   # From: src/retrieval.py line 37
   for doc, score in results:
       content = doc.page_content.lower()
       term_matches = sum(1 for term in query_terms if term in content)
       boosted_score = score - (term_matches * 0.05)  # Boost exact matches
   ```
   Example: Query "climate policy" + exact keyword match in doc = lower score = ranked higher
8. Slide: Vector Space Visualization
   - Each embedding is a point in 768-dimensional space (visualize as 2D for humans)
   - Semantically similar documents cluster near each other
   - "climate change" and "global warming" are close in vector space
9. Slide: The 6-Hour Teaching Timeline
   - Hour 1: Keyword search limitations with examples
   - Hour 2: Embedding concept (text → 768-dim vector)
   - Hour 3: Chunking strategy tradeoffs
   - Hour 4: Hands-on: Chunk a document, embed it, store in ChromaDB
   - Hour 5: Hands-on: Query and retrieve semantically related documents
   - Hour 6: Debug clinic (why is wrong document ranked #1? Check boosting logic)
10. Slide: Chunking Mistakes to Avoid
    - ❌ Chunk too small (< 100 chars) = broken context
    - ❌ Chunk too large (> 2000 chars) = expensive embeddings
    - ❌ No overlap = missing context at boundaries
    - ✅ 500 chars + 50 overlap = NewsNexus sweet spot
11. Slide: Performance Optimization
    - Batch embeddings (embed 100 chunks at once vs 1 at a time)
    - Use GPU if available (Ollama can offload to GPU)
    - Cache embeddings (don't re-embed on every query)
12. Summary Slide: Why This Matters
    - Skeleton 4 (Retrieval Layer): Semantic search finds relevant docs before LLM
    - Better retrieval = better grounded responses from LLM
    - Vector similarity is the foundation of RAG (Day 5)

VISUAL REQUIREMENTS:
- 2D vector space diagram showing semantic clusters
- Chunk boundary diagram (overlap visualization)
- Comparison chart: Keyword vs Semantic search results
- Timeline: chunk → embed → store → query → retrieve

OUTPUT FORMAT: 12-15 slides maximum. Include speaker notes.
```

---

## **DAY 5 PROMPT - RAG Pipeline**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "RAG Pipeline (Retrieval-Augmented Generation)"

PROJECT CONTEXT: NewsNexus is fundamentally a RAG system. This Day 5 teaches how retrieved documents prevent LLM hallucination by grounding responses in real data.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 5: RAG Pipeline"
2. Slide: The Hallucination Problem
   - LLM alone: "What does the Climate Policy Act say?" → Model makes up plausible-sounding answer
   - LLM + RAG: "What does the Climate Policy Act say?" → Model reads actual policy, extracts facts
   - RAG = Retrieval-Augmented Generation = facts first, then synthesize
3. Slide: The RAG Trust Model
   - Source of truth: Internal PDF documents (policies, reports)
   - Retrieval step: Find relevant documents matching user query
   - Synthesis step: LLM reads retrieved docs and answers based on them
   - Citation step: Report where each fact came from
4. Slide: The Complete RAG Flow (Visual Pipeline)
   - User Query: "What is the climate policy?"
   - → Retrieve Step: Find 3 most relevant PDFs (semantic search from Day 4)
   - → LLM Step: "Here's what the policy says: [from retrieved docs]"
   - → Citation Step: "Source: page 2 of Climate_Policy.pdf"
5. Slide: RAG Tool Contract (EXACT CODE BLOCK)
   ```python
   # From: src/tools.py line 9
   @tool
   def lookup_policy_docs(query: str) -> str:
       if isinstance(query, str) and "{" in query:
           query = query.replace("{", "").replace("}", "").replace("value:", "")
       
       docs = retrieve_documents(query, k=3)  # Get top 3 relevant docs
       if not docs:
           return f"RAG: No relevant internal documents found for query: '{query}'."
       
       results = []
       for doc, score in docs:
           source_name = doc.metadata.get('source', 'Unknown PDF')
           basename = os.path.basename(source_name)
           safe_source_path = source_name.replace('\\', '/')
           results.append(f"Content: {doc.page_content}\\nSource Link: [{basename}](file:///{safe_source_path})")
       
       return "\\n\\n".join(results)
   ```
   Teaching Point: Notice the tool ALWAYS returns source link, never hides provenance
6. Slide: Inside lookup_policy_docs
   - Input: User query as string
   - Process: Call retrieve_documents() (from Day 4) to find top 3 semantically similar chunks
   - Output: Chunk content + source file name + file path
   - Contract: Always returns source, never synthesizes facts
7. Slide: Tool Invocation from Agent (EXACT CODE BLOCK)
   ```python
   # From: src/agents.py line 50
   # Researcher node calls tools:
   response = llm_with_tools.invoke([system_message, user_message])
   # Model decides to call lookup_policy_docs, web_search_stub, or rss_feed_search
   ```
8. Slide: RAG vs No-RAG Comparison
   - NO RAG: "What's the climate policy?" → Generic 3-point summary (likely hallucinated)
   - RAG: "What's the climate policy?" → 6-section analysis grounded in actual policy docs
9. Slide: Edge Cases in RAG
   - No documents found: Tool returns "No relevant docs found" (honest failure)
   - Weak match: Top result has low relevance score → Still returned but analyst notes low confidence
   - Ambiguous query: Multiple docs retrieved → Analyst synthesizes common themes
10. Slide: The 6-Hour Teaching Timeline
    - Hour 1: Hallucination discussion with business examples (medical, finance, legal)
    - Hour 2: Walk through lookup_policy_docs() end-to-end
    - Hour 3: Trace retrieved chunk and metadata into response
    - Hour 4: Run same query with/without RAG and compare outputs
    - Hour 5: Analyze edge cases (no documents, weak matches, contradictions)
    - Hour 6: Build groundedness rubric for student grading (fact-checking)
11. Slide: Groundedness Rubric
    - ✓ Every claim has cited source in retrieved documents
    - ✓ No facts introduced that aren't in the sources
    - ✓ Direct quotes marked with quotation marks
    - ✓ Synthesis is stated as "derived from" not "is stated in"
12. Slide: RAG Quality Metrics
    - Retrieval recall: Did we fetch the document that contains the answer?
    - Retrieval precision: Did we fetch irrelevant documents?
    - LLM grounding: Did model stay true to retrieved docs?
13. Summary Slide: Why This Matters
    - Skeleton 5 (RAG Core): Retrieved docs = source of truth
    - RAG = enterprise-grade vs generic LLM responses
    - This is the foundation of Days 6-10 agent orchestration

VISUAL REQUIREMENTS:
- Flowchart: Query → Retrieve → Synthesize → Cite
- Side-by-side: No-RAG output vs RAG output
- Color code: Orange for retrieval, Purple for synthesis, Green for citations
- Include actual code block on slides (syntax highlighted)

OUTPUT FORMAT: 13-15 slides maximum. Include speaker notes with timing.
```

---

## **DAY 6 PROMPT - LangChain & LangGraph**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "LangChain & LangGraph Orchestration"

PROJECT CONTEXT: NewsNexus uses LangGraph StateGraph to orchestrate Researcher → Analyst → Writer workflow. This Day 6 teaches how to compose multi-agent systems with LangChain.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 6: LangChain & LangGraph Orchestration"
2. Slide: From Sequential Calls to Graph
   - Before: Script calls model → processes result → calls model again
   - After: Graph with nodes and edges → state flows through + persists
   - Why graph? Enables checkpointing, interrupts, conditional routing, parallel execution
3. Slide: The Shared State (EXACT CODE BLOCK)
   ```python
   # From: src/agents.py line 13
   class AgentState(TypedDict):
       messages: Annotated[List[BaseMessage], operator.add]
       research_data: List[str]
       chart_data: List[dict]
   ```
   - messages: List of all conversation turns (accumulates with operator.add)
   - research_data: Facts gathered by Researcher node
   - chart_data: Structured data for Plotly from Analyst node
4. Slide: Node Functions
   - Researcher Node: Calls tools, updates messages with tool results
   - Analyst Node: Reads messages, performs reasoning, outputs 6-section analysis
   - Writer Node: Reads analysis, formats as detailed HTML
5. Slide: Graph Construction (EXACT CODE BLOCK)
   ```python
   # From: src/agents.py line 193
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
   Teaching Point: Graph is declarative (nodes + edges), execution is compiled
6. Slide: Execution Flow
   - Entry: User query enters Researcher node
   - Node 1: Researcher processes state, calls tools, appends to messages
   - Edge 1→2: State flows to Analyst
   - Node 2: Analyst reads all messages, processes analysis, appends
   - Edge 2→3: State flows to Writer
   - Node 3: Writer reads all messages, formats HTML, appends
   - Exit: Final state is checkpointed to memory
7. Slide: State Accumulation Pattern
   - operator.add on messages list means: don't replace, append
   - Researcher appends tool calls: "I found 3 documents"
   - Analyst appends analysis: "Executive summary: ..."
   - Writer appends HTML: "<article>...</article>"
   - Final state has full conversation thread for auditing
8. Slide: Checkpointing (Interrupts for Human-in-the-Loop)
   - Compile with: app.compile(checkpointer=memory)
   - Enables: Pause before approval node, collect human feedback, resume with revised output
   - Day 10 feature: HITL loop integrated here
9. Slide: The 6-Hour Teaching Timeline
   - Hour 1: Graph concepts (nodes, edges, state, entry, exit)
   - Hour 2: Build minimal 2-node graph (Researcher → Writer)
   - Hour 3: Add Analyst node, test 3-node workflow
   - Hour 4: Add conditional edges (if condition → route A else B)
   - Hour 5: Add checkpointing and interrupts
   - Hour 6: Debug graph execution (inspect state at each node)
10. Slide: Debugging Graph Execution
    - Print state after each node: print(app.get_state(config))
    - Inspect messages list: How many tool calls? What was synthesized?
    - Trace edge: Did it route to the expected next node?
11. Slide: Advanced Features (Teaser for Day 10)
    - Conditional routing: "If analyst confidence < 0.5, route to Researcher again"
    - Parallel nodes: "Run multiple tools concurrently"
    - Interrupts: "Pause before node X for human approval"
    - Memory: "Persist state across sessions"
12. Summary Slide: Why This Matters
    - Skeleton 6 (Orchestration Layer): Graph composes stateless functions into workflows
    - LangGraph = production-grade workflow engine
    - Enables complex multi-agent systems with reliability

VISUAL REQUIREMENTS:
- Graph diagram: 3 nodes (Researcher, Analyst, Writer) with edges
- State evolution visualization: Show messages list growing at each node
- Code snippets highlighted on slides
- Color code: Blue for nodes, Green for edges, Purple for state

OUTPUT FORMAT: 12-15 slides maximum. Include speaker notes.
```

---

## **DAY 7 PROMPT - GenAI Applications (Streamlit)**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "GenAI Applications with Streamlit"

PROJECT CONTEXT: NewsNexus UI is built with Streamlit. This Day 7 teaches how to wrap the LangGraph pipeline in a user-facing web application.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 7: GenAI Applications (Streamlit UI)"
2. Slide: UI Layer Purpose
   - Encapsulates: User input, session state, graph execution, real-time streaming
   - Handles: Text input, button clicks, display of intermediate results
   - Manages: State persistence across Streamlit reruns
3. Slide: Streamlit Basics (Quick Review)
   - Streamlit = Python framework that rerun on every interaction
   - Need session_state to persist data across reruns
   - Widgets (text_input, button, etc.) trigger reruns
4. Slide: Input & State Initialization (EXACT CODE BLOCK)
   ```python
   # From: src/streamlit_app.py (example from Day 7 lesson)
   st.set_page_config(layout="wide", page_title="NewsNexus")
   
   if "current_step" not in st.session_state:
       st.session_state.current_step = "idle"
       st.session_state.topic = ""
       st.session_state.messages = []
       st.session_state.research_data = []
   ```
   Teaching Point: Initialize session_state once, never reinitialize on reruns
5. Slide: Topic Input with Normalization (EXACT CODE BLOCK)
   ```python
   # From: src/streamlit_app.py line 343
   topic = st.text_input("Enter a topic:", placeholder="e.g., Climate Policy")
   
   if st.button("🚀 Start Agents", disabled=st.session_state.current_step != "idle") and topic:
       interpreted_topic = normalize_topic(topic)  # Correct typos
       st.session_state.topic = topic
       st.session_state.interpreted_topic = interpreted_topic
       st.session_state.current_step = "researching"
       st.session_state.messages = [HumanMessage(content=interpreted_topic)]
   ```
   Teaching Point: User types "nauruto" → Normalized to "Naruto" → Passed to agents
6. Slide: Graph Streaming into UI (EXACT CODE BLOCK)
   ```python
   # From: src/streamlit_app.py line 400
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
   Teaching Point: .stream() yields events as graph executes → update UI in real-time
7. Slide: Real-Time Status Updates
   - Placeholder for status: st.empty()
   - Update as nodes execute: placeholder.info("🔍 Researching...")
   - Build user confidence that system is working
8. Slide: Display Results
   - Research data → Expandable sections
   - Analysis → 6 sections with sources
   - HTML content → st.markdown() with unsafe_allow_html=True
9. Slide: Session State Lifecycle
   - Idle: Waiting for topic input
   - Researching: Graph executing, status updates
   - Analyzing: Analyst node output ready
   - Writing: Final HTML ready, show publish button
   - Memory saved: Archive written, ready for next query
10. Slide: Error Handling in UI
    - Tool failures (no docs found) → Display gracefully
    - Model timeouts → Show timeout message, offer retry
    - Ollama connection lost → Show specific error, recovery steps
11. Slide: The 6-Hour Teaching Timeline
    - Hour 1: Streamlit architecture (reruns, session_state, widgets)
    - Hour 2: Build minimal topic input → button → status display
    - Hour 3: Connect button to graph.stream() execution
    - Hour 4: Add real-time status updates during graph execution
    - Hour 5: Format and display results (research, analysis, HTML)
    - Hour 6: Debug Streamlit reruns (why does state disappear?)
12. Slide: Common Streamlit Mistakes
    - ❌ Initialize session_state on every rerun → lose data
    - ❌ Call graph.stream() on every widget interaction → waste computation
    - ❌ Don't check current_step before allowing new queries → confusing UX
    - ✅ Disable button until previous query completes
13. Summary Slide: Why This Matters
    - Skeleton 7 (UI Layer): Streamlit bridges graph → user interaction
    - Real-time streaming shows users what's happening
    - Session state persistence = smooth multi-turn workflows

VISUAL REQUIREMENTS:
- UI mockup: Input field, button, status messages, results
- State machine diagram: Idle → Researching → Analyzing → Writing → Memory saved
- Event flow: User click → .stream() events → UI update
- Color code: Green for active state, Gray for disabled

OUTPUT FORMAT: 12-15 slides maximum. Include speaker notes with UX tips.
```

---

## **DAY 8 PROMPT - Optimization & Evaluation**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Optimization & Evaluation"

PROJECT CONTEXT: NewsNexus demonstrates resilient tool design and evaluation metrics. This Day 8 teaches how to make GenAI systems reliable in production.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 8: Optimization & Evaluation"
2. Slide: Reliability in GenAI Systems
   - Challenge: Tools fail (network down, model timeout, no data found)
   - Production requirement: Fail gracefully, don't hallucinate
   - Strategy: Fallback backends, explicit error messages, outage transparency
3. Slide: The Web Search Failure Problem
   - DuckDuckGo API returns 403 Forbidden
   - ❌ WRONG: Treat 403 as "no results" and make up facts
   - ✅ RIGHT: Report outage explicitly, don't synthesize
4. Slide: Web Search Resilience (EXACT CODE BLOCK)
   ```python
   # From: src/tools.py line 51
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
   Teaching Point: Try multiple backends, don't fail on first error
5. Slide: Outage-Safe Return (EXACT CODE BLOCK)
   ```python
   # From: src/tools.py line 78
   return (
       "WEB: Search temporarily unavailable. "
       "Treat this as a retrieval outage, not as factual evidence about the topic. "
       f"Debug detail: {' | '.join(backend_errors)}"
   )
   ```
   Teaching Point: Explicit message prevents analyst from fabricating analysis
6. Slide: Tool Error Handling Philosophy
   - Contract: Each tool returns a message, never throws uncaught exception
   - Analyst reads message: "No documents found" vs "Search unavailable" = different handling
   - Writer includes outage status in final output if needed
7. Slide: Evaluation Metrics (What to Measure)
   - Retrieval Quality: Did we fetch relevant documents? (Precision/Recall)
   - LLM Groundedness: Did model stay true to retrieved docs? (Fact-check)
   - Response Coherence: Is the output structured and readable? (Pass/Fail)
   - User Satisfaction: Did the answer help the user? (Feedback)
8. Slide: Retrieval Precision & Recall
   - Precision: Of top 3 retrieved docs, how many are relevant?
   - Recall: Of all relevant docs in the database, did we retrieve any?
   - Trade-off: Low k = high precision, high k = high recall
   - NewsNexus chooses k=3 for balance
9. Slide: Groundedness Scoring
   - Read final output
   - Highlight facts → find source
   - Score: % of facts that are in retrieved documents
   - Target: 90%+ grounded facts
10. Slide: Performance Optimization
    - Batch embeddings: Embed 100 docs at once (faster than 1 at a time)
    - Cache embeddings: Don't re-embed documents
    - Use GPU: Ollama can offload embedding to NVIDIA GPU
    - Monitor: Track inference time per node
11. Slide: The 6-Hour Teaching Timeline
    - Hour 1: Reliability vs performance tradeoffs
    - Hour 2: Walk through web search fallback logic
    - Hour 3: Hands-on: Break web search, see graceful failure
    - Hour 4: Build evaluation rubric (groundedness checklist)
    - Hour 5: Score 5 real outputs using rubric
    - Hour 6: Optimize: Batch embeddings, measure latency improvement
12. Slide: Monitoring in Production
    - Log every tool call: Success? Failure? Response time?
    - Alert on: Tool failures > 5% of calls, P95 latency > 10s
    - Dashboard: Show reliability metrics over time
13. Summary Slide: Why This Matters
    - Skeleton 8 (Reliability Layer): Systems fail gracefully, don't hallucinate
    - Evaluation metrics = confidence in production deployments
    - This makes GenAI suitable for enterprise use

VISUAL REQUIREMENTS:
- Error flow chart: Try backend 1 → fail → try backend 2 → fail → return outage message
- Precision vs Recall visualization
- Performance timeline: Before optimization → After optimization
- Color code: Red for failures, Green for graceful handling

OUTPUT FORMAT: 12-15 slides maximum. Include speaker notes with rubric templates.
```

---

## **DAY 9 PROMPT - Project Phase 1 (Memory & Persistence)**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Project Phase 1 - Memory & Persistence"

PROJECT CONTEXT: NewsNexus integrates persistent memory to avoid re-researching the same topics. This Day 9 teaches long-term memory patterns and archive strategies.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 9: Project Phase 1 - Memory & Persistence"
2. Slide: Why Memory Matters
   - User asks about "Climate Policy" on Monday
   - User asks about "Environmental Regulations" on Wednesday (related topic)
   - Without memory: Re-research everything (wasteful)
   - With memory: "I recall similar analysis from Monday → reuse + adapt"
3. Slide: Memory Architecture
   - Separate ChromaDB collection: data/archive_memory/
   - Each entry: (topic_query, analysis_summary, timestamp)
   - Similarity threshold: 0.4 = "similar enough to use as context"
4. Slide: Memory Check in Researcher (EXACT CODE BLOCK)
   ```python
   # From: src/phase5_final.py line 30
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
   Teaching Point: Memory injected into researcher prompt before tool calls
5. Slide: Memory Store API (EXACT CODE BLOCK)
   ```python
   # From: src/memory_store.py line 11
   class MemoryStore:
       def save_memory(self, topic: str, summary: str):
           # Store (topic, summary) in archive ChromaDB
       
       def check_memory(self, topic: str) -> str:
           # Search archive: similar_search(topic, k=1)
           # if score < 0.4: return "No prior analysis"
           # else: return "I found a similar analysis from [date]: [summary]"
   ```
6. Slide: Memory Workflow
   - Query enters Researcher
   - Researcher calls memory_store.check_memory()
   - If found: Inject past analysis into prompt
   - Researcher: "Use memory as context, gather any new facts"
   - On approval: Call memory_store.save_memory() to archive
7. Slide: Archive Structure
   - Location: data/archive_memory/chroma.sqlite3
   - Metadata: topic, summary, timestamp, source docs
   - Persistence: Survives app restarts
8. Slide: Memory Update Workflow
   ```text
   Query 1: "Climate Policy" 
   → Researcher → Analyst → Writer 
   → User approves → memory_store.save_memory("Climate Policy", analysis)
   
   Query 2: "Environmental Rules" (similar to Query 1)
   → memory_store.check_memory() 
   → Finds Query 1 analysis with score 0.6 
   → Injects: "Prior analysis: [summary]" into Researcher prompt
   → Researcher builds on prior analysis
   ```
9. Slide: Phase 1 Deliverables
   - ✓ Memory store implemented and integrated
   - ✓ Researcher reads from memory before researching
   - ✓ Memory saves on human approval
   - ✓ Archive grows over time
10. Slide: Phase 1 Evaluation
    - Test 1: Same query on day 1 and day 2 → should use memory
    - Test 2: Related but different query → should find memory and adapt
    - Test 3: Unrelated query → should report "No prior"
    - Test 4: Restart app → memory persists
11. Slide: The 6-Hour Teaching Timeline
    - Hour 1: Memory patterns in GenAI (why persistence matters)
    - Hour 2: ChromaDB collection setup for archive
    - Hour 3: Implement MemoryStore class
    - Hour 4: Integrate memory into researcher prompt
    - Hour 5: Hands-on: Query → approve → check memory on next similar query
    - Hour 6: Debug memory retrieval (why score is low? Similarity threshold tuning)
12. Slide: Development Planning Checklist (Whiteboard Live)
    - ✓ Problem statement: "Avoid re-researching similar topics"
    - ✓ Data sources finalized: Internal archive
    - ✓ Retrieval quality criteria: Similarity > 0.4 = reusable
    - ✓ Agent output sections defined: Researcher memo format
    - ✓ Review/approval workflow defined: Memory saves on approve
13. Summary Slide: Why This Matters
    - Skeleton 9 (Memory Layer): Long-term learning from past queries
    - Memory = efficiency boost + context awareness
    - User sees: "I remember investigating this before"

VISUAL REQUIREMENTS:
- Archive directory structure tree
- Query flow: Check memory → Inject → Respond
- Timeline: Query 1 (save) → Query 2 (retrieve memory) → Query 3 (new)
- Color code: Gold for memory hits, Gray for memory misses

OUTPUT FORMAT: 13-15 slides maximum. Include speaker notes with whiteboard checklist.
```

---

## **DAY 10 PROMPT - Project Phase 2 (Human-in-the-Loop Approval)**
*Copy everything below into GenSpark AI*

```
Generate a PowerPoint presentation for: "Project Phase 2 - Human-in-the-Loop Approval"

PROJECT CONTEXT: NewsNexus integrates human approval gates before archiving analysis. This Day 10 teaches HITL patterns for production quality control.

PRESENTATION STRUCTURE:
1. Title Slide: "Day 10: Project Phase 2 - Human-in-the-Loop Approval"
2. Slide: The Quality Control Problem
   - Fully automated: Risk of low-quality or hallucinated analysis published
   - Fully manual: Slower but higher quality guarantee
   - HITL (Human-in-the-Loop): Automated + human approval for critical decisions
3. Slide: HITL Workflow
   - Researcher gathers facts (automated)
   - Analyst synthesizes analysis (automated)
   - Writer formats output (automated)
   - Approval Gate: Human reviews and decides: "Publish? Or revise?"
   - If revise: Send feedback back to Writer (or Researcher if major issues)
   - If approve: Archive to memory, deliver to user
4. Slide: LangGraph Interrupts for HITL (EXACT CODE BLOCK)
   ```python
   # From: src/phase4_human_loop.py line 22
   def human_approval_node(state: AgentState):
       # This node triggers an interrupt
       # App pauses here, waits for human input
       pass
   ```
   Teaching Point: Interrupt checkpoints pause execution mid-workflow
5. Slide: Conditional Routing After Approval (EXACT CODE BLOCK)
   ```python
   # From: src/phase4_human_loop.py line 30
   def route_after_human(state: AgentState) -> Literal["Writer", "__end__"]:
       last_msg = state["messages"][-1].content.lower()
       
       if "approve" in last_msg:
           return "__end__"  # Archive and finish
       else:
           return "Writer"   # Back to writer for revision
   ```
   Teaching Point: Human feedback → routing decision → conditional execution
6. Slide: Memory Archive on Approve (EXACT CODE BLOCK)
   ```python
   # From: src/phase5_final.py line 151
   if "approve" in feedback.lower():
       memory_store.save_memory(user_topic, draft)
       break  # Exit the HITL loop
   ```
   Teaching Point: Only archive on human approval, never on automated output alone
7. Slide: Full HITL Graph (Visual Diagram)
   - Entry: Researcher
   - → Analyst
   - → Writer
   - → Human Approval Node (INTERRUPT)
   - ← If "approve": END (archive to memory)
   - ← If "revise": Writer (feedback incorporated)
   - → Repeat approval gate until approved
8. Slide: Phase 2 Deliverables
   - ✓ Human approval gate integrated into graph
   - ✓ Conditional routing based on human feedback
   - ✓ Memory archive only on approval
   - ✓ Feedback loop enables iterative refinement
9. Slide: HITL Metrics
   - Approval rate: % of outputs approved on first pass
   - Revision cycles: Average iterations before approval
   - Time to approval: How long human takes to review
   - Revision value: Quality improvement from revision
10. Slide: UI for HITL (Streamlit Integration)
    - Display draft before approval gate
    - Show button: [✅ Approve] [❌ Revise with feedback]
    - Feedback text field for revision requests
    - Status: "Awaiting human approval"
11. Slide: Production Considerations
    - Scale: Who approves when multiple queries arrive?
    - SLA: How long to wait for approval before timeout?
    - Archive: What metadata to store with approved analysis?
    - Feedback: How to track human feedback patterns?
12. Slide: The 6-Hour Teaching Timeline
    - Hour 1: HITL concepts and when to use them
    - Hour 2: LangGraph interrupt checkpoints
    - Hour 3: Implement human_approval_node + route_after_human
    - Hour 4: Hands-on: Full workflow with approval, see pause + resume
    - Hour 5: Add feedback text field, route to Writer
    - Hour 6: Measure approval metrics, identify systemic revision patterns
13. Slide: Final System Architecture (Full 10-Day Build)
    - Day 1: Setup foundation
    - Day 2-3: Prompts + models
    - Day 4-5: Retrieval + RAG
    - Day 6-7: Orchestration + UI
    - Day 8: Reliability
    - Day 9: Memory persistence
    - Day 10: Human approval gates
    - Result: Production-ready enterprise GenAI system
14. Slide: Lessons Learned & Best Practices
    - ✓ Local-first = privacy + no API costs
    - ✓ Modular pipeline = testable + maintainable
    - ✓ Explicit error handling = reliability
    - ✓ Memory + HITL = user trust
    - ✓ Graph-based orchestration = scalable
15. Summary Slide: Why This Matters & Next Steps
    - Complete 10-day curriculum: From setup to production system
    - NewsNexus = teaching vehicle for real GenAI patterns
    - Extensions: Add document parsing, multi-format output, API layer

VISUAL REQUIREMENTS:
- HITL loop diagram: Query → Pipeline → Approval (INTERRUPT) → Feedback → Revision → Approve → Archive
- Metrics dashboard mockup: Approval rate, revision cycles, time to approval
- Full system architecture: All 10 days integrated into one diagram
- Color code: Blue for automation, Orange for human decision, Green for archive

OUTPUT FORMAT: 15-17 slides maximum. Include speaker notes with production deployment tips.

---

**BONUS: Deployment & Demo Slides** (Optional, add if needed)
- Slide: "Running NewsNexus Locally"
- Slide: "API Layer Extension (FastAPI)"
- Slide: "Scaling to Multiple Users"
- Slide: "Next: Knowledge Graph Indexing"
```

---

## **HOW TO USE THESE PROMPTS:**

1. **Copy one full prompt** (from Day 1 through Day 10 above)
2. **Open GenSpark AI** (https://gensparktools.com or your GenSpark interface)
3. **Paste the entire prompt** into the input field
4. **Click "Generate"** to create the PowerPoint
5. **Review the output** for project-specific code blocks, TOC references, and skeleton progression
6. **Download the PPT** when ready

---

## **What Each Prompt Includes:**

✅ **Exact code blocks** from NewsNexus files with line numbers  
✅ **Day-specific TOC topics** (not generic)  
✅ **Skeleton progression** (Day 1→10 builds incrementally)  
✅ **Visual requirements** (diagrams, color codes, syntax highlighting)  
✅ **Teaching timeline** (Hour-by-hour 6-hour script)  
✅ **Project context** (NewsNexus-specific, not generic GenAI)  
✅ **Hands-on activities** (Labs, debugging, evaluation)  
✅ **Assessment checkpoints** (What students should be able to do)  

---

## **Example: What You Get After Pasting Day 1 Prompt Into GenSpark:**

- Professional PowerPoint with 10-15 slides
- Slide 1: Title with gradient background
- Slide 2-7: Code blocks syntax-highlighted, with architecture diagrams
- Slide 8: 6-hour timeline with speaker notes
- Slide 9: Skeleton 1 file structure visualization
- Slide 10: Why this matters + learning objectives
- Slides 11+: Speaker notes with exact timing and debug scenarios

---

## **Next Steps After Generating PPTs:**

1. **Download all 10 PPTs** (Day 1 through Day 10)
2. **Add your own examples** (e.g., your own policy PDFs)
3. **Test live coding** (use PerDay_Live_Coding_Blocks.md during class)
4. **Collect feedback** from students after each day
5. **Refine prompts** based on student questions

Ready to paste into GenSpark? Any day you'd like me to customize further?
