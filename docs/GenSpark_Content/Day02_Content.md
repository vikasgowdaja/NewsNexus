# Day 2 Content - Prompt Engineering

## Learning Objectives
- Design role-specific prompts with measurable output contracts
- Understand multi-role prompt composition
- Implement query normalization guardrails
- Evaluate prompt quality

## Skeleton 2 (Day 2 - Prompt Control Layer)
```
NewsNexus/
└── src/
    ├── agents.py        # Researcher / Analyst / Writer prompts
    └── streamlit_app.py # Input normalization
```

## The 4 Stages of Day 2
1. **Stage A:** Prompt anatomy (role, objective, constraints, output schema)
2. **Stage B:** Multi-role prompt design
3. **Stage C:** Robust query interpretation (typo normalization)
4. **Stage D:** Prompt quality evaluation

## Prompt Anatomy (4 Components)
1. **Role:** What hat does the model wear? ("You are a data gatherer")
2. **Objective:** What is the model's single job? ("Find facts, don't analyze")
3. **Constraints:** What must/must-not happen? ("Correct typos before searching")
4. **Output Schema:** What exact format? ("Return facts + sources")

## Critical Code Blocks

### Block 1: Researcher Role (src/agents.py:31)
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
- **Teaching Point:** Notice the typo-correction rule built into the prompt itself

### Block 2: Analyst Role (src/agents.py:100 - Summary)
Expected output structure:
```python
# 6 SECTIONS REQUIRED:
1. Executive Summary
2. Key Findings
3. Trend Analysis
4. Evidence (with source citations)
5. Implications
6. Visualization metadata (JSON for Plotly)
```

### Block 3: Writer Role (src/agents.py:162 - Summary)
```python
# Writer prompt ensures output is detailed HTML with semantic tags
# Input: Previous agent messages + analysis sections
# Output: <article><h1> ... <section> ... </section> ... </article>
```

### Block 4: Query Normalization (src/streamlit_app.py:221)
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
- **Use Case:** User types "nauruto" → Normalized to "Naruto" → Passed to agents
- **UI Feedback:** "Interpreted topic: Naruto" shown before pipeline starts

## Multi-Role Workflow
- **Researcher Output:** Raw facts + sources
- → **Analyst Output:** Structured 6-section analysis with evidence
- → **Writer Output:** Formatted HTML article

## Prompt Quality Evaluation Rubric
- ✓ Is the role definition clear and unmistakable?
- ✓ Is output format specified (JSON, HTML, structured text)?
- ✓ Are constraints (don't do X) explicit?
- ✓ Do examples show edge cases?
- ✓ Does it prevent common failure modes (hallucination, vagueness)?

## Why This Day Matters
- Better prompts = less hallucination, better structure, fewer revisions
- Role separation = testable + maintainable
- Typo correction = user intent normalization (practical guardrail)

## 6-Hour Teaching Script

**Hour 1: Prompt Engineering Theory (60 min)**
- Show weak prompt: "Write about this topic"
- Show strong prompt: Full Researcher prompt with constraints
- Discuss enterprise examples: medical, finance, legal
- Why explicit constraints reduce hallucination

**Hour 2: Build & Compare (60 min)**
- Build weak prompt together
- Run it on same query
- Observe noisy output (vague, unstructured)
- Ask: "What's missing from the prompt?"

**Hour 3: Add Constraints (60 min)**
- Add role definition
- Add output schema
- Add constraints
- Run same query again
- Compare: Quality improvement visible

**Hour 4: Analyst Prompt Deep Dive (60 min)**
- Walk through all 6 sections of analyst prompt
- Why each section matters
- Examples of good vs bad analyst output
- JSON extraction for charts

**Hour 5: Writer Prompt Deep Dive (60 min)**
- Walk through writer prompt
- HTML structure requirements
- Semantic tags (article, section, etc)
- Link preservation

**Hour 6: Prompt Review Exercise (60 min)**
- Students pair up
- Each pair critiques another's prompt
- Present feedback
- Iterate on prompts

## Assessment Checkpoint
By end of Day 2, students should:
- ✓ Design role prompts with measurable output contracts
- ✓ Explain where and why query normalization is applied
- ✓ Identify what makes a prompt weak vs strong
- ✓ Score prompt quality using rubric
