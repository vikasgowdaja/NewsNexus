# Day 7 - GenAI Applications (6 Hours)

## Skeleton 7 (Day 7)
Application skeleton from user input to approval and export.

```text
Topic Input
 -> Agent Pipeline
 -> Draft Review
 -> Human Feedback/Approve
 -> Save + Export
```

## Stage-by-Stage Delivery
1. Stage A - UI state management
2. Stage B - Agent streaming integration
3. Stage C - Human review and revision loop
4. Stage D - Output export and archive

## Code Breakdown
- App boot and theme: [src/streamlit_app.py](src/streamlit_app.py#L21)
- Research trigger button and gating: [src/streamlit_app.py](src/streamlit_app.py#L343)
- Memory pre-check in UI flow: [src/streamlit_app.py](src/streamlit_app.py#L371)
- Stream events rendering: [src/streamlit_app.py](src/streamlit_app.py#L400)
- Review tabs: [src/streamlit_app.py](src/streamlit_app.py#L451)
- Approval persistence: [src/streamlit_app.py](src/streamlit_app.py#L488)

## Teacher Script (Detailed 6-Hour Plan)
- Hour 1: Product-level flow and user journey mapping.
- Hour 2: Streamlit state and rerun behavior deep dive.
- Hour 3: Bind UI to LangGraph stream updates.
- Hour 4: Human feedback mechanics and routing.
- Hour 5: HTML/PDF export and archive save path.
- Hour 6: Build one real feature enhancement in UI.

## Assessment Checkpoint
- Student can explain full request lifecycle from text input to archived result.

