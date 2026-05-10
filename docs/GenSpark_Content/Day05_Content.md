# Day 5 Content - RAG Pipeline

## Learning Objectives
- Understand hallucination problem and RAG solution
- Design retrieval-augmented workflows
- Implement evidence formatting and citation
- Compare grounded vs ungrounded LLM outputs

## Skeleton 5 (Day 5 - RAG Core)
```
User Query
 → Researcher Node
 → lookup_policy_docs Tool
 → retrieve_documents
 → Chroma top-k chunks
 → LLM grounded synthesis
```

## The 4 Stages of Day 5
1. **Stage A:** RAG motivation and trust model
2. **Stage B:** Retrieval tool implementation
3. **Stage C:** Evidence formatting and citation path
4. **Stage D:** Compare grounded vs ungrounded outputs

## The Hallucination Problem
- **LLM alone:** "What does the Climate Policy Act say?" → Model makes up plausible-sounding answer
- **LLM + RAG:** "What does the Climate Policy Act say?" → Model reads actual policy, extracts facts
- **RAG = Retrieval-Augmented Generation = facts first, then synthesize**

## RAG Trust Model
1. **Source of truth:** Internal PDF documents (policies, reports)
2. **Retrieval step:** Find relevant documents matching user query
3. **Synthesis step:** LLM reads retrieved docs and answers based on them
4. **Citation step:** Report where each fact came from

## Complete RAG Flow (Visual Pipeline)
- User Query: "What is the climate policy?"
- → Retrieve Step: Find 3 most relevant PDFs (semantic search from Day 4)
- → LLM Step: "Here's what the policy says: [from retrieved docs]"
- → Citation Step: "Source: page 2 of Climate_Policy.pdf"

## Critical Code Blocks

### Block 1: RAG Tool Contract (src/tools.py:9)
```python
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
        results.append(f"Content: {doc.page_content}\nSource Link: [{basename}](file:///{safe_source_path})")
    
    return "\n\n".join(results)
```
- **Teaching Point:** Notice the tool ALWAYS returns source link, never hides provenance

### Block 2: Inside lookup_policy_docs
- **Input:** User query as string
- **Process:** Call retrieve_documents() (from Day 4) to find top 3 semantically similar chunks
- **Output:** Chunk content + source file name + file path
- **Contract:** Always returns source, never synthesizes facts

### Block 3: Tool Invocation from Agent (src/agents.py:50)
```python
# Researcher node calls tools:
response = llm_with_tools.invoke([system_message, user_message])
# Model decides to call lookup_policy_docs, web_search_stub, or rss_feed_search
```

## RAG vs No-RAG Comparison
- **NO RAG:** "What's the climate policy?" → Generic 3-point summary (likely hallucinated)
- **RAG:** "What's the climate policy?" → 6-section analysis grounded in actual policy docs

## Edge Cases in RAG
- No documents found: Tool returns "No relevant docs found" (honest failure)
- Weak match: Top result has low relevance score → Still returned but analyst notes low confidence
- Ambiguous query: Multiple docs retrieved → Analyst synthesizes common themes

## Groundedness Rubric
- ✓ Every claim has cited source in retrieved documents
- ✓ No facts introduced that aren't in the sources
- ✓ Direct quotes marked with quotation marks
- ✓ Synthesis is stated as "derived from" not "is stated in"

## RAG Quality Metrics
- **Retrieval recall:** Did we fetch the document that contains the answer?
- **Retrieval precision:** Did we fetch irrelevant documents?
- **LLM grounding:** Did model stay true to retrieved docs?

## Why This Day Matters
- Skeleton 5 (RAG Core): Retrieved docs = source of truth
- RAG = enterprise-grade vs generic LLM responses
- This is the foundation of Days 6-10 agent orchestration

## 6-Hour Teaching Script

**Hour 1: Hallucination Discussion (60 min)**
- Show business examples: medical, finance, legal domains
- Why hallucination happens in LLMs
- Cost of hallucination: Wrong medical advice, fake citations, fabricated policies
- How RAG prevents it: Use retrieved documents as source of truth

**Hour 2: Walk Through lookup_policy_docs (60 min)**
- Line-by-line code walkthrough
- Input: User query
- Process: retrieve_documents() call
- Output: Sources + content
- Why always return source: Auditable, traceable

**Hour 3: Trace Retrieval into Response (60 min)**
- Researcher calls lookup_policy_docs
- Model sees retrieved docs
- Model uses retrieved docs to construct answer
- Analyst reads model response
- Analyst includes evidence sections with sources

**Hour 4: Run Same Query With/Without RAG (60 min)**
- Query 1: Without RAG → Thin generic answer (likely hallucinated)
- Query 2: With RAG → 6-section detailed answer grounded in docs
- Compare side-by-side
- Show: Sources appear in RAG output

**Hour 5: Analyze Edge Cases (60 min)**
- No documents found: See "No relevant docs found" message
- Weak matches: See low confidence scores in analyst output
- Contradictions: Multiple docs say different things → analyst notes contradiction
- Hands-on: Craft queries that trigger edge cases

**Hour 6: Build Groundedness Rubric (60 min)**
- Create checklist: Every claim has source?
- Fact-check 5 real outputs using rubric
- Score 1-5 for groundedness
- Identify patterns in weak answers (missing sources, synthesis beyond docs)

## Assessment Checkpoint
By end of Day 5, students should:
- ✓ Draw full RAG execution path and explain why each step exists
- ✓ Identify hallucinations vs grounded facts
- ✓ Score outputs using groundedness rubric
