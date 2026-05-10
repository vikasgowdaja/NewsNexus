# NewsNexus Architecture - Mermaid Diagram

## Complete System Architecture

```mermaid
graph TB
    subgraph UI["🎨 User Interface Layer"]
        SA["streamlit_app.py<br/>(~750 lines)<br/>UI + Session State + HTML Normalization"]
    end
    
    subgraph Core["⚙️ Orchestration Core"]
        ORK["orchestrator.py<br/>(36 lines)<br/>Single LangGraph Authority"]
    end
    
    subgraph Brain["🧠 Agent Layer"]
        AG["agents.py<br/>(~200 lines)<br/>Researcher | Analyst | Writer"]
    end
    
    subgraph Tools["🔧 Tool Layer"]
        TL["tools.py<br/>(~140 lines)<br/>RAG | Web Search | RSS Feeds"]
    end
    
    subgraph Vector["📚 Knowledge Base"]
        VS["vector_store.py<br/>(74 lines)<br/>Unified Ingestion + Retrieval"]
        ING["ingestion.py<br/>(6 lines)<br/>Wrapper"]
        RET["retrieval.py<br/>(4 lines)<br/>Wrapper"]
        CHR["Chroma DB<br/>Main: /data/chroma_db<br/>Archive: /data/archive_memory"]
    end
    
    subgraph Memory["💾 Archive Layer"]
        MS["memory_store.py<br/>(~60 lines)<br/>Long-term Newsletter Archive"]
    end
    
    SA -->|Controls| ORK
    ORK -->|Executes| AG
    AG -->|Uses| TL
    TL -->|Queries| VS
    VS -->|Reads/Writes| CHR
    ING -->|Wraps| VS
    RET -->|Wraps| VS
    CHR -->|Stores| MS
    MS -->|Saves to| CHR
    SA -->|Direct Access| ING
    SA -->|Direct Access| MS
    
    classDef uiLayer fill:#FF6B6B,stroke:#C92A2A,color:#fff,stroke-width:3px
    classDef core fill:#4ECDC4,stroke:#0B7285,color:#fff,stroke-width:3px
    classDef brain fill:#95E1D3,stroke:#38B2AC,color:#000,stroke-width:3px
    classDef tools fill:#FFE66D,stroke:#F59E0B,color:#000,stroke-width:3px
    classDef vector fill:#A8E6CF,stroke:#5DBA8F,color:#000,stroke-width:3px
    classDef memory fill:#C7CEEA,stroke:#7B68EE,color:#000,stroke-width:3px
    
    class SA uiLayer
    class ORK core
    class AG brain
    class TL tools
    class VS,ING,RET,CHR vector
    class MS memory
```

## Data Flow: User Request → Newsletter

```mermaid
graph LR
    A["👤 User Input<br/>Topic: Naruto"] --> B["normalize_topic()<br/>Check Memory"]
    B --> C["Init Orchestrator<br/>Create StateGraph"]
    C --> D["🔍 Researcher Node<br/>Execute Tools"]
    
    D --> E{Which Tools?}
    E -->|RAG| F["lookup_policy_docs<br/>Vector Search<br/>+ Keyword Boost"]
    E -->|Web| G["web_search_stub<br/>DuckDuckGo<br/>+ Fallbacks<br/>+ Wikipedia"]
    E -->|RSS| H["rss_feed_search<br/>Industry Feeds<br/>TechReview, OpenAI, etc"]
    E -->|None| I["Use Prior Knowledge"]
    
    F --> J["📊 Analyst Node<br/>6-Section Analysis"]
    G --> J
    H --> J
    I --> J
    
    J --> K["Extract Chart Data<br/>JSON from response"]
    K --> L["✍️ Writer Node<br/>Premium HTML"]
    L --> M["normalize_generated_html()<br/>Strip preface/fences"]
    M --> N["sanitize_html()<br/>Bleach + CSS Preserve"]
    N --> O["👁️ Human Review<br/>HITL Approval"]
    
    O -->|Has Feedback| P["📝 Revise via Writer<br/>Keep Topic Lock"]
    P --> Q["Compare Drafts<br/>Show Changes"]
    Q --> O
    
    O -->|Approved| R["💾 Archive to Memory<br/>Save Newsletter"]
    R --> S["✅ Finished State<br/>Download HTML/PDF"]
    
    classDef input fill:#FF6B6B,stroke:#C92A2A,color:#fff
    classDef process fill:#4ECDC4,stroke:#0B7285,color:#fff
    classDef research fill:#FFE66D,stroke:#F59E0B,color:#000
    classDef analysis fill:#A8E6CF,stroke:#5DBA8F,color:#000
    classDef html fill:#FFB6C1,stroke:#FF69B4,color:#000
    classDef hitl fill:#DDA15E,stroke:#A67C52,color:#fff
    classDef finish fill:#90EE90,stroke:#228B22,color:#000
    
    class A input
    class B,C process
    class D,E,F,G,H,I,J,K research
    class L,M,N html
    class O,P,Q hitl
    class R,S finish
```

