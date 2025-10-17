---
description: Generate BMAD Product Requirements Document
---

# BMAD PRD - Generate Product Requirements Document

You are generating a comprehensive Product Requirements Document (PRD) following BMAD methodology. The PRD is the complete specification of product requirements, features, user stories, and technical needs.

## Purpose

Create a detailed PRD that defines all product requirements, organizes features into epics, documents user stories, and establishes technical specifications. This document guides architecture and implementation.

## Process

### Step 1: Check for Product Brief

```bash
ls bmad-backlog/product-brief.md 2>/dev/null || echo "No brief found"
```

**If brief exists**:
- Read it with Read tool
- Use brief content as foundation

**If no brief**:
- Ask user: "No product brief found. Would you like to:
  1. Create a brief first with `/bmad:brief` (recommended)
  2. Provide requirements directly
  3. Cancel"

If user chooses option 2, gather requirements through questions.

### Step 2: Generate PRD

Use the `bmad_generator` MCP tool:

```
mcp__plugin_titanium-toolkit_tt__bmad_generator(
  doc_type: "prd",
  input_path: "bmad-backlog/product-brief.md",
  project_path: "$(pwd)"
)
```

This generates `bmad-backlog/prd/prd.md` with complete PRD structure (500-1000 lines).

**Sections generated**:
1. Executive Summary (Vision, Mission)
2. Product Overview (Users, Value Props, Competitive Positioning)
3. Success Metrics (North Star, KPIs)
4. Feature Requirements (V1 MVP, V2 Features with acceptance criteria)
5. User Stories (organized by Epic)
6. Technical Requirements (Performance, Scalability, Security, etc.)
7. Data Requirements (if applicable)
8. AI/ML Requirements (if applicable)
9. Design Requirements
10. Go-to-Market Strategy
11. Risks & Mitigation (tables)
12. Open Questions
13. Appendix (Glossary, References)

### Step 3: Review Generated PRD

Read the PRD:

```bash
Read bmad-backlog/prd/prd.md
```

**Key sections to review with user**:

1. **Epic List** (from User Stories section):
   ```
   Epic Structure:
   - Epic 1: {{name}} ({{story count}} stories)
   - Epic 2: {{name}} ({{story count}} stories)
   - Epic 3: {{name}} ({{story count}} stories)
   ...

   Total: {{N}} epics, {{M}} stories

   Is this epic breakdown logical and complete?
   ```

2. **Feature Requirements**:
   ```
   V1 MVP Features: {{count}}
   V2 Features: {{count}}

   Are priorities correct (P0, P1, P2)?
   ```

3. **Technical Requirements**:
   ```
   Performance: {{targets}}
   Security: {{requirements}}
   Tech Stack Preferences: {{from brief or inferred}}

   Any adjustments needed?
   ```

### Step 4: Detect Research Needs

Scan PRD for research keywords:
- "API", "vendor", "data source", "integration"
- "payment", "authentication provider"
- "hosting", "infrastructure"

**If research needs detected**:
```
⚠️  I detected you'll need research on:
- {{Research topic 1}} (e.g., "data vendors for pricing")
- {{Research topic 2}} (e.g., "authentication providers")
- {{Research topic 3}} (e.g., "hosting platforms")

Would you like me to generate research prompts for these?

Research prompts help you:
- Use ChatGPT/Claude web (they have web search!)
- Get current pricing and comparisons
- Make informed architecture decisions

Generate research prompts? (yes/no/specific topics)
```

**If user says yes**:
- For each research topic, run `/bmad:research "{{topic}}"`
- Wait for user to complete research
- Note that architecture generation will use research findings

**If user says no**:
- Continue without research
- Architecture will make best guesses

### Step 5: Refine PRD (if needed)

**If user wants changes**:
- Identify specific sections to refine
- Can regenerate entire PRD with additional context
- Or user can manually edit the file

**To regenerate**:
```
# Add context to brief or provide directly
mcp__plugin_titanium-toolkit_tt__bmad_generator(
  doc_type: "prd",
  input_path: "bmad-backlog/product-brief.md",
  project_path: "$(pwd)"
)
```

### Step 6: Validate PRD Structure

Use the `bmad_validator` MCP tool to check completeness:

```
mcp__plugin_titanium-toolkit_tt__bmad_validator(
  doc_type: "prd",
  document_path: "bmad-backlog/prd/prd.md"
)
```

**Check results**:
- If valid → Continue
- If missing sections → Alert user, regenerate

### Step 7: Validate with vibe-check

```
mcp__vibe-check__vibe_check(
  goal: "Create comprehensive PRD for {{project}}",
  plan: "Generated PRD with {{N}} epics, {{M}} features, technical requirements, user stories",
  uncertainties: [
    "Is epic structure logical and sequential?",
    "Are requirements complete?",
    "Any missing critical features?"
  ]
)
```

**Process feedback**:
- Review vibe-check suggestions
- Make adjustments if needed
- Regenerate if significant concerns

### Step 8: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Product Requirements Document for {{project}}",
  summary: "Complete PRD generated with {{N}} sections. Epics: {{list epics}}. Key features: {{list main features}}. Technical requirements: {{summary}}. User stories: {{count}} across {{epic count}} epics. Ready for architecture generation.",
  files: [
    "bmad-backlog/product-brief.md",
    "bmad-backlog/prd/prd.md"
  ],
  project: "$(pwd)"
)
```

### Step 9: Present Summary

```
✅ Product Requirements Document Complete!

📄 Location: bmad-backlog/prd/prd.md

📊 PRD Summary:
- {{N}} Epics defined
- {{M}} User stories
- {{F}} V1 MVP features
- Technical requirements specified
- Success metrics defined

Epic Structure:
1. Epic 1: {{name}} (Foundation - this is always first)
2. Epic 2: {{name}}
3. Epic 3: {{name}}
...

📏 Document Size: ~{{line count}} lines

✅ vibe-check validated structure

---

💡 Next Steps:

Option 1: Generate Architecture (Recommended)
Run: /bmad:architecture

Option 2: Review PRD first
Open: bmad-backlog/prd/prd.md
(Review and come back when ready)

Option 3: Generate complete backlog
Run: /bmad:start
(Will use this PRD to generate Architecture and all Epics)

What would you like to do?
```

## Important Guidelines

**Always**:
- ✅ Check for product brief first
- ✅ Use `bmad_generator` MCP tool (don't generate manually)
- ✅ Detect research needs from requirements
- ✅ Validate with `bmad_validator` MCP tool
- ✅ Validate with vibe-check
- ✅ Store in Pieces
- ✅ Present epic structure clearly
- ✅ Suggest next steps

**Never**:
- ❌ Generate PRD content manually
- ❌ Skip validation steps
- ❌ Ignore vibe-check concerns
- ❌ Forget to check epic structure (Epic 1 must be Foundation)
- ❌ Miss research opportunities

## Epic List Quality Check

**Verify Epic 1 is Foundation**:
```
Epic 1 should be: "Foundation", "Infrastructure", "Core Setup", or similar
Epic 1 should NOT be: Feature-specific like "User Profiles" or "Dashboard"

If Epic 1 is not foundation:
- Alert user
- Suggest reordering
- Regenerate with correct sequence
```

## Integration with Workflow

**Standalone Usage**:
```
/bmad:brief
/bmad:prd        ← You are here
/bmad:architecture
```

**Part of `/bmad:start`**:
- Guided workflow generates brief first
- Then calls PRD generation
- Uses brief automatically
- Continues to architecture

**Cost**: ~$0.06 (GPT-4 for PRD generation)

---

**This command creates the complete product specification that drives architecture and implementation!**
