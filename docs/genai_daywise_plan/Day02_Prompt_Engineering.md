# Day 2 - Prompt Engineering (6 Hours)

## Skeleton 2 (Day 2)
Prompt control layer over base execution.

```text
NewsNexus/
└── src/
    ├── agents.py        # role prompts: Researcher / Analyst / Writer
    └── streamlit_app.py # input normalization before prompting
```

## Stage-by-Stage Delivery
1. Stage A - Prompt anatomy (role, objective, constraints, output schema)
2. Stage B - Multi-role prompt design
3. Stage C - Robust query interpretation (typo normalization)
4. Stage D - Prompt quality evaluation

## Code Breakdown (What to Teach in Code)
- Researcher prompt and query rules: [src/agents.py](src/agents.py#L31)
- Analyst prompt for evidence-first reasoning: [src/agents.py](src/agents.py#L100)
- Writer prompt for detailed HTML structure: [src/agents.py](src/agents.py#L162)
- Topic normalization function: [src/streamlit_app.py](src/streamlit_app.py#L221)

## Instructor Logic Script
- Explain why “ask model nicely” fails in production.
- Show how explicit constraints reduce irrelevant outputs.
- Show how role-specific prompts separate responsibilities.
- Show typo correction path (`nauruto` -> `Naruto`) as practical guardrail.

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: Prompt engineering theory with enterprise examples.
- Hour 2: Build a weak prompt; observe noisy output.
- Hour 3: Add role + output constraints; compare quality.
- Hour 4: Deep dive into analyst prompt sections and JSON extraction requirements.
- Hour 5: Deep dive into writer prompt sections and HTML layout constraints.
- Hour 6: Prompt review rubric and team-style feedback exercise.

## Hands-on Tasks
1. Run same query with minimal and constrained prompts.
2. Compare outputs on:
   - specificity
   - source usage
   - structure
   - hallucination risk

## Assessment Checkpoint
- Student can design role prompts with measurable output contracts.
- Student can explain where and why query normalization is applied.
