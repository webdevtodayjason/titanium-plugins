---
description: Complete guided BMAD backlog generation workflow
---

# BMAD Start - Complete Guided Workflow

You are orchestrating complete BMAD backlog generation from idea to implementation-ready documentation. This guided workflow creates Product Brief, PRD, Architecture, all Epic files, and Story Index in one comprehensive session.

## Purpose

Take user from empty folder to complete project backlog (30-45 minutes):
- Product Brief (high-level vision)
- PRD (comprehensive requirements with epics and user stories)
- Architecture (technical design with code examples)
- Epic files (all epics with detailed stories and acceptance criteria)
- Story Index (summary of all stories)

## Overview

**This workflow has 6 phases**:
1. **Introduction** - Welcome and mode selection
2. **Product Brief** - Capture high-level vision
3. **PRD** - Comprehensive requirements
4. **Research** - Technical research (if needed)
5. **Architecture** - Technical design
6. **Epics & Index** - All epic files and summary

**Duration**: 30-45 minutes
**Cost**: ~$0.22 (GPT-4 for all documents)
**Output**: Complete bmad-backlog/ folder

---

## Phase 1: Introduction & Setup

### Step 1.1: Welcome User

```
🚀 BMAD Document Generation - Complete Guided Workflow

Welcome to the BMAD backlog creation process!

This workflow will create complete project documentation:
✅ Product Brief - High-level vision and goals
✅ PRD - Comprehensive requirements with epics
✅ Architecture - Technical design with code examples
✅ Epic Files - Detailed user stories with acceptance criteria
✅ Story Index - Summary of all stories for sprint planning

⏱️  Duration: 30-45 minutes
💰 Cost: ~$0.22 (GPT-4 for document generation)
📁 Output: bmad-backlog/ folder with all documentation

Ready to start? (yes/no)
```

If no → Exit
If yes → Continue

### Step 1.2: Check for Existing Documentation

```bash
ls -la bmad-backlog/ 2>/dev/null || echo "No backlog found"
```

**If bmad-backlog/ exists**:
```
⚠️  Found existing BMAD documentation!

bmad-backlog/ folder exists with:
{{List existing files}}

Options:
1. **Start fresh** - Delete existing and create new (DESTRUCTIVE)
2. **Add to existing** - Generate new epics only
3. **Cancel** - Review existing docs first

What would you like to do?
```

**If option 1**: Confirm destruction, delete bmad-backlog/, continue
**If option 2**: Skip to Phase 5 (epic generation)
**If option 3**: Exit

