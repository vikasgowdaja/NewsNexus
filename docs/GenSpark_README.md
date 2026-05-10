# GenSpark PPT Generation Files

This folder contains clean separation of **Content** and **Prompts** for generating professional PowerPoints with NewsNexus project-specific code mappings.

## Folder Structure

```
GenSpark_Content/
├── Day01_Content.md     ← Learning objectives, code blocks, teaching script
├── Day02_Content.md
├── ...
└── Day10_Content.md

GenSpark_Prompts/
├── Day01_Prompt.txt     ← Copy-paste directly into GenSpark AI
├── Day02_Prompt.txt
├── ...
└── Day10_Prompt.txt
```

## How to Use

### Option 1: Generate Full PPT from Single Prompt

1. **Open GenSpark AI:** https://gensparktools.com/
2. **Copy entire Day N prompt:** Open `GenSpark_Prompts/DayNN_Prompt.txt`
3. **Paste into GenSpark** input box
4. **Click "Generate"** → Wait for PowerPoint
5. **Download** the generated PPT

### Option 2: Reference Content While Customizing

1. **Read the content:** Open `GenSpark_Content/DayNN_Content.md`
2. **Understand:** Learning objectives, skeleton, code blocks, teaching script
3. **Modify the prompt** if needed (e.g., add your own examples)
4. **Generate new PPT** with customized version

## What Each File Contains

### Content Files (GenSpark_Content/)
- **Learning Objectives:** What students should know after this day
- **Skeleton Structure:** What gets built on this day
- **4 Stages:** Progression through the day's content
- **Critical Code Blocks:** EXACT code from NewsNexus with line numbers
- **Why This Matters:** Connection to previous/next days
- **6-Hour Teaching Script:** Hour-by-hour breakdown with activities
- **Assessment Checkpoint:** What students should be able to do

### Prompt Files (GenSpark_Prompts/)
- **Copy-paste ready** into GenSpark AI
- **Project context** explaining NewsNexus architecture
- **Presentation structure:** 12-15 slides with exact code blocks
- **Visual requirements:** Diagrams, color codes, syntax highlighting specs
- **Output format:** Number of slides + speaker notes

## Quick Workflow

```
Day 1 PPT:
  1. Open: GenSpark_Prompts/Day01_Prompt.txt
  2. Copy entire text
  3. Paste into GenSpark AI
  4. Click "Generate" 
  5. Download: Day01_GenAI_Setup.pptx

Day 2 PPT:
  (Same process with Day02_Prompt.txt)
```

## File Organization Rationale

- **Content files:** For reference during teaching prep, understanding context
- **Prompt files:** For GenSpark AI generation (clean, no extra text)
- **Separate folders:** Easy to navigate, clear purpose of each file

## Example: What You'll Get

After pasting `Day01_Prompt.txt` into GenSpark:

**Generated PowerPoint includes:**
- ✅ 10-15 professional slides
- ✅ Code blocks syntax-highlighted (Python)
- ✅ Skeleton 1 file structure visualization
- ✅ System architecture diagram
- ✅ 4-stage flow chart
- ✅ Model contract code with explanation
- ✅ Preflight check code with teaching notes
- ✅ 6-hour timeline with speaker notes
- ✅ Visual requirements met (color coding, icons)

## Tips for Best Results

1. **Use the full prompt** - Don't edit the GenSpark prompt sections
2. **Mention your customizations** - If adding local PDFs, add to prompt manually
3. **Review speaker notes** - GenSpark generates detailed speaker notes per slide
4. **Test one day first** - Start with Day 01 to see quality
5. **Download & customize** - After downloading, you can edit slides in PowerPoint

## Content Coverage (All 10 Days)

| Day | Focus | Skeleton |
|-----|-------|----------|
| 1 | Setup & Environment | requirements.txt + run_all.py |
| 2 | Prompt Engineering | agents.py prompts |
| 3 | Open Models | ChatOllama + OllamaEmbeddings |
| 4 | Embeddings & Search | ingestion.py + retrieval.py |
| 5 | RAG Pipeline | lookup_policy_docs tool |
| 6 | LangChain & Graphs | StateGraph + nodes + edges |
| 7 | Streamlit UI | st.text_input + .stream() |
| 8 | Optimization & Eval | Web search resilience + metrics |
| 9 | Memory & Archive | MemoryStore + check_memory |
| 10 | HITL Approval | Interrupts + conditional routing |

## Troubleshooting

**Q: Prompt text is too long?**
- GenSpark has input limits. If it fails, break into 2 parts.

**Q: Generated slides missing code blocks?**
- Make sure full prompt was pasted (copy entire txt file).

**Q: Want to customize visual style?**
- After download, edit PowerPoint theme, fonts, colors in Office.

**Q: Need to add your own examples?**
- Modify the prompt before pasting: Add your case studies, data, use cases.

## Next Steps

1. Generate all 10 PPTs (Day 1-10)
2. Review and customize in PowerPoint
3. Add your own supplementary materials (videos, labs, PDFs)
4. Create merged instructor handbook
5. Prepare assignment sheets + rubrics

---

**Created:** For NewsNexus 10-Day Generative AI Teaching Curriculum  
**Format:** Project-specific GenSpark AI prompts with exact code mappings  
**Target:** Clean, professional, production-ready educational materials