## Feedback Cycle Detail

```mermaid
graph TD
    A["Writer Completes<br/>Graph Paused at<br/>human_approval Node"] --> B["📋 Streamlit Review Stage<br/>State Persisted:<br/>• messages<br/>• research_data<br/>• analysis_content<br/>• revision_notes"]
    
    B --> C["Display:<br/>• Plotly Chart<br/>• Draft HTML<br/>• Research Tabs<br/>• Feedback Input"]
    
    C --> D{User<br/>Decision}
    
    D -->|Empty Submit| E["✅ APPROVE"]
    D -->|With Feedback| F["🔄 REVISE"]
    
    E --> E1["save_memory topic_key<br/>Save to archive Chroma"]
    E1 --> E2["Set state: finished"]
    E2 --> E3["Show Balloons<br/>Download Buttons"]
    
    F --> F1["st.status Spinner<br/>Update State:<br/>• messages: feedback<br/>• revision_notes: feedback"]
    F1 --> F2["route_after_human<br/>Return Writer"]
    F2 --> F3["Writer Re-runs:<br/>• Reads analysis_content<br/>• Reads revision_notes<br/>• Maintains topic_lock"]
    F3 --> F4["Generate Revised HTML"]
    F4 --> F5["Compare Old vs New:<br/>Same → Warning<br/>Different → Success"]
    F5 --> F6["Spinner Closes<br/>Loop to Review"]
    F6 --> C
    
    classDef pause fill:#FF6B6B,stroke:#C92A2A,color:#fff,stroke-width:2px
    classDef review fill:#4ECDC4,stroke:#0B7285,color:#fff,stroke-width:2px
    classDef approve fill:#90EE90,stroke:#228B22,color:#000,stroke-width:2px
    classDef revise fill:#FFD700,stroke:#DAA520,color:#000,stroke-width:2px
    classDef archive fill:#9370DB,stroke:#6A5ACD,color:#fff,stroke-width:2px
    classDef finish fill:#87CEEB,stroke:#4682B4,color:#000,stroke-width:2px
    
    class A pause
    class B,C,D review
    class E,E1,E2,E3 approve
    class F,F1,F2,F3,F4,F5,F6 revise
    class E1 archive
    class E3 finish
```

## Tool Invocation Paths

```mermaid
graph TB
    REQ["Researcher Node<br/>Query: Naruto"] --> LLM["LLM with Tools<br/>Decides which to call"]
    
    LLM --> RAG["🗂️ RAG Path<br/>lookup_policy_docs"]
    LLM --> WEB["🌐 Web Path<br/>web_search_stub"]
    LLM --> RSS["📡 RSS Path<br/>rss_feed_search"]
    LLM --> NONE["⚪ No Tools<br/>Use Prior Knowledge"]
    
    RAG --> RAGA["vector_store.retrieve<br/>Chroma Similarity Search<br/>+ Keyword Boost"]
    RAGA --> RAGR["Return: doc1, doc2, doc3<br/>Formatted with sources"]
    
    WEB --> WEBA["Try DuckDuckGo lite"]
    WEBA --> WEBB["Try DuckDuckGo html"]
    WEBB --> WEBC["Try DuckDuckGo news"]
    WEBC --> WEBD["Try Wikipedia fallback"]
    WEBD --> WEBE["Try RSS fallback"]
    WEBE --> WEBR["Return: web results<br/>Or 'low coverage'"]
    
    RSS --> RSSA["Parse industry feeds:<br/>TechReview, OpenAI,<br/>Apple ML, HackerNews"]
    RSSA --> RSSB["Keyword matching"]
    RSSB --> RSSR["Return: RSS entries<br/>Or 'no matches'"]
    
    NONE --> NONER["Return: blank<br/>Model uses knowledge"]
    
    RAGR --> COMBINE["Combine Tool Responses"]
    WEBR --> COMBINE
    RSSR --> COMBINE
    NONER --> COMBINE
    
    COMBINE --> RESEARCH["research_data Array<br/>All findings compiled"]
    RESEARCH --> NEXT["↓ Pass to Analyst Node"]
    
    classDef rag fill:#FFE66D,stroke:#F59E0B,color:#000,stroke-width:2px
    classDef web fill:#FFB6C1,stroke:#FF69B4,color:#000,stroke-width:2px
    classDef rss fill:#A8E6CF,stroke:#5DBA8F,color:#000,stroke-width:2px
    classDef none fill:#D3D3D3,stroke:#808080,color:#000,stroke-width:2px
    classDef result fill:#4ECDC4,stroke:#0B7285,color:#fff,stroke-width:2px
    
    class RAG,RAGA,RAGR rag
    class WEB,WEBA,WEBB,WEBC,WEBD,WEBE,WEBR web
    class RSS,RSSA,RSSB,RSSR rss
    class NONE,NONER none
    class COMBINE,RESEARCH,NEXT result
```