**If no bmad-backlog/**:
- Continue to Step 1.3

### Step 1.3: Choose Mode

```
Choose your workflow mode:

1. **Interactive** (Recommended)
   - I'll ask questions section by section
   - You review and refine as we go
   - Higher quality, more control
   - ~45 minutes

2. **YOLO** (Faster)
   - I'll generate complete drafts from your idea
   - You refine afterwards
   - Faster but may need more editing
   - ~30 minutes

Which mode? (1 or 2)
```

Store user's choice for the workflow.

---

## Phase 2: Product Brief Generation

### Step 2.1: Capture High-Level Idea

```
🎯 Let's start with your project idea.

Describe your project at a high level:
- What is it?
- Who is it for?
- What problem does it solve?

You can be brief (one sentence) or detailed (a paragraph).
I'll ask follow-up questions to flesh it out.

Your idea:
```

Wait for user response.

### Step 2.2: Interactive Questions (if Interactive mode)

Ask clarifying questions:
1. "What problem does this solve for users?"
2. "Who are the primary users (be specific)?"
3. "What makes this different from existing solutions?"
4. "What are the 3-5 core features for MVP?"
5. "What should be out of scope for MVP?"
6. "Any technical preferences (language, framework, hosting)?"
7. "Budget and timeline constraints?"

### Step 2.3: Generate Product Brief

```
Generating Product Brief...
```

Run:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py brief "{{user_idea}}" "$(pwd)"
```

Creates: `bmad-backlog/product-brief.md`

### Step 2.4: Review Brief with User

Read and show key sections:

```
✅ Product Brief Generated!

{{Show Executive Summary}}

{{Show Problem Statement (first paragraph)}}

{{Show MVP Scope - core features}}

Full brief: bmad-backlog/product-brief.md

Approve brief, or refine specific sections? (approve/refine/regenerate)
```

**If refine**: Ask which sections, regenerate with additions
**If regenerate**: Ask for more context, run utility again
**If approve**: Continue

### Step 2.5: Validate Brief

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_validator.py brief "bmad-backlog/product-brief.md"
```

If invalid, fix and regenerate.

---

## Phase 3: PRD Generation

### Step 3.1: Generate PRD

```
Generating comprehensive Product Requirements Document...

This will take about 1-2 minutes (large document).
```

Run:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py prd "bmad-backlog/product-brief.md" "$(pwd)"
```

Creates: `bmad-backlog/prd/prd.md` (500-1000 lines)

### Step 3.2: Review Epic Structure

Read PRD and extract epic list:

```
✅ PRD Generated!

📊 PRD Structure:
- {{N}} Epics
- {{M}} User Stories
- {{F}} V1 MVP Features
- Technical requirements defined
- Success metrics set

Epic List:
1. Epic 1: {{name}} - {{description}}
2. Epic 2: {{name}} - {{description}}
3. Epic 3: {{name}} - {{description}}
...

⚠️  IMPORTANT: Epic 1 should be "Foundation" or "Infrastructure"
{{If Epic 1 is not foundation: Alert and suggest reordering}}

Epic structure look good? (yes/refine)
```

**If refine**: Adjust epic list, regenerate PRD
**If yes**: Continue

### Step 3.3: Validate PRD

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_validator.py prd "bmad-backlog/prd/prd.md"
```

Check validation, fix if needed.

### Step 3.4: vibe-check Validation

```
mcp__vibe-check__vibe_check(
  goal: "Create comprehensive PRD for {{project}}",
  plan: "Generated PRD with {{N}} epics, {{M}} user stories, technical requirements, success metrics",
  uncertainties: [
    "Is epic structure logical?",
    "Are requirements complete?",
    "Any critical features missing?"
  ]
)
```

Present vibe-check feedback, adjust if needed.

---

## Phase 4: Research (If Needed)

### Step 4.1: Detect Research Needs

Scan PRD for keywords:
- "API", "vendor", "data source"
- "payment", "authentication"
- "hosting", "infrastructure"

**If research topics detected**:
```
🔍 Research Opportunities Detected!

Your PRD mentions:
- {{Topic 1}} (e.g., "data vendors")
- {{Topic 2}} (e.g., "authentication provider")
- {{Topic 3}} (e.g., "hosting platform")

These decisions will impact your architecture.

Would you like research prompts for these? (yes/no/specific topics)
```

### Step 4.2: Generate Research Prompts

**For each selected topic**:
Run `/bmad:research "{{topic}}"` for each

Present:
```
📋 Research Prompts Generated!

I've created research prompts for:
1. {{Topic 1}} - bmad-backlog/research/RESEARCH-{{slug}}-prompt.md
2. {{Topic 2}} - bmad-backlog/research/RESEARCH-{{slug}}-prompt.md

Please:
1. Open each prompt file
2. Copy to ChatGPT/Claude web
3. Complete research (~10-15 min per topic)
4. Fill in findings templates
5. Return here when done

Ready to continue after research? (yes/skip)
```

**If yes**: Wait for confirmation research is complete
**If skip**: Continue without research

---

## Phase 5: Architecture Generation

### Step 5.1: Generate Architecture

```
Generating Technical Architecture...

This will take 2-3 minutes (comprehensive document with code examples).
```

Run:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py architecture "bmad-backlog/prd/prd.md" "$(pwd)"
```

Creates: `bmad-backlog/architecture/architecture.md` (1000-1500 lines)

### Step 5.2: Review Tech Stack

Present proposed tech stack:

```
✅ Architecture Generated!

🏗️  Proposed Tech Stack:
- Frontend: {{framework}}
- Backend: {{framework}}
- Database: {{database}}
- Cache: {{Redis/etc}}
- Hosting MVP: {{platform}}
- Hosting Production: {{platform}}

{{If research completed:}}
✅ Based on your research:
- {{Research-based decision 1}}
- {{Research-based decision 2}}

Tech stack approval? (yes/changes)
```

**If changes**: Note changes, can regenerate or user edits manually
**If yes**: Continue

### Step 5.3: Validate Architecture

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_validator.py architecture "bmad-backlog/architecture/architecture.md"
```

Ensure all sections present, fix if needed.

---

## Phase 6: Epic Generation & Index

### Step 6.1: Extract Epic List from PRD

Read PRD and identify all epics from User Stories section.

Count epics:
```
Found {{N}} epics in PRD:
1. {{Epic name}}
2. {{Epic name}}
3. {{Epic name}}
...

Generating all {{N}} epic files...
```

### Step 6.2: Generate All Epics

For each epic (sequential):

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py epic "bmad-backlog/prd/prd.md" "bmad-backlog/architecture/architecture.md" {{epic_num}} "$(pwd)"
```

Show progress:
```
Generating epics...
✅ Epic 1: {{name}} ({{X}} stories)
✅ Epic 2: {{name}} ({{Y}} stories)
✅ Epic 3: {{name}} ({{Z}} stories)
⏳ Epic 4: {{name}} (generating...)
```

### Step 6.3: Generate Story Index

After all epics:

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py index "bmad-backlog/epics/" "$(pwd)"
```

Creates: `bmad-backlog/STORY-INDEX.md`

---

## Phase 7: Final Review & Summary

### Step 7.1: Validate Complete Backlog

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_validator.py all "bmad-backlog/"
```

Check all documents valid.

### Step 7.2: Final vibe-check

```
mcp__vibe-check__vibe_check(
  goal: "Create complete BMAD backlog for {{project}}",
  plan: "Generated: Product Brief, PRD ({{N}} epics, {{M}} stories), Architecture ({{tech stack}}), {{N}} Epic files, Story Index",
  uncertainties: [
    "Is documentation complete and consistent?",
    "Are epics logically sequenced?",
    "Is architecture aligned with requirements?",
    "Any gaps in the backlog?"
  ]
)
```

Present vibe-check assessment.

### Step 7.3: Store Complete Backlog in Pieces

**First, build explicit file list** (Pieces doesn't expand wildcards):

```bash
# Use Glob to find all epic files
Glob bmad-backlog/epics/EPIC-*.md
```

Store the results, then build files array.

**If research was completed**:
```bash
# Find research files
Glob bmad-backlog/research/RESEARCH-*.md
```

**Then call Pieces with explicit paths**:

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Complete BMAD backlog for {{project}}",
  summary: "Generated complete project backlog using BMAD methodology.

Documents created:
- Product Brief: {{vision summary}}
- PRD: {{N}} sections, {{E}} epics, {{M}} user stories, {{F}} features
- Architecture: Tech stack ({{stack}}), database schemas ({{table count}} tables), infrastructure plan ({{hosting}}), security architecture
- {{E}} Epic files: Each with stories, acceptance criteria, technical notes
- Story Index: {{M}} stories, {{P}} story points

Key features:
{{List main features}}

Tech stack:
{{Stack summary}}

Epics:
{{List all epics}}

Cost estimates:
- MVP: ${{X}}/month
- Production: ${{Y}}/month

Ready for implementation with /titanium:plan bmad-backlog/epics/EPIC-001-*.md",
  files: [
    "bmad-backlog/product-brief.md",
    "bmad-backlog/prd/prd.md",
    "bmad-backlog/architecture/architecture.md",
    "{{list each epic file from Glob results}}",
    "bmad-backlog/STORY-INDEX.md",
    "{{list each research file from Glob results if research completed}}"
  ],
  project: "$(pwd)"
)
```

**Example with explicit paths**:
```
files: [
  "bmad-backlog/product-brief.md",
  "bmad-backlog/prd/prd.md",
  "bmad-backlog/architecture/architecture.md",
  "bmad-backlog/epics/EPIC-001-foundation.md",
  "bmad-backlog/epics/EPIC-002-core-features.md",
  "bmad-backlog/epics/EPIC-003-advanced.md",
  "bmad-backlog/epics/EPIC-004-polish.md",
  "bmad-backlog/STORY-INDEX.md"
]
```

**If research completed, add**:
```
  "bmad-backlog/research/RESEARCH-data-vendors-prompt.md",
  "bmad-backlog/research/RESEARCH-data-vendors-findings.md"
```

### Step 7.4: Present Complete Summary

```
🎉 BMAD Backlog Generation Complete!

📚 Documentation Created:

✅ Product Brief
   Location: bmad-backlog/product-brief.md
   Purpose: High-level vision and goals

✅ Product Requirements Document (PRD)
   Location: bmad-backlog/prd/prd.md
   Size: ~{{lines}} lines
   Epics: {{N}}
   User Stories: {{M}}
   Features: {{F}}

✅ Technical Architecture
   Location: bmad-backlog/architecture/architecture.md
   Size: ~{{lines}} lines
   Tech Stack: {{stack summary}}
   Database Tables: {{count}}
   Cost Estimate: ${{MVP cost}}/month MVP

✅ Epic Files ({{N}} epics)
   Location: bmad-backlog/epics/
   Files:
   - EPIC-001-{{name}}.md ({{X}} stories)
   - EPIC-002-{{name}}.md ({{Y}} stories)
   - EPIC-003-{{name}}.md ({{Z}} stories)
   ...

✅ Story Index
   Location: bmad-backlog/STORY-INDEX.md
   Total: {{M}} stories, {{P}} story points

{{If research completed:}}
✅ Research Findings
   Location: bmad-backlog/research/
   Topics: {{list topics}}

---

📊 Project Summary:

Goal: {{high-level goal}}
Target Users: {{primary user segment}}
MVP Features: {{core feature count}}
Tech Stack: {{Frontend}} + {{Backend}} + {{Database}}
MVP Timeline: 12-16 weeks (from PRD estimate)
Cost: ${{X}}/month MVP, ${{Y}}/month Production

Epic Sequence:
1. {{Epic 1}} - Foundation ({{stories}} stories, {{points}} points)
2. {{Epic 2}} - {{name}} ({{stories}} stories, {{points}} points)
3. {{Epic 3}} - {{name}} ({{stories}} stories, {{points}} points)
...

Total Development Effort: {{total story points}} story points

---

📁 Folder Structure:

bmad-backlog/
├── product-brief.md
├── prd/
│   └── prd.md
├── architecture/
│   └── architecture.md
├── epics/
│   ├── EPIC-001-{{name}}.md
│   ├── EPIC-002-{{name}}.md
│   └── ... ({{N}} total)
{{If research:}}
├── research/
│   ├── RESEARCH-{{topic}}-prompt.md
│   └── RESEARCH-{{topic}}-findings.md
└── STORY-INDEX.md

---

💡 Next Steps:

Ready to start implementing?

**Option 1: Plan First Epic** (Recommended)
```
/titanium:plan bmad-backlog/epics/EPIC-001-{{name}}.md
```
This will break Epic 1 into implementation tasks.

**Option 2: Review Documentation First**
Open and review:
- bmad-backlog/prd/prd.md (requirements)
- bmad-backlog/architecture/architecture.md (technical design)
- bmad-backlog/epics/*.md (user stories)

Then come back and run:
```
/titanium:plan bmad-backlog/epics/EPIC-001-{{name}}.md
```

**Option 3: Complete Workflow**
```
/titanium:work bmad-backlog/epics/EPIC-001-{{name}}.md
```
This will plan AND implement Epic 1 in one go.

---

🎊 Congratulations! You now have complete project documentation following BMAD methodology.

Your backlog is ready for professional AI-powered development with Titanium Toolkit.

What would you like to do next?
```

---

## Detailed Workflow

### Interactive Mode Steps

**Product Brief**:
1. Capture idea
2. Ask 7-10 clarifying questions
3. Generate brief
4. Show to user
5. Refine if needed
6. Validate and approve

**PRD**:
1. Read brief
2. Ask about success metrics
3. Ask about features (work through MVP features)
4. Propose epic structure
5. For each epic, ask about user stories
6. Ask about technical requirements
7. Ask about data/AI needs
8. Ask about design preferences
9. Ask about go-to-market
10. Ask about risks
11. Generate comprehensive PRD
12. Review epic list with user
13. Validate and approve

**Research** (if needed):
1. Detect research needs from PRD
2. Offer to generate prompts
3. Generate prompts and templates
4. Wait for user to research
5. Confirm research complete
6. Continue

**Architecture**:
1. Read PRD
2. Read research findings (if exist)
3. Propose tech stack
4. Get user approval
5. Generate comprehensive architecture
6. Show tech stack and cost estimates
7. Validate and approve

**Epics**:
1. Extract epic list from PRD
2. For each epic:
   - Generate epic file
   - Show story count
   - Progress indicator
3. Generate story index
4. Show totals

### YOLO Mode Steps

**All at once**:
1. Capture idea
2. Ask 2-3 critical questions only
3. Generate ALL documents with one set of prompts
4. Present complete backlog
5. User reviews and refines any sections needed

**Faster but less precise** - good for experienced users.

---

## Error Handling

### If OPENAI_API_KEY Missing

```
❌ Error: OPENAI_API_KEY required

This workflow uses GPT-4 to generate comprehensive documentation.

Add your key to ~/.env:
  echo 'OPENAI_API_KEY=sk-your-key' >> ~/.env
  chmod 600 ~/.env

Restart Claude Code and try again.

Cost: ~$0.22 for complete backlog (less than a coffee!)
```

### If Generation Fails Mid-Workflow

```
❌ Error during {{document}} generation

Error: {{error message}}

Options:
1. Retry this step
2. Skip this document (not recommended)
3. Cancel workflow (documents created so far are saved)

What would you like to do?
```

### If User Cancels Mid-Workflow

```
⏸️  Workflow Paused

Documents created so far:
{{List what's been created}}

You can resume by running individual commands:
- /bmad:prd (if brief complete)
- /bmad:architecture (if PRD complete)
- /bmad:epic {{N}} (if architecture complete)

Or start over: /bmad:start
```

---

## Voice Feedback

Voice announces progress:
- "Starting BMAD workflow" (at beginning)
- "Product brief complete" (after phase 2)
- "PRD complete: {{N}} epics" (after phase 3)
- "Architecture complete" (after phase 5)
- "Generating epics" (phase 6)
- "Epic {{N}} of {{total}} complete" (each epic)
- "Backlog complete: {{M}} stories" (at end)

---

## Time Estimates

**Interactive Mode**:
- Product Brief: ~10 minutes (questions + generation)
- PRD: ~15 minutes (questions + generation)
- Research: ~15 minutes per topic (optional)
- Architecture: ~5 minutes (generation + review)
- Epics: ~2 minutes per epic (generation)
- **Total: ~45 minutes** (without research) to ~60 minutes (with research)

**YOLO Mode**:
- Idea capture: ~5 minutes
- Generation: ~10 minutes (all documents)
- Review: ~15 minutes
- **Total: ~30 minutes**

---

## Important Guidelines

**Always**:
- ✅ Validate each document before proceeding
- ✅ Use vibe-check for quality validation
- ✅ Store progress in Pieces after each phase
- ✅ Present clear summaries
- ✅ Verify Epic 1 is Foundation
- ✅ Offer research opportunities
- ✅ Guide user to next steps

**Never**:
- ❌ Skip document validation
- ❌ Ignore vibe-check concerns
- ❌ Generate incomplete documents
- ❌ Forget to generate story index
- ❌ Leave user uncertain about next steps

## Integration

**After `/bmad:start`** completes:
```
/titanium:plan bmad-backlog/epics/EPIC-001-*.md
/titanium:work
```

**Complete cycle**:
```
Idea → /bmad:start → /titanium:plan → /titanium:work → Working Code
  (45 min)        (2 min)         (3-6 hours)
```

**Cost Breakdown**:
- BMAD generation: $0.22
- Implementation: $0.10 per epic
- **Total for MVP**: $0.22 + (4 epics × $0.10) = ~$0.62

---

**This command transforms an idea into a complete, implementation-ready project backlog in under an hour!**
