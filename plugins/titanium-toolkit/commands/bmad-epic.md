---
description: Generate single BMAD epic with user stories
---

# BMAD Epic - Generate Epic File

Use the product-manager subagent to create a single epic file with user stories following BMAD methodology. This command is used to add NEW epics to existing backlog or regenerate existing epics.

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

## Task Delegation

First check prerequisites, determine which epic to generate, then launch the product-manager subagent to handle the complete epic generation workflow.

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

Stop here - do not launch product-manager without PRD.

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

If user chooses 1: Run `/bmad:architecture` first, then continue
If user chooses 2: Continue to Step 2
If user chooses 3: Exit gracefully

### Step 2: Determine Epic to Generate

**If user provided epic number**:
```bash
# User ran: /bmad:epic 3
```
- Epic number = 3
- Store epic_identifier = "3"

**If user provided epic name**:
```bash
# User ran: /bmad:epic "Mobile App"
```
- Epic name = "Mobile App"
- Store epic_identifier = "Mobile App"

**If user provided nothing**:
- Ask: "Which epic would you like to generate?
  - Provide epic number (e.g., 1, 2, 3)
  - Or epic name for NEW epic (e.g., 'Mobile App')
  - Or 'all' to generate all epics from PRD"
- Wait for response
- Store epic_identifier

### Step 3: Launch Product-Manager Subagent

Use the Task tool to launch the product-manager subagent in its own context window:

```
Task(
  description: "Generate BMAD epic with user stories",
  prompt: "Create comprehensive epic file following BMAD methodology.

Epic to Generate: {{epic_identifier}}

Input:
- PRD: bmad-backlog/prd/prd.md
- Architecture: bmad-backlog/architecture/architecture.md (if exists)

Output:
- Epic file: bmad-backlog/epics/EPIC-{num:03d}-{slug}.md
- Updated index: bmad-backlog/STORY-INDEX.md

Your workflow:

1. **Read inputs** to understand context:
   - Read bmad-backlog/prd/prd.md
   - Read bmad-backlog/architecture/architecture.md (if exists)
   - Extract epic definition and user stories

2. **Generate epic** using MCP tool:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_generator(
     doc_type: \"epic\",
     input_path: \"bmad-backlog/prd/prd.md bmad-backlog/architecture/architecture.md {{epic_identifier}}\",
     project_path: \"$(pwd)\"
   )
   ```

3. **Review and present** epic summary:
   - Read generated epic file
   - Present title, priority, story count, story points
   - Show story list
   - Note if technical notes included/minimal

4. **Validate epic** using:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_validator(
     doc_type: \"epic\",
     document_path: \"bmad-backlog/epics/EPIC-{num}-{name}.md\"
   )
   ```

5. **Update story index**:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_generator(
     doc_type: \"index\",
     input_path: \"bmad-backlog/epics/\",
     project_path: \"$(pwd)\"
   )
   ```

6. **Run vibe-check** to validate epic quality

7. **Store in Pieces** for future reference

8. **Present summary** with next steps:
   - If more epics in PRD: offer to generate next
   - If this was last epic: show completion status
   - If new epic not in PRD: suggest updating PRD

**IMPORTANT**: Keep your summary response VERY BRIEF (under 200 tokens). Just return:
- Confirmation epic is complete
- Epic title and number
- Story count
- Story points total

DO NOT include the full epic content in your response - it's already saved to the file.

Follow your complete epic workflow from the bmad-methodology skill.

Project path: $(pwd)",
  subagent_type: "product-manager"
)
```

The product-manager subagent will handle:
- Reading PRD and Architecture
- Generating epic file (300-500 lines)
- Presenting epic summary
- Validation (structural and vibe-check)
- Updating story index
- Pieces storage
- Summary presentation with next steps

### Step 4: Return Results

The product-manager will return a summary when complete. Present this to the user.

## What the Product-Manager Creates

The product-manager subagent generates `bmad-backlog/epics/EPIC-{num:03d}-{slug}.md` containing:

- **Epic Header**: Owner, Priority, Sprint, Status, Effort
- **Epic Description**: What and why
- **Business Value**: Why this epic matters
- **Success Criteria**: Checkboxes for completion
- **User Stories**: STORY-{epic}-{num} format
  - Each with "As a... I want... so that..."
  - Acceptance criteria (checkboxes)
  - Technical notes (code examples from architecture)
- **Dependencies**: Blocks/blocked by relationships
- **Risks & Mitigation**: Potential issues and solutions
- **Related Epics**: Cross-references
- **Definition of Done**: Completion checklist

Also updates `bmad-backlog/STORY-INDEX.md` with new epic totals.

## Epic Numbering

**If adding new epic**:
- Determines next epic number by counting existing epics
- New epic becomes EPIC-{next_num}-{slug}.md

**If regenerating**:
- Uses existing epic number
- Overwrites file
- Preserves filename

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

## Voice Feedback

Voice announces:
- "Generating epic" (when starting)
- "Epic {{num}} complete: {{story count}} stories" (when done)

## Cost

Typical cost: ~$0.01 per epic (Claude Haiku 4.5 API usage in bmad_generator tool)

---

**This command delegates to the product-manager subagent who creates complete epic files with user stories!**
