import streamlit as st
import os
import time
from datetime import datetime
import re
import bleach
from bleach.css_sanitizer import CSSSanitizer

# --- Import our Backend Logic ---
# We assume these files exist from previous steps
from ingestion import ingest_documents
from tools import get_llm_with_tools, lookup_policy_docs, web_search_stub
from orchestrator import app as agent_app
from memory_store import MemoryStore
from langchain_core.messages import HumanMessage

# --- Paths Configuration ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw_pdfs")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "chroma_db")

# --- Page Config ---
st.set_page_config(page_title="NewsNexus AI", page_icon="📰", layout="wide")

# --- Premium UI Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

    :root {
        --nn-bg-1: #f6f8fc;
        --nn-bg-2: #eef3ff;
        --nn-bg-3: #f9fbf2;
        --nn-ink-1: #0f172a;
        --nn-ink-2: #334155;
        --nn-muted: #64748b;
        --nn-primary: #0a4e9b;
        --nn-primary-soft: #dbeafe;
        --nn-accent: #0f766e;
        --nn-card: rgba(255, 255, 255, 0.86);
        --nn-card-border: rgba(148, 163, 184, 0.24);
        --nn-shadow: 0 18px 42px rgba(15, 23, 42, 0.08);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 8%, rgba(10, 78, 155, 0.1), transparent 33%),
            radial-gradient(circle at 88% 14%, rgba(15, 118, 110, 0.11), transparent 34%),
            linear-gradient(160deg, var(--nn-bg-1) 0%, var(--nn-bg-2) 50%, var(--nn-bg-3) 100%);
        color: var(--nn-ink-1);
    }

    .stApp, .stMarkdown, .stTextInput label, .stButton button, .stSubheader, .stTitle {
        font-family: "Manrope", "Segoe UI", sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(7, 32, 64, 0.95) 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    .nn-side-title {
        font-size: 1.18rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.02em;
        margin-bottom: 0.35rem;
    }

    .nn-side-sub {
        font-size: 0.84rem;
        color: #94a3b8;
        margin-bottom: 0.6rem;
    }

    .nn-hero {
        background: linear-gradient(127deg, rgba(10, 78, 155, 0.96) 0%, rgba(15, 118, 110, 0.88) 100%);
        border: 1px solid rgba(255, 255, 255, 0.24);
        border-radius: 22px;
        box-shadow: var(--nn-shadow);
        padding: 1.4rem 1.45rem 1.2rem 1.45rem;
        margin: 0.25rem 0 0.9rem 0;
        color: #f8fafc;
        animation: nnFadeSlide 0.65s ease-out;
    }

    .nn-hero h1 {
        margin: 0;
        font-size: 2rem;
        letter-spacing: -0.025em;
        line-height: 1.16;
        font-weight: 800;
        color: #ffffff;
    }

    .nn-hero p {
        margin: 0.35rem 0 0.8rem 0;
        color: rgba(241, 245, 249, 0.96);
        font-size: 1rem;
    }

    .nn-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }

    .nn-chip {
        border: 1px solid rgba(255, 255, 255, 0.35);
        background: rgba(255, 255, 255, 0.12);
        border-radius: 999px;
        padding: 0.32rem 0.72rem;
        font-size: 0.8rem;
        letter-spacing: 0.02em;
        font-weight: 700;
        color: #e2e8f0;
        backdrop-filter: blur(5px);
    }

    .nn-section-title {
        margin-top: 0.25rem;
        color: var(--nn-ink-1);
        font-size: 1.18rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }

    .nn-section-sub {
        color: var(--nn-ink-2);
        margin-top: -0.12rem;
        margin-bottom: 0.55rem;
        font-size: 0.92rem;
    }

    [data-testid="stTextInput"] > div > div > input {
        border-radius: 14px;
        border: 1px solid var(--nn-card-border);
        background: var(--nn-card);
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
        color: var(--nn-ink-1);
        font-size: 0.96rem;
        padding-top: 0.75rem;
        padding-bottom: 0.75rem;
    }

    [data-testid="stTextInput"] > div > div > input:focus {
        border-color: rgba(10, 78, 155, 0.55);
        box-shadow: 0 0 0 0.16rem rgba(10, 78, 155, 0.16), 0 10px 26px rgba(15, 23, 42, 0.08);
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(10, 78, 155, 0.35);
        background: linear-gradient(180deg, #0f62ba 0%, #0a4e9b 100%);
        color: #ffffff;
        font-weight: 700;
        letter-spacing: 0.01em;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        box-shadow: 0 11px 24px rgba(10, 78, 155, 0.24);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 30px rgba(10, 78, 155, 0.3);
    }

    [data-testid="stStatusWidget"],
    [data-testid="stAlert"],
    [data-testid="stExpander"] {
        border-radius: 14px;
    }

    .nn-success {
        background: linear-gradient(120deg, rgba(16, 185, 129, 0.17), rgba(20, 184, 166, 0.12));
        border: 1px solid rgba(15, 118, 110, 0.28);
        border-radius: 14px;
        color: #115e59;
        font-size: 1rem;
        font-weight: 700;
        padding: 0.85rem 1rem;
    }

    code, pre {
        font-family: "IBM Plex Mono", Consolas, monospace !important;
    }

    @keyframes nnFadeSlide {
        from {
            opacity: 0;
            transform: translateY(6px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "research_data" not in st.session_state:
    st.session_state.research_data = []
if "chart_data" not in st.session_state:
    st.session_state.chart_data = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"session_{int(time.time())}"
if "current_step" not in st.session_state:
    st.session_state.current_step = "idle" # idle, researching, reviewing, finished
if "draft_content" not in st.session_state:
    st.session_state.draft_content = ""
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "interpreted_topic" not in st.session_state:
    st.session_state.interpreted_topic = ""
if "revision_notes" not in st.session_state:
    st.session_state.revision_notes = []
if "feedback_status_kind" not in st.session_state:
    st.session_state.feedback_status_kind = ""
if "feedback_status_message" not in st.session_state:
    st.session_state.feedback_status_message = ""


def normalize_topic(raw_topic: str) -> str:
    """Normalize user input dynamically without hardcoded topic mappings."""
    cleaned = raw_topic.strip()
    cleaned = " ".join(cleaned.split())
    return cleaned

# --- HTML Sanitizer ---
_ALLOWED_TAGS = [
    "a", "abbr", "b", "blockquote", "br", "caption", "cite", "code",
    "col", "colgroup", "dd", "del", "dfn", "div", "dl", "dt", "em",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "ins", "kbd",
    "li", "mark", "ol", "p", "pre", "q", "s", "samp", "section",
    "small", "span", "strong", "sub", "sup", "table", "tbody", "td",
    "tfoot", "th", "thead", "tr", "u", "ul",
]
_ALLOWED_ATTRS = {
    "*": ["class", "style", "id"],
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "width", "height"],
}

_CSS_SANITIZER = CSSSanitizer(
    allowed_css_properties=[
        "background", "background-color", "background-image",
        "color", "font-family", "font-size", "font-weight", "font-style",
        "line-height", "letter-spacing", "text-align", "text-decoration",
        "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
        "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
        "border", "border-top", "border-right", "border-bottom", "border-left",
        "border-radius", "display", "max-width", "width", "height",
        "box-shadow", "opacity",
    ]
)


def normalize_generated_html(raw_output: str) -> str:
    """Strip LLM wrappers (e.g. prose, code fences) and keep only HTML payload."""
    text = (raw_output or "").strip()
    if not text:
        return text

    # Remove markdown fences if present.
    text = re.sub(r"^```(?:html)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # If the model prepends prose, cut to first meaningful HTML tag.
    first_html = re.search(r"<(article|div|section|header|h1|h2|p|ul|ol)\b", text, flags=re.IGNORECASE)
    if first_html:
        text = text[first_html.start():]

    # If there is trailing fence/prose after HTML, trim at the last closing tag.
    last_close = max(text.rfind("</article>"), text.rfind("</div>"), text.rfind("</section>"))
    if last_close != -1:
        # Include the closing tag length for the matched case.
        if text.rfind("</article>") == last_close:
            text = text[: last_close + len("</article>")]
        elif text.rfind("</section>") == last_close:
            text = text[: last_close + len("</section>")]
        else:
            text = text[: last_close + len("</div>")]

    return text.strip()

def sanitize_html(html: str) -> str:
    """Strip unsafe tags/attributes (e.g. <script>) before rendering."""
    normalized = normalize_generated_html(html)
    return bleach.clean(
        normalized,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRS,
        css_sanitizer=_CSS_SANITIZER,
        strip=True,
    )

# --- PDF Export Utility ---
def export_as_pdf(html_content):
    from io import BytesIO
    from xhtml2pdf import pisa
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        return None
    return pdf_buffer.getvalue()

# --- Sidebar: Data Management ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2593/2593240.png", width=80)
    st.markdown('<div class="nn-side-title">NewsNexus Control Deck</div>', unsafe_allow_html=True)
    st.markdown('<div class="nn-side-sub">AI research operations and knowledge orchestration</div>', unsafe_allow_html=True)
    st.divider()
    
    st.subheader("📂 Knowledge Base")
    
    # 1. Show existing files
    existing_pdfs = []
    if os.path.exists(DATA_PATH):
        existing_pdfs = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
    
    if existing_pdfs:
        with st.expander(f"Documents in Library ({len(existing_pdfs)})", expanded=False):
            for pdf in existing_pdfs:
                st.write(f"📄 {pdf}")
    else:
        st.caption("No documents in library yet.")

    st.divider()
    
    # 2. Upload new files
    uploaded_files = st.file_uploader("Add New Reports (PDF)", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_path = os.path.join(DATA_PATH, uploaded_file.name)
            os.makedirs(DATA_PATH, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} files!")
        st.rerun() # Refresh to show in list
        
    if st.button("🧠 Build/Update Vector Index"):
        if not existing_pdfs:
            st.warning("Please upload at least one PDF first.")
        else:
            with st.spinner("Processing Library..."):
                try:
                    pages, chunks = ingest_documents() 
                    st.success(f"Success! Processed {pages} pages into {chunks} chunks.")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()
    # Check system status
    db_ready = os.path.exists(DB_PATH) and os.listdir(DB_PATH)
    status_msg = "✅ Database: ACTIVE" if db_ready else "⚠️ Database: MISSING"
    st.info(f"System Status: {status_msg}")
    st.caption(f"Mode: {'Hybrid (PDF+Web)' if existing_pdfs else 'Web Search Only'}")
    st.caption("LLM: Llama 3.2 (768-dim Ollama)")

# --- Main Interface ---

ui_mode_label = 'Hybrid (PDF + Web)' if existing_pdfs else 'Web Search Only'
db_status_label = 'Knowledge Base Active' if db_ready else 'Knowledge Base Missing'
st.markdown(
    f'''<div class="nn-hero">
        <h1>NewsNexus Corporate Intelligence Studio</h1>
        <p>Multi-agent research, analysis, and writing with professional review and memory-backed continuity.</p>
        <div class="nn-chip-row">
            <span class="nn-chip">{ui_mode_label}</span>
            <span class="nn-chip">{db_status_label}</span>
            <span class="nn-chip">Model: Llama 3.2</span>
        </div>
    </div>''',
    unsafe_allow_html=True,
)
st.divider()

# Input Area
st.markdown('<div class="nn-section-title">Research Brief</div>', unsafe_allow_html=True)
st.markdown('<div class="nn-section-sub">Define the scope and launch the agent pipeline.</div>', unsafe_allow_html=True)
topic = st.text_input("Enter Research Topic:", placeholder="e.g., 'Impact of Generative AI on Banking sector 2024'")

if topic.strip():
    interpreted_topic = normalize_topic(topic)
    if interpreted_topic != topic.strip():
        st.info(f"Interpreted topic: **{interpreted_topic}**")

if st.button("🚀 Start Agents", disabled=st.session_state.current_step != "idle") and topic:
    # --- SMART INITIALIZATION LOGIC ---
    db_exists = os.path.exists(DB_PATH) and os.listdir(DB_PATH)
    raw_pdfs_exist = os.path.exists(DATA_PATH) and any(f.endswith(".pdf") for f in os.listdir(DATA_PATH))
    
    if db_exists:
        st.success("📂 Using existing Knowledge Base...")
    elif raw_pdfs_exist:
        with st.info("🔍 Indexing your library for the first time..."):
            try:
                pages, chunks = ingest_documents()
                st.success(f"Library Indexed! ({pages} pages, {chunks} chunks)")
            except Exception as e:
                st.error(f"Auto-index failed: {e}")
                st.stop()
    else:
        st.warning("🌐 No PDFs found. Proceeding with Web Search only.")
    # -------------------------

    interpreted_topic = normalize_topic(topic)
    st.session_state.topic = topic
    st.session_state.interpreted_topic = interpreted_topic
    st.session_state.current_step = "researching"
    st.session_state.messages = [HumanMessage(content=interpreted_topic)]
    st.session_state.research_data = []
    
    # Initialize Memory Store
    try:
        mem_store = MemoryStore()
        with st.spinner("Checking historical archives..."):
            past_memory = mem_store.check_memory(interpreted_topic)
    except Exception as e:
        st.error(f"Memory Store failed: {e}")
        st.stop()
    
    if "WARNING" in past_memory:
        st.warning(past_memory)

# --- Visualization Logic ---

if st.session_state.current_step == "researching":
    
    # Create containers for real-time updates
    col1, col2, col3 = st.columns(3)
    with col1:
        research_status = st.status("🕵️ Researcher Agent", expanded=True)
    with col2:
        analyst_status = st.status("🧠 Analyst Agent", state="running", expanded=False)
    with col3:
        writer_status = st.status("✍️ Writer Agent", state="running", expanded=False)

    # Run the Graph Stream
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    inputs = {
        "messages": st.session_state.messages,
        "research_data": [],
        "chart_data": [],
        "analysis_content": "",
        "revision_notes": [],
    }
    
    try:
        print(f"\n[Streamlit] Starting graph for topic: '{st.session_state.topic}'")
        for event in agent_app.stream(inputs, config):
            if "Researcher" in event:
                research_output = event["Researcher"]
                st.session_state.research_data = research_output.get("research_data", [])
                with research_status:
                    for item in st.session_state.research_data:
                        st.markdown(f"--- \n{item}")
                research_status.update(label=f"Researcher: Found {len(st.session_state.research_data)} items", state="complete", expanded=False)
                analyst_status.update(expanded=True)

            if "Analyst" in event:
                analyst_output = event["Analyst"]
                st.session_state.chart_data = analyst_output.get("chart_data", [])
                with analyst_status:
                    st.write("Identified Trends & Extracted Data:")
                    if st.session_state.chart_data:
                        st.json(st.session_state.chart_data)
                    else:
                        st.write("No numeric trends found.")
                analyst_status.update(label="Analyst: Complete", state="complete", expanded=False)
                writer_status.update(expanded=True)

            if "Writer" in event:
                writer_output = event["Writer"]
                st.session_state.draft_content = normalize_generated_html(writer_output["messages"][-1].content)
                with writer_status:
                    st.success("Draft Generated!")
                    st.code(st.session_state.draft_content[:200] + "...", language="html")
                writer_status.update(label="Writer: Complete", state="complete")
        
        st.session_state.current_step = "reviewing"
        st.rerun()
    except Exception as e:
        st.error(f"Execution Error: {e}")


# --- Review Stage (Human-in-the-Loop) ---
if st.session_state.current_step == "reviewing":
    st.markdown('<div class="nn-section-title">Draft Review Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="nn-section-sub">Inspect findings, validate quality, and decide approval or refinement.</div>', unsafe_allow_html=True)

    if st.session_state.feedback_status_message:
        if st.session_state.feedback_status_kind == "success":
            st.success(st.session_state.feedback_status_message)
        elif st.session_state.feedback_status_kind == "warning":
            st.warning(st.session_state.feedback_status_message)
        elif st.session_state.feedback_status_kind == "error":
            st.error(st.session_state.feedback_status_message)
        else:
            st.info(st.session_state.feedback_status_message)
    
    # Interactive Visualization
    if st.session_state.chart_data:
        import plotly.express as px
        import pandas as pd
        st.markdown("#### 📊 Extracted Trend Analysis")
        df = pd.DataFrame(st.session_state.chart_data)
        fig = px.bar(df, x="label", y="value", title="Data Visualization", color="label")
        st.plotly_chart(fig, use_container_width=True)

    # Tabs for different views
    tab1, tab2 = st.tabs(["📄 Newsletter Draft", "🔍 Raw Research Log"])
    
    with tab1:
        # Display HTML Preview
        with st.expander("View Rendered HTML", expanded=True):
            st.components.v1.html(sanitize_html(st.session_state.draft_content), height=600, scrolling=True)
            
    with tab2:
        st.markdown("### 🕵️ Raw Research Findings")
        if st.session_state.research_data:
            for i, data in enumerate(st.session_state.research_data):
                st.info(f"**Finding {i+1}:**\n\n{data}")
        else:
            st.warning("No raw research data found. The agents might have relied on internal knowledge.")
    
    col_a, col_b = st.columns([3, 1])
    
    with col_a:
        feedback = st.text_input("Feedback (Leave empty to approve):", placeholder="e.g., 'Make the tone more formal'")
    
    with col_b:
        st.write("") 
        st.write("") 
        if st.button("Submit Decision"):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            if feedback:
                previous_draft = st.session_state.draft_content
                st.session_state.revision_notes.append(feedback)
                st.session_state.feedback_status_kind = "info"
                st.session_state.feedback_status_message = "Feedback received. Starting revision cycle..."

                try:
                    with st.status("🔄 Applying feedback revision...", expanded=True) as feedback_status:
                        feedback_status.write("Routing feedback to human approval node...")
                        agent_app.update_state(
                            config,
                            {"messages": [HumanMessage(content=feedback)], "revision_notes": [feedback]},
                            as_node="human_approval",
                        )

                        feedback_status.write("Running writer revision...")
                        for event in agent_app.stream(None, config):
                            if "Writer" in event:
                                feedback_status.write("Writer produced a revised draft.")

                        state = agent_app.get_state(config)
                        revised_draft = normalize_generated_html(state.values['messages'][-1].content)
                        st.session_state.draft_content = revised_draft
                        st.session_state.chart_data = state.values.get('chart_data', [])

                        if revised_draft.strip() == previous_draft.strip():
                            st.session_state.feedback_status_kind = "warning"
                            st.session_state.feedback_status_message = (
                                "Feedback cycle completed, but the draft is unchanged. "
                                "Try more explicit instructions (for example: 'Rewrite Executive Summary in formal tone and add 3 bullet risks')."
                            )
                            feedback_status.update(label="⚠️ Feedback cycle completed (no visible content change)", state="complete")
                        else:
                            st.session_state.feedback_status_kind = "success"
                            st.session_state.feedback_status_message = "Feedback cycle completed and draft updated successfully."
                            feedback_status.update(label="✅ Feedback cycle completed and applied", state="complete")
                except Exception as e:
                    st.session_state.feedback_status_kind = "error"
                    st.session_state.feedback_status_message = f"Feedback cycle failed: {e}"

                st.rerun()
            else:
                st.session_state.current_step = "finished"
                mem_store = MemoryStore()
                topic_key = st.session_state.messages[0].content 
                mem_store.save_memory(topic_key, st.session_state.draft_content)
                st.rerun()

# --- Final Stage ---
if st.session_state.current_step == "finished":
    st.balloons()
    st.markdown('<div class="nn-success">✅ Newsletter approved and archived successfully.</div>', unsafe_allow_html=True)
    
    # Export Options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 Download HTML",
            data=st.session_state.draft_content,
            file_name=f"newsletter_{int(time.time())}.html",
            mime="text/html"
        )
    
    with col2:
        pdf_data = export_as_pdf(st.session_state.draft_content)
        if pdf_data:
            st.download_button(
                label="📁 Download PDF",
                data=pdf_data,
                file_name=f"newsletter_{int(time.time())}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("PDF Export failed.")

    with col3:
        if st.button("🔄 New Research"):
            st.session_state.current_step = "idle"
            st.rerun()

    st.markdown("### Final Output Preview")
    st.components.v1.html(sanitize_html(st.session_state.draft_content), height=800, scrolling=True)