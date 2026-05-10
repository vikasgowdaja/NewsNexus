import operator
from datetime import datetime
from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

# Import our tools and LLM setup from Phase 2
from tools import get_llm_with_tools, lookup_policy_docs, web_search_stub, rss_feed_search

# --- 1. Define the State (Enhanced for Visualization) ---
# AgentState is a custom TypedDict that defines the structure of data flowing between nodes.
class AgentState(TypedDict):
    # operator.add ensures we append new messages instead of overwriting existing ones.
    messages: Annotated[List[BaseMessage], operator.add]
    research_data: List[str]
    chart_data: List[dict] # New: Stores structured data for Plotly
    analysis_content: str
    revision_notes: List[str]

# Initialize Resources
llm, llm_with_tools, tools = get_llm_with_tools()

# --- 2. Define the Nodes / Agent Personas ---

def researcher_node(state: AgentState):
    """
    Agent 1: Researcher
    Responsibility: Look up information using tools.
    """
    print("\n--- [Agent: Researcher] is gathering data ---")
    last_message = state["messages"][-1]
    
    # Force the researcher persona via system prompt
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
    
    # Invoke model
    response = llm_with_tools.invoke([sys_msg, last_message])
    
    research_findings = []
    
    # Execute Tools if requested by the LLM
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"   > Executing Tool: {tool_name}")
            
            # --- ARGUMENT CLEANING LOGIC ---
            # Extract the actual string from the dictionary
            q = tool_args.get('query')
            if isinstance(q, dict): 
                # If nested like {'value': 'search term'} or {'type': 'string', ...}
                q = q.get('value', str(q))
            
            # Fallback for Llama 3.2 schema confusion
            if not q or q == "{'type': 'string'}":
                # Check if the LLM provided more info in the args
                q = tool_args.get('__arg1', tool_args.get('input', last_message.content))
            
            # Convert to string just in case
            q = str(q)
            # -------------------------------

            if tool_name == "lookup_policy_docs":
                res = lookup_policy_docs.invoke(q)
            elif tool_name == "web_search_stub":
                res = web_search_stub.invoke(q)
            elif tool_name == "rss_feed_search":
                res = rss_feed_search.invoke(q)
            
            research_findings.append(f"Source: {tool_name}\nData: {res}")
    else:
        research_findings.append("AGENT: The researcher agent did not call any specific tools for this query. This might happen if the topic is too broad or if the model thinks it has sufficient internal knowledge.")

    print(f"   > Researcher found {len(research_findings)} items.")
    return {
        "messages": [response], 
        "research_data": research_findings
    }

def analyst_node(state: AgentState):
    """
    Agent 2: Analyst (Enhanced with Data Extraction)
    Responsibility: Identify key trends AND extract numeric data for plotting.
    """
    print("\n--- [Agent: Analyst] is identifying trends ---")
    raw_data = "\n\n".join(state["research_data"])
    
    # Note: We use a standard LLM invocation here (no tools bound)
    # because the Analyst only needs to think, not act.
    prompt = f"""You are a senior corporate intelligence analyst.

    Your job is to transform the raw research into a detailed, decision-useful analysis.

    Produce the response using these sections:
    1. Executive Summary
        - 1 concise paragraph explaining the overall story.
    2. Key Findings
        - At least 5 detailed bullet points.
        - Each point must explain what happened, why it matters, and where the evidence came from.
    3. Trend Analysis
        - Explain patterns, shifts, comparisons, risks, or opportunities found in the data.
    4. Source-backed Evidence
        - Quote or reference important facts from the raw data.
    5. Implications
        - Explain what this means for a business reader.
    6. DATA VIZ EXTRACTION
        - Look for REAL numeric trends such as percentages, market sizes, counts, growth rates, or years.
        - If you find numeric data, extract it into a JSON block like this:
        ```json
        [{{ "label": "2024", "value": 50 }}, {{ "label": "2025", "value": 75 }}]
        ```

    CRITICAL RULES:
    - Be detailed, specific, and evidence-driven.
    - Do not write only 3 short trends.
    - Do not invent facts, figures, or citations.
    - Treat retrieval diagnostics (e.g., 'HTTP 403', 'no matching live web results', backend/debug messages) as system telemetry, NOT topic facts.
    - Do NOT conclude "the topic has low coverage" solely from tool outages or blocked endpoints.
    - If external retrieval is weak, explicitly say: "external retrieval was limited in this run" and prioritize any valid internal/RSS/entity facts.
    - If evidence is weak, explicitly say what is uncertain.
    - If the raw data is empty or insufficient, DO NOT make up hypothetical numbers. Only extract data that is EXPLICITLY present.

    RAW DATA:
    {raw_data}
    """
    
    print(f"   > Analyst node invoking base LLM with {len(raw_data)} chars of raw data...")
    response = llm.invoke(prompt)
    print(f"   > Analyst response received.")
    content = response.content
    
    # Extract JSON if present for Plotly
    chart_data = []
    import json
    import re
    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        try:
            chart_data = json.loads(json_match.group(1))
        except:
            pass
            
    return {"messages": [response], "chart_data": chart_data, "analysis_content": content}

def writer_node(state: AgentState):
    """
    Agent 3: Writer (Enhanced for Citations)
    Responsibility: Format analysis into HTML while preserving deep links.
    """
    print("\n--- [Agent: Writer] is formatting the newsletter ---")
    # Always prefer persisted analyst output so HITL feedback does not overwrite topic context.
    analyst_insight = state.get("analysis_content", "")
    if not analyst_insight:
        analyst_insight = state["messages"][-1].content

    primary_topic = "the user's requested topic"
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            candidate = (msg.content or "").strip()
            if candidate:
                primary_topic = candidate
                break

    revision_feedback = ""
    notes = state.get("revision_notes", [])
    if notes:
        revision_feedback = str(notes[-1]).strip()
    elif state["messages"] and isinstance(state["messages"][-1], HumanMessage):
        revision_feedback = state["messages"][-1].content.strip()
    
    prompt = f"""You are a senior editorial writer for a corporate intelligence platform.

    Convert the analysis into a polished, premium HTML newsletter report.

    The HTML must include these sections:
    - Title
    - Executive Summary
    - Key Findings
    - Detailed Analysis
    - Business Implications
    - Source Highlights
    - Conclusion

    WRITING RULES:
    - PRIMARY TOPIC LOCK: Keep the report centered on "{primary_topic}".
    - Do not switch to a generic or unrelated domain unless the analyst evidence explicitly supports it.
    - Treat revision feedback as style/edit instructions, not as a topic replacement.
    - Make it detailed, not minimal.
    - Use professional but readable language.
    - Expand short bullets into meaningful paragraphs where useful.
    - Preserve all links provided in the analysis (e.g., [Title](URL)).
    - Convert those links into clickable <a> tags in the HTML.
        - Use semantic HTML such as <article>, <section>, <h1>, <h2>, <h3>, <p>, <ul>, and <li>.
    - Do NOT include raw CSS, <style> tags, or stylesheet text like 'body {{ ... }}'.
        - Apply visual styling using INLINE style attributes only (no <style> block).
        - Output only clean semantic HTML content.
    - Keep the report clean and presentation-ready.
    - Do not fabricate citations or numbers.

        VISUAL DESIGN CONTRACT (MANDATORY):
        - Wrap everything in one <article> with inline styles for:
            background: light gradient, max-width layout, center alignment, padding, rounded corners.
        - Build a hero header section with:
            <h1> title, short subtitle paragraph, and a small metadata row (topic/date/confidence note).
        - Every major section must look like a card:
            light background, border, padding, border-radius, margin-bottom.
        - For Key Findings and Source Highlights:
            use <ul>/<li> with generous spacing and subtle separators.
        - For numbers or trend points:
            present 2-4 compact "insight chips" using <div>/<span> with inline badges.
        - Add a professional typography system via inline styles:
            clear heading hierarchy, improved line-height, readable paragraph width.
        - Preserve all source links as clickable <a> tags with visible link styling.
        - End with a footer note block highlighting limitations/uncertainties when evidence is weak.
        - Ensure the final HTML is visually rich in Streamlit's rendered component without external CSS.

        OUTPUT TEMPLATE CONTRACT (STRICT):
        - Follow this exact section order and keep the same outer structure.
        - You may improve text content, but do not remove required sections.
        - Return only HTML, no markdown fences.

        REQUIRED HTML SKELETON:
        <article style="max-width: 980px; margin: 24px auto; padding: 28px; border-radius: 18px; background: linear-gradient(180deg, #f8fbff 0%, #f3f7fc 100%); border: 1px solid #dbe7f3; color: #0f172a; font-family: 'Segoe UI', Tahoma, sans-serif; line-height: 1.65;">
            <header style="padding: 20px; border-radius: 14px; background: #eaf2fb; border: 1px solid #d0e1f2; margin-bottom: 18px;">
                <h1 style="margin: 0 0 8px 0; font-size: 30px; color: #0b3b67;">{{Title}}</h1>
                <p style="margin: 0 0 10px 0; color: #334155; font-size: 15px;">{{Subtitle}}</p>
                <div style="font-size: 13px; color: #475569;">
                    <span style="display: inline-block; margin-right: 12px;"><strong>Topic:</strong> {{PrimaryTopic}}</span>
                    <span style="display: inline-block; margin-right: 12px;"><strong>Date:</strong> {{Today}}</span>
                    <span style="display: inline-block;"><strong>Evidence Status:</strong> {{EvidenceNote}}</span>
                </div>
            </header>

            <section style="background: #ffffff; border: 1px solid #d9e4ef; border-radius: 14px; padding: 18px; margin-bottom: 14px;">
                <h2 style="margin-top: 0; color: #0b3b67;">Executive Summary</h2>
                <p>{{ExecutiveSummary}}</p>
            </section>

            <section style="background: #ffffff; border: 1px solid #d9e4ef; border-radius: 14px; padding: 18px; margin-bottom: 14px;">
                <h2 style="margin-top: 0; color: #0b3b67;">Key Findings</h2>
                <ul style="padding-left: 20px; margin: 0;">{{KeyFindingsList}}</ul>
            </section>

            <section style="background: #ffffff; border: 1px solid #d9e4ef; border-radius: 14px; padding: 18px; margin-bottom: 14px;">
                <h2 style="margin-top: 0; color: #0b3b67;">Detailed Analysis</h2>
                <p>{{DetailedAnalysis}}</p>
            </section>

            <section style="background: #ffffff; border: 1px solid #d9e4ef; border-radius: 14px; padding: 18px; margin-bottom: 14px;">
                <h2 style="margin-top: 0; color: #0b3b67;">Business Implications</h2>
                <p>{{BusinessImplications}}</p>
            </section>

            <section style="background: #ffffff; border: 1px solid #d9e4ef; border-radius: 14px; padding: 18px; margin-bottom: 14px;">
                <h2 style="margin-top: 0; color: #0b3b67;">Source Highlights</h2>
                <ul style="padding-left: 20px; margin: 0;">{{SourceHighlightsListWithLinks}}</ul>
            </section>

            <section style="background: #ffffff; border: 1px solid #d9e4ef; border-radius: 14px; padding: 18px; margin-bottom: 14px;">
                <h2 style="margin-top: 0; color: #0b3b67;">Conclusion</h2>
                <p>{{Conclusion}}</p>
            </section>

            <footer style="margin-top: 10px; padding: 14px; border-radius: 12px; background: #fff7ed; border: 1px solid #fed7aa; color: #7c2d12; font-size: 13px;">
                <strong>Evidence & Limitations:</strong> {{LimitationsNote}}
            </footer>
        </article>

    REVISION FEEDBACK (apply if present, otherwise ignore):
    {revision_feedback}

    TRENDS & ANALYSIS:
    {analyst_insight}
    """
    
    print(f"   > Writer node invoking base LLM with {len(analyst_insight)} chars of insight...")
    response = llm.invoke(prompt)
    print(f"   > Writer response received.")
    return {"messages": [response]}
