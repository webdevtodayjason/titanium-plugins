---
description: Generate BMAD product brief from project idea
---

# BMAD Brief - Generate Product Brief

Use the product-manager subagent to create a comprehensive Product Brief following BMAD methodology. The brief captures the high-level vision and goals.

## Task Delegation

First gather the project idea, then launch the product-manager subagent to handle the complete brief generation workflow.

## Process

### Step 1: Gather Project Idea

**If user provided description**:
- Store their description

**If user said just `/bmad:brief`**:
- Ask: "What's your project idea at a high level?"
- Wait for response
- Ask follow-up if needed: "What problem does it solve? Who is it for?"

### Step 2: Launch Product-Manager Subagent

Use the Task tool to launch the product-manager subagent in its own context window:

```
Task(
  description: "Generate BMAD product brief",
  prompt: "Create comprehensive product brief following BMAD methodology.

User's Project Idea:
{{user_idea}}

Your workflow:

1. **Generate product brief** using the MCP tool:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_generator(
     doc_type: \"brief\",
     input_path: \"{{user_idea}}\",
     project_path: \"$(pwd)\"
   )
   ```

2. **Review generated brief** - Read bmad-backlog/product-brief.md and present key sections to user

3. **Validate the brief** using:
   ```
   mcp__plugin_titanium-toolkit_tt__bmad_validator(
     doc_type: \"brief\",
     document_path: \"bmad-backlog/product-brief.md\"
   )
   ```

4. **Run vibe-check** to validate the brief quality

5. **Store in Pieces** for future reference

6. **Present summary** to user with next steps

**IMPORTANT**: Keep your summary response BRIEF (under 300 tokens). Just return:
- Confirmation brief is complete
- 1-2 sentence project description
- Primary user segment
- MVP feature count

DO NOT include the full brief content in your response - it's already saved to the file.

Follow your complete brief workflow from the bmad-methodology skill.

Project path: $(pwd)",
  subagent_type: "product-manager"
)
```

The product-manager subagent will handle:
- Generating product brief
- Reviewing and presenting key sections
- Validation (structural and vibe-check)
- Pieces storage
- Summary presentation

### Step 3: Return Results

The product-manager will return a summary when complete. Present this to the user.

## What the Product-Manager Creates

The product-manager subagent generates `bmad-backlog/product-brief.md` containing:

- **Executive Summary**: Project concept, problem, target market, value proposition
- **Problem Statement**: Current state, pain points, urgency
- **Proposed Solution**: Core concept, differentiators
- **Target Users**: Primary and secondary user segments with detailed profiles
- **Goals & Success Metrics**: Business objectives, user success metrics, KPIs
- **MVP Scope**: Core features and what's out of scope
- **Technical Considerations**: Platform requirements, tech preferences
- **Constraints & Assumptions**: Budget, timeline, resources
- **Risks & Open Questions**: Key risks and areas needing research
- **Next Steps**: Immediate actions and PM handoff

## Integration with Research

The product-manager may identify research needs during brief generation and suggest running `/bmad:research` for topics like:
- Data vendors or APIs
- Technology comparisons
- Market research

## Voice Feedback

Voice hooks announce:
- "Generating product brief" (when starting)
- "Product brief complete" (when finished)

## Cost

Typical cost: ~$0.01 per brief generation (Claude Haiku 4.5 API usage in bmad_generator tool)

### Step 4: Present Summary and Next Steps

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