## HTML Newsletter Generation Pipeline

```mermaid
graph LR
    A["Analyst Complete<br/>6-Section Analysis"] --> B["Writer Node Receives:<br/>• analysis_content<br/>• primary_topic<br/>• revision_feedback"]
    
    B --> C["LLM Contract:<br/>PRIMARY TOPIC LOCK<br/>Strict HTML Skeleton<br/>Inline CSS Only"]
    
    C --> D["Model Output<br/>Raw with preface:<br/>Here is...\n\n```html\n...\n```"]
    
    D --> E["normalize_generated_html<br/>1. Strip prose<br/>2. Remove fences<br/>3. Extract clean HTML"]
    
    E --> F["Clean HTML<br/>!DOCTYPE html\n..."]
    
    F --> G["sanitize_html<br/>1. Bleach tags<br/>2. Bleach styles<br/>3. Preserve inline CSS<br/>4. Remove script/iframe"]
    
    G --> H["Safe HTML<br/>Ready to render"]
    
    H --> I["Display in Streamlit<br/>st.components.v1.html"]
    I --> J["Download Buttons<br/>HTML | PDF"]
    
    classDef input fill:#FFE66D,stroke:#F59E0B,color:#000
    classDef prompt fill:#4ECDC4,stroke:#0B7285,color:#fff
    classDef model fill:#95E1D3,stroke:#38B2AC,color:#000
    classDef norm fill:#FFB6C1,stroke:#FF69B4,color:#000
    classDef clean fill:#A8E6CF,stroke:#5DBA8F,color:#000
    classDef safe fill:#90EE90,stroke:#228B22,color:#000
    classDef render fill:#87CEEB,stroke:#4682B4,color:#000
    
    class A,B input
    class C prompt
    class D model
    class E,F norm
    class G,H clean
    class I,J render
```

## Chroma Vector Store Organization

```mermaid
graph TB
    subgraph MAIN["Main Database (RAG)"]
        M1["data/chroma_db/"]
        M2["Collection: default"]
        M3["Purpose: Knowledge Storage"]
        M4["Use: Researcher RAG queries"]
        M5["Embedding: nomic-embed-text"]
        M6["Scale: Many documents"]
    end
    
    subgraph ARCHIVE["Archive Database (Memory)"]
        A1["data/archive_memory/"]
        A2["Collection: newsletter_archive"]
        A3["Purpose: Duplicate Detection"]
        A4["Use: Pre-request topic lookup"]
        A5["Embedding: nomic-embed-text"]
        A6["Scale: Small, curated"]
    end
    
    subgraph INGESTION["Ingestion Flow"]
        I1["PDF Upload"]
        I2["RecursiveCharacterTextSplitter<br/>chunk_size=500, overlap=50"]
        I3["OllamaEmbeddings<br/>nomic-embed-text"]
        I4["Batch Write<br/>100 chunks/batch"]
        I5["Persist to Main DB"]
    end
    
    subgraph RETRIEVAL["Retrieval Flow"]
        R1["Query: Naruto"]
        R2["Get embedding<br/>nomic-embed-text"]
        R3["Similarity search<br/>k=5"]
        R4["Keyword boost<br/>score - matches*0.05"]
        R5["Return top-k"]
        R6["Format with sources"]
    end
    
    subgraph ARCHIVE_SAVE["Archive Save Flow"]
        AS1["Approved Newsletter"]
        AS2["Create Document<br/>content + metadata"]
        AS3["Embed query<br/>topic + HTML preview"]
        AS4["Add to archive collection"]
        AS5["Persist to Archive DB"]
    end
    
    subgraph ARCHIVE_CHECK["Archive Check Flow"]
        AC1["New Request<br/>Topic: Naruto"]
        AC2["Query archive<br/>similarity_search k=1"]
        AC3["If score < 0.4<br/>Show warning<br/>Else: No prior found"]
        AC4["Inject into researcher<br/>system prompt"]
    end
    
    I1 --> I2
    I2 --> I3
    I3 --> I4
    I4 --> I5
    I5 --> MAIN
    
    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> R5
    R5 --> R6
    MAIN -.-> R2
    
    AS1 --> AS2
    AS2 --> AS3
    AS3 --> AS4
    AS4 --> AS5
    AS5 --> ARCHIVE
    
    AC1 --> AC2
    ARCHIVE -.-> AC2
    AC2 --> AC3
    AC3 --> AC4
    
    classDef main fill:#A8E6CF,stroke:#5DBA8F,color:#000,stroke-width:2px
    classDef archive fill:#C7CEEA,stroke:#7B68EE,color:#000,stroke-width:2px
    classDef ingestion fill:#FFE66D,stroke:#F59E0B,color:#000,stroke-width:1px
    classDef retrieval fill:#95E1D3,stroke:#38B2AC,color:#000,stroke-width:1px
    classDef save fill:#FFB6C1,stroke:#FF69B4,color:#000,stroke-width:1px
    classDef check fill:#DDA15E,stroke:#A67C52,color:#fff,stroke-width:1px
    
    class MAIN,M1,M2,M3,M4,M5,M6 main
    class ARCHIVE,A1,A2,A3,A4,A5,A6 archive
    class INGESTION,I1,I2,I3,I4,I5 ingestion
    class RETRIEVAL,R1,R2,R3,R4,R5,R6 retrieval
    class ARCHIVE_SAVE,AS1,AS2,AS3,AS4,AS5 save
    class ARCHIVE_CHECK,AC1,AC2,AC3,AC4 check
```

