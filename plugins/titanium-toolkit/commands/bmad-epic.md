---
description: Generate single BMAD epic with user stories
---

# BMAD Epic - Generate Epic File

You are generating a single epic file with user stories following BMAD methodology. This command is used to add NEW epics to existing backlog or regenerate existing epics.

## When to Use This Command

**Add NEW Epic** (change request, new feature):
```bash
# 6 months after launch, need mobile app
/bmad:epic "Mobile App"
# → Creates EPIC-012-mobile-app.md
```

**Regenerate Existing Epic** (refinement):
```bash
/bmad:epic 3
# → Regenerates EPIC-003 with updated content
```

**NOT used during `/bmad:start`** - guided workflow generates all epics automatically.

## Process

### Step 1: Check Prerequisites

**Require PRD**:
```bash
ls bmad-backlog/prd/prd.md 2>/dev/null || echo "No PRD found"
```

If not found:
```
❌ Error: PRD required for epic generation

Please run: /bmad:prd
(Or /bmad:start for complete workflow)
```

**Check for Architecture** (recommended):
```bash
ls bmad-backlog/architecture/architecture.md 2>/dev/null || echo "No architecture found"
```

If not found:
```
⚠️  Architecture not found

Epic generation works best with architecture (for technical notes).

Would you like to:
1. Generate architecture first (recommended): /bmad:architecture
2. Continue without architecture (epics will have minimal technical notes)
3. Cancel

Choose:
```

###  Step 2: Determine Epic to Generate

**If user provided epic number**:
```bash
# User ran: /bmad:epic 3
```
- Epic number = 3
- Read PRD to find Epic 3 definition
- Generate EPIC-003

**If user provided epic name**:
```bash
# User ran: /bmad:epic "Mobile App"
```
- Determine next epic number (count existing epics + 1)
- Generate new epic with this name
- Save as EPIC-{next_num}-mobile-app.md

**If user provided nothing**:
- Ask: "Which epic would you like to generate?
  - Provide epic number (e.g., 1, 2, 3)
  - Or epic name for NEW epic (e.g., 'Mobile App')
  - Or 'all' to generate all epics from PRD"

### Step 3: Read PRD and Architecture

```bash
Read bmad-backlog/prd/prd.md
Read bmad-backlog/architecture/architecture.md
```

**Extract from PRD**:
- Epic definition from User Stories section
- Related feature requirements
- User stories for this epic

**Extract from Architecture**:
- Relevant tech stack details
- Database schemas for epic entities
- Security implementation for epic features
- Infrastructure notes

### Step 4: Generate Epic

Use the `bmad_generator` MCP tool:

```
mcp__plugin_titanium-toolkit_tt__bmad_generator(
  doc_type: "epic",
  input_path: "bmad-backlog/prd/prd.md bmad-backlog/architecture/architecture.md {{epic_number}}",
  project_path: "$(pwd)"
)
```

This creates: `bmad-backlog/epics/EPIC-{num:03d}-{slug}.md`

**Generated content** (300-500 lines):
- Epic header (Owner, Priority, Sprint, Status, Effort)
- Epic Description (what and why)
- Business Value
- Success Criteria (checkboxes)
- User Stories (STORY-{epic}-{num} format)
  - Each with "As a... I want... so that..."
  - Acceptance criteria (checkboxes)
  - Technical notes (code examples from architecture)
- Dependencies (blocks/blocked by)
- Risks & Mitigation
- Related Epics
- Definition of Done

### Step 5: Review Generated Epic

Read and present summary:

```bash
Read bmad-backlog/epics/EPIC-{num}-{name}.md
```

```
✅ Epic {{num}} Generated!

📄 Location: bmad-backlog/epics/EPIC-{{num}}-{{name}}.md

📊 Epic Summary:
- Title: {{epic title}}
- Priority: {{P0/P1/P2}}
- Stories: {{count}}
- Estimated Effort: {{points}} story points

Stories Included:
1. STORY-{{epic}}-01: {{title}}
2. STORY-{{epic}}-02: {{title}}
3. STORY-{{epic}}-03: {{title}}
...

{{If technical notes present:}}
✅ Technical notes from architecture included

{{If architecture missing:}}
⚠️  Technical notes minimal (no architecture document)

Review epic? (yes/no)
```

