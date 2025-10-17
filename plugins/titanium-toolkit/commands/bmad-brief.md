---
description: Generate BMAD product brief from project idea
---

# BMAD Brief - Generate Product Brief

You are generating a Product Brief following BMAD methodology. This is the first document in the BMAD workflow, capturing the high-level vision and goals.

## Purpose

Create a comprehensive product brief that serves as the foundation for PRD generation. The brief captures the project idea, problem statement, target users, and MVP scope.

## Process

### Step 1: Gather Project Idea

**If user provided description**:
- Use their description directly

**If user said just `/bmad:brief`**:
- Ask: "What's your project idea at a high level?"
- Wait for response
- Ask follow-up if needed: "What problem does it solve? Who is it for?"

### Step 2: Generate Product Brief

Use the `bmad_generator` MCP tool:

```
mcp__plugin_titanium-toolkit_tt__bmad_generator(
  doc_type: "brief",
  input_path: "{{user_idea}}",
  project_path: "$(pwd)"
)
```

This creates `bmad-backlog/product-brief.md` with all required sections.

**Important**: The tool uses Claude Haiku 4.5 to generate comprehensive content. Requires ANTHROPIC_API_KEY in ~/.env

### Step 3: Review Generated Brief

Read the generated brief:

```bash
Read bmad-backlog/product-brief.md
```

Present key sections to user:

```
📄 Product Brief Generated

Project: {{project name}}

Key Sections:
- Executive Summary: {{first paragraph}}
- Problem Statement: {{brief summary}}
- Target Users: {{primary segment}}
- MVP Scope: {{core features count}}

Full brief saved to: bmad-backlog/product-brief.md

Would you like to:
1. Approve and continue to PRD
2. Refine specific sections
3. Regenerate with more details
```

### Step 4: Handle User Response

**If user wants refinements**:
- Ask which sections to refine
- Regenerate brief with additional context
- Show updated content

**If user approves**:
- Continue to Step 5

**If user wants to regenerate**:
- Ask for more details
- Re-run the `bmad_generator` tool with enhanced prompt

### Step 5: Validate with vibe-check

```
mcp__vibe-check__vibe_check(
  goal: "Create product brief for {{project}}",
  plan: "Generated brief with: Executive Summary, Problem Statement, Solution, Target Users, MVP Scope, Technical Considerations",
  uncertainties: [
    "Is the problem statement clear enough?",
    "Are target users well-defined?",
    "Is MVP scope realistic?"
  ]
)
```

**Handle vibe-check response**:
- If concerns raised → Present to user, refine as needed
- If approved → Continue

### Step 6: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Product brief for {{project name}}",
  summary: "Created product brief for {{project}}. Problem: {{problem summary}}. Target users: {{users}}. MVP scope: {{features}}. Tech stack preferences: {{stack}}. Ready for PRD generation.",
  files: [
    "bmad-backlog/product-brief.md"
  ],
  project: "$(pwd)"
)
```

### Step 7: Present Summary and Next Steps

```
✅ Product Brief Complete!

📄 Location: bmad-backlog/product-brief.md

📊 Summary:
- Problem: {{one-line problem}}
- Solution: {{one-line solution}}
- Users: {{primary user segment}}
- MVP Features: {{count}} core features

💡 Next Steps:

Option 1: Generate PRD next
Run: /bmad:prd

Option 2: Generate complete backlog
Run: /bmad:start
(This will use the brief to generate PRD, Architecture, and all Epics)

What would you like to do?
```

## Error Handling

### If ANTHROPIC_API_KEY Missing

```
❌ Error: ANTHROPIC_API_KEY not found

The brief generation needs Anthropic Claude to create comprehensive content.

Please add your API key to ~/.env:
  echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' >> ~/.env
  chmod 600 ~/.env

Get your key from: https://console.anthropic.com/settings/keys

Then restart Claude Code and try again.
```

### If Generation Fails

```
❌ Brief generation failed

This could be due to:
- API rate limits
- Network issues
- Invalid project description

Let me try again with a simplified approach.

[Retry with more basic prompt]
```

### If User Wants to Skip Brief

```
Note: Product brief is optional but recommended.

You can skip directly to PRD with:
/bmad:prd

However, the brief helps organize your thoughts and produces better PRDs.

Skip brief and go to PRD? (yes/no)
```

## Voice Feedback

Voice hooks will announce:
- "Generating product brief" (when utility starts)
- "Product brief complete" (when done)

## Example Usage

**Example 1: Simple Idea**
```
User: /bmad:brief "Social network for developers"

Claude: "What problem does it solve?"
User: "Developers want to show off projects, not just resumes"

Claude: "Who are the primary users?"
User: "Junior developers looking for jobs"

[Generates brief]

Claude: "Brief complete! Would you like to generate the PRD next?"
```

**Example 2: Detailed Idea**
```
User: /bmad:brief "AI-powered precious metals research platform with real-time pricing, company fundamentals, smart screening, and AI-generated trade ideas for retail investors"

[Generates comprehensive brief from detailed description]

Claude: "Comprehensive brief generated! Next: /bmad:prd"
```

**Example 3: Interactive Mode**
```
User: /bmad:brief

Claude: "What's your project idea?"
User: "Todo app"

Claude: "What makes it different from existing todo apps?"
User: "Uses voice input and AI scheduling"

Claude: "Who is it for?"
User: "Busy professionals"

[Generates brief with full context]
```

## Important Guidelines

**Always**:
- ✅ Use `bmad_generator` MCP tool (don't generate manually)
- ✅ Validate with vibe-check
- ✅ Store in Pieces
- ✅ Present clear summary
- ✅ Suggest next steps

**Never**:
- ❌ Generate brief content manually (use the tool)
- ❌ Skip vibe-check validation
- ❌ Forget to store in Pieces
- ❌ Leave user uncertain about next steps

## Integration

**After `/bmad:brief`**:
- Suggest `/bmad:prd` to continue
- Or suggest `/bmad:start` to generate complete backlog
- Brief is referenced by PRD generation

**Part of `/bmad:start`**:
- Guided workflow calls brief generation
- Uses brief for PRD generation
- Seamless flow

---

**This command creates the foundation for your entire project backlog!**