## Session State Flow

```mermaid
stateDiagram-v2
    [*] --> idle
    
    idle --> idle: PDF Upload<br/>Build Index<br/>Check Memory
    
    idle --> researching: [Click Start Agents]<br/>Initialize orchestrator
    
    researching --> researching: Stream graph events<br/>Show research_data<br/>Show chart_data<br/>Update draft preview
    
    researching --> reviewing: Graph completes<br/>Pause at human_approval
    
    reviewing --> reviewing: Show HTML draft<br/>Show chart<br/>Show research tabs<br/>User can read
    
    reviewing --> researching: [Submit Feedback]<br/>Update revision_notes<br/>Resume Writer node<br/>Show spinner
    
    reviewing --> finished: [Approve]<br/>save_memory()<br/>archive to Chroma
    
    finished --> finished: Show balloons<br/>Display final preview<br/>Download buttons
    
    finished --> idle: [New Research]<br/>Reset session state
    
    note right of idle\n      Waiting for user input\n      Can upload PDFs\n    end note
    
    note right of researching\n      LangGraph executing\n      Researcher → Analyst → Writer\n    end note
    
    note right of reviewing\n      PAUSE POINT\n      Human intervention\n      Can revise or approve\n    end note
    
    note right of finished\n      Newsletter ready\n      Can download\n      Can start new\n    end note
```

---

## Key Files Reference

| File | Purpose | Lines | Key Responsibility |
|------|---------|-------|-------------------|
| **streamlit_app.py** | UI + Session | ~750 | User interaction, HTML normalization, session state management |
| **orchestrator.py** | Graph Authority | 36 | Single LangGraph center, node routing, conditional logic |
| **agents.py** | Agent Nodes | ~200 | Researcher/Analyst/Writer behaviors, prompts, state mutations |
| **tools.py** | Tool Layer | ~140 | RAG/web/RSS tools, fallbacks, LLM tool binding |
| **vector_store.py** | Vector Access | 74 | Unified ingestion + retrieval, embedding, Chroma connection |
| **ingestion.py** | Wrapper | 6 | Backward compatibility for PDF → vector workflow |
| **retrieval.py** | Wrapper | 4 | Backward compatibility for vector → search workflow |
| **memory_store.py** | Archive | ~60 | Newsletter persistence, duplicate detection, memory search |

---

## Design Principles

✅ **Single Orchestrator** - One source of truth for workflow  
✅ **Unified Vector Store** - Centralized embedding + retrieval  
✅ **Node-Only Agents** - Clean separation of concerns  
✅ **Resilient Fallbacks** - Web search tries 5 paths before failure  
✅ **State-Driven** - No position inference, explicit state mutations  
✅ **Inline CSS Only** - Survives Bleach sanitizer  
✅ **Two Chroma DBs** - Main (RAG) + Archive (memory) separate purposes  
✅ **Visible Feedback** - User sees all revisions and changes  

---

**All 8 files working together to deliver a complete GenAI news research → analysis → newsletter pipeline with human-in-the-loop approval and long-term memory.**