**If user wants to review**:
- Show key stories
- Show acceptance criteria examples
- Ask for refinements

**If user approves**:
- Continue

### Step 6: Validate Epic

```
mcp__plugin_titanium-toolkit_tt__bmad_validator(
  doc_type: "epic",
  document_path: "bmad-backlog/epics/EPIC-{{num}}-{{name}}.md"
)
```

Check:
- Required fields present (Owner, Priority, Status, Effort)
- Required sections present
- Stories in correct format (STORY-XXX-YY)
- Acceptance criteria present
- User story format ("As a... I want... so that...")

If validation fails, regenerate.

### Step 7: Update Story Index

**If STORY-INDEX.md exists**:
```
I'll update the story index with this new epic.

Regenerating index...
```

Run:
```
mcp__plugin_titanium-toolkit_tt__bmad_generator(
  doc_type: "index",
  input_path: "bmad-backlog/epics/",
  project_path: "$(pwd)"
)
```

Show:
```
✅ Story index updated!

Total: {{N}} epics, {{M}} stories, {{P}} story points
```

**If no index exists**:
- Create new one
- Show totals

### Step 8: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Epic {{num}}: {{name}}",
  summary: "Generated epic file for {{name}}. Contains {{story count}} user stories with acceptance criteria and technical notes. Priority: {{priority}}. Estimated effort: {{points}} story points. Epic focuses on: {{brief description}}. Dependencies: {{blocks/blocked by}}. Ready for implementation with /titanium:plan.",
  files: [
    "bmad-backlog/epics/EPIC-{{num}}-{{name}}.md",
    "bmad-backlog/STORY-INDEX.md" (if updated)
  ],
  project: "$(pwd)"
)
```

### Step 9: Suggest Next Steps

**If more epics in PRD**:
```
📋 More epics to generate?

Your PRD has {{total}} epics:
{{List all epics with status}}

Generate next epic? (yes/epic number/no)
```

**If this was the last epic**:
```
🎉 All epics complete!

Your backlog is now complete:
- Product Brief ✅
- PRD ✅
- Architecture ✅
- {{N}} Epics ✅
- Story Index ✅

Total: {{M}} user stories ready for implementation

Ready to implement?

Run: /titanium:plan bmad-backlog/epics/EPIC-001-*.md
Then: /titanium:work
```

**If adding NEW epic** (not in PRD):
```
✅ New epic added to backlog!

This epic was added as EPIC-{{num}}.

Consider:
1. Update PRD to include this epic in the epic list
2. Update STORY-INDEX.md (already done ✅)
3. Start implementing: /titanium:plan bmad-backlog/epics/EPIC-{{num}}-{{name}}.md
```

## Important Guidelines

**Always**:
- ✅ Require PRD (cannot generate epic without it)
- ✅ Check for architecture (improves technical notes quality)
- ✅ Use bmad_generator.py utility
- ✅ Validate with bmad_validator.py
- ✅ Update story index after generation
- ✅ Validate with vibe-check
- ✅ Store in Pieces
- ✅ Suggest next steps clearly

**Never**:
- ❌ Generate epic manually
- ❌ Skip validation
- ❌ Forget to update story index
- ❌ Generate epic without PRD context

## Epic Numbering

**If adding new epic**:
```bash
# Count existing epics
EXISTING=$(ls bmad-backlog/epics/EPIC-*.md 2>/dev/null | wc -l)
NEXT_NUM=$((EXISTING + 1))

# New epic becomes EPIC-{NEXT_NUM}
```

**If regenerating**:
- Use existing epic number
- Overwrite file
- Preserve filename

## Integration

**Standalone**:
```
/bmad:epic 1
/bmad:epic 2
/bmad:epic 3
```

**Part of `/bmad:start`**:
- Guided workflow generates all epics automatically
- Loops through epic list from PRD
- Generates each sequentially

**After Initial Backlog**:
```
# 6 months later, need new feature
/bmad:epic "Mobile App"
# → Adds EPIC-012
# → Updates index
# → Ready to implement
```

**Cost**: ~$0.01 per epic (GPT-4 generation)

---

**This command enables incremental backlog growth and epic refinement!**
