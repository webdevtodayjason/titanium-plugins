---
description: Generate BMAD Product Requirements Document
---

# BMAD PRD - Generate Product Requirements Document

Use the product-manager subagent to create a comprehensive Product Requirements Document (PRD) following BMAD methodology.

## Task Delegation

First check for product brief, then launch the product-manager subagent to handle the complete PRD generation workflow.

## Process

### Step 1: Check for Product Brief

```bash
ls bmad-backlog/product-brief.md 2>/dev/null || echo "No brief found"
```

**If brief NOT found**:
```
❌ Error: Product Brief not found at bmad-backlog/product-brief.md

PRD generation requires a product brief to work from.

Please run: /titanium-toolkit:bmad-brief first
(Or /titanium-toolkit:bmad-start for complete guided workflow)
```

Stop here - do not launch product-manager without brief.

**If brief exists**: Continue to Step 2.

### Step 2: Launch Product-Manager Subagent

Use the Task tool to launch the product-manager subagent in its own context window:

```
Task(
  description: "Generate BMAD PRD",
  prompt: "Create comprehensive Product Requirements Document following BMAD methodology.

Input:
- Product Brief: bmad-backlog/product-brief.md

Output:
- PRD: bmad-backlog/prd/prd.md

Your workflow:

1. **Read the product brief** to understand the project vision

2. **Generate PRD** using the MCP tool:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_generator(
     doc_type: \"prd\",
     input_path: \"bmad-backlog/product-brief.md\",
     project_path: \"$(pwd)\"
   )
   ```

3. **Review epic structure** - Ensure Epic 1 is \"Foundation\" and epic sequence is logical

4. **Detect research needs** - Scan for API, vendor, data source, payment, hosting keywords

5. **Validate PRD** using:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_validator(
     doc_type: \"prd\",
     document_path: \"bmad-backlog/prd/prd.md\"
   )
   ```

6. **Run vibe-check** to validate PRD quality and completeness

7. **Store in Pieces** for future reference

8. **Present summary** with epic list, research needs, and next steps

**IMPORTANT**: Keep your summary response BRIEF (under 500 tokens). Just return:
- Confirmation PRD is complete
- Epic count and list (just titles)
- Total user stories count
- Total features count

DO NOT include the full PRD content in your response - it's already saved to the file.

Follow your complete PRD workflow from the bmad-methodology skill.

Project path: $(pwd)",
  subagent_type: "product-manager"
)
```

The product-manager subagent will handle:
- Reading product brief
- Generating comprehensive PRD (500-1000 lines)
- Epic structure review
- Research needs detection
- Validation (structural and vibe-check)
- Pieces storage
- Summary presentation

### Step 3: Return Results

The product-manager will return a summary when complete. Present this to the user.

## What the Product-Manager Creates

The product-manager subagent generates `bmad-backlog/prd/prd.md` containing:

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

**Cost**: ~$0.03 (Claude Haiku 4.5 for PRD generation)

---

**This command creates the complete product specification that drives architecture and implementation!**
