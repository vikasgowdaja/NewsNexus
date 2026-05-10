# Day 7 Content - GenAI Applications (Streamlit)

## Learning Objectives
- Understand UI layer architecture for GenAI systems
- Manage session state across Streamlit reruns
- Integrate graph streaming into UI
- Build real-time status updates for long-running workflows

## Skeleton 7 (Day 7 - UI Layer)
```
Streamlit UI
├── Input: st.text_input (topic)
├── Action: st.button (Start Agents)
├── Processing: for event in agent_app.stream()
└── Display: Results panels + HTML content
```

## The 4 Stages of Day 7
1. **Stage A:** Streamlit architecture (reruns, session_state, widgets)
2. **Stage B:** Session state initialization and persistence
3. **Stage C:** Graph streaming and real-time UI updates
4. **Stage D:** Error handling and user feedback

## UI Layer Purpose
- **Encapsulates:** User input, session state, graph execution, real-time streaming
- **Handles:** Text input, button clicks, display of intermediate results
- **Manages:** State persistence across Streamlit reruns

## Streamlit Basics
- Streamlit = Python framework that reruns on every interaction
- **Problem:** Need session_state to persist data across reruns
- **Solution:** Initialize session_state once, never reinitialize on reruns

## Input & State Initialization (EXACT CODE from src/streamlit_app.py)
```python
st.set_page_config(layout="wide", page_title="NewsNexus")

if "current_step" not in st.session_state:
    st.session_state.current_step = "idle"
    st.session_state.topic = ""
    st.session_state.messages = []
    st.session_state.research_data = []
```
- **Teaching Point:** Initialize session_state once, never reinitialize on reruns

## Topic Input with Normalization (EXACT CODE from src/streamlit_app.py:343)
```python
topic = st.text_input("Enter a topic:", placeholder="e.g., Climate Policy")

if st.button("🚀 Start Agents", disabled=st.session_state.current_step != "idle") and topic:
    interpreted_topic = normalize_topic(topic)  # Correct typos
    st.session_state.topic = topic
    st.session_state.interpreted_topic = interpreted_topic
    st.session_state.current_step = "researching"
    st.session_state.messages = [HumanMessage(content=interpreted_topic)]
```
- **Teaching Point:** User types "nauruto" → Normalized to "Naruto" → Passed to agents

## Graph Streaming into UI (EXACT CODE from src/streamlit_app.py:400)
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
- **Teaching Point:** .stream() yields events as graph executes → update UI in real-time

## Real-Time Status Updates
- Placeholder for status: st.empty()
- Update as nodes execute: placeholder.info("🔍 Researching...")
- Build user confidence that system is working

## Display Results
- Research data → Expandable sections
- Analysis → 6 sections with sources
- HTML content → st.markdown() with unsafe_allow_html=True

## Session State Lifecycle
- **Idle:** Waiting for topic input
- **Researching:** Graph executing, status updates
- **Analyzing:** Analyst node output ready
- **Writing:** Final HTML ready, show publish button
- **Memory saved:** Archive written, ready for next query

## Error Handling in UI
- Tool failures (no docs found) → Display gracefully
- Model timeouts → Show timeout message, offer retry
- Ollama connection lost → Show specific error, recovery steps

## Why This Day Matters
- Streamlit bridges graph → user interaction
- Real-time streaming shows users what's happening
- Session state persistence = smooth multi-turn workflows

## 6-Hour Teaching Script

**Hour 1: Streamlit Architecture (60 min)**
- How Streamlit works: reruns on interaction
- Why session_state exists: Persist data across reruns
- Widgets: text_input, button, markdown, expander
- Lifecycle: Script runs top to bottom on every interaction

**Hour 2: Build Minimal Input (60 min)**
- Create text_input for topic
- Create button to trigger action
- Initialize session_state
- Test: Change topic, see it persist

**Hour 3: Connect to Graph.stream() (60 min)**
- When button clicked, call agent_app.stream()
- Loop through events
- Extract state updates
- Store in session_state

**Hour 4: Add Real-Time Status (60 min)**
- Create placeholder for status message
- Update as graph executes: "Researching...", "Analyzing...", "Writing..."
- Show: Users see progress
- Observe: No blank screens

**Hour 5: Format & Display Results (60 min)**
- Display research data in columns
- Display analysis in 6 sections
- Display HTML with markdown
- Add expandable sections for organization

**Hour 6: Debug Streamlit Reruns (60 min)**
- Why does state disappear? Check session_state initialization
- Why does button click not work? Check disabled state
- Why do results not update? Check event loop
- Hands-on: Fix intentional bugs

## Assessment Checkpoint
By end of Day 7, students should:
- ✓ Understand Streamlit rerun model and session_state purpose
- ✓ Build UI with input → button → graph execution
- ✓ Stream graph events into UI in real-time
- ✓ Format and display multi-part results
