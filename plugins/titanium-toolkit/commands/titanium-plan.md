---
description: Analyze requirements and create detailed implementation plan
---

# Titanium Plan Command

You are creating a structured implementation plan from requirements. Follow this systematic process to break down work into actionable tasks with agent assignments.

## Process Overview

This command will:
1. Gather and validate requirements
2. Use Claude to generate structured plan
3. Validate plan with vibe-check
4. Create human-readable documentation
5. Store plan in Pieces for future reference

## Step 1: Gather Requirements

**If user provides a file path:**
```bash
# User might say: /titanium:plan ~/bmad/output/user-auth-prd.md
```
- Use Read tool to read the file
- Extract requirements text

**If user provides inline description:**
```bash
# User might say: /titanium:plan
# Then describe: "I need to add JWT authentication with login, register, password reset"
```
- Write description to `.titanium/requirements.md` using Write tool
- Ask clarifying questions if needed:
  - What tech stack? (Node.js, Python, Ruby, etc.)
  - What database? (PostgreSQL, MongoDB, etc.)
  - Any specific libraries or frameworks?
  - Security requirements?
  - Performance requirements?

## Step 2: Generate Structured Plan

Use the `plan_parser` MCP tool to generate the plan:

```
mcp__plugin_titanium-toolkit_tt__plan_parser(
  requirements_file: ".titanium/requirements.md",
  project_path: "$(pwd)"
)
```

This will:
- Call Claude with the requirements
- Generate structured JSON plan with:
  - Epics (major features)
  - Stories (user-facing functionality)
  - Tasks (implementation steps)
  - Agent assignments
  - Time estimates
  - Task dependencies
- Save to `.titanium/plan.json`
- Return the JSON plan directly to Claude

**Important**: The plan_parser tool needs ANTHROPIC_API_KEY environment variable. If it fails with an API key error, inform the user they need to add it to ~/.env

## Step 3: Review the Generated Plan

Read and analyze `.titanium/plan.json`:

```bash
# Read the plan
Read .titanium/plan.json
```

Check that the plan:
- Has reasonable epics (1-5 major features)
- Each epic has logical stories (1-5 per epic)
- Each story has actionable tasks (2-10 per story)
- Agent assignments are appropriate
- Time estimates seem realistic
- Dependencies make sense

**Common issues to watch for:**
- Tasks assigned to wrong agents (e.g., frontend work to @api-developer)
- Missing testing tasks
- Missing documentation tasks
- Unrealistic time estimates
- Circular dependencies

If the plan needs adjustments:
- Edit `.titanium/requirements.md` to add clarifications
- Re-run the `plan_parser` tool
- Review again

## Step 4: Validate Plan with vibe-check

Use vibe-check to validate the plan quality:

```
mcp__vibe-check__vibe_check(
  goal: "User's stated goal from requirements",
  plan: "Summary of the generated plan - list epics, key stories, agents involved, total time",
  uncertainties: [
    "List any concerns about complexity",
    "Note any ambiguous requirements",
    "Mention any technical risks"
  ]
)
```

**Example**:
```
mcp__vibe-check__vibe_check(
  goal: "Implement JWT authentication system with login, register, and password reset",
  plan: "2 epics: Backend API (JWT middleware, 3 endpoints, database) and Frontend UI (login/register forms, password reset flow). Agents: @product-manager, @api-developer, @frontend-developer, @test-runner, @security-scanner. Total: 4 hours",
  uncertainties: [
    "Should we use refresh tokens or just access tokens?",
    "Password hashing algorithm not specified - suggest argon2",
    "Rate limiting strategy needs clarification"
  ]
)
```

**Handle vibe-check response:**
- If vibe-check raises **concerns**:
  - Review the concerns carefully
  - Update requirements or plan approach
  - Re-run the `plan_parser` tool with adjustments
  - Validate again with vibe-check
- If vibe-check **approves**:
  - Continue to next step

## Step 5: Create Human-Readable Plan

Write a markdown version of the plan to `.titanium/plan.md`:

```markdown
# Implementation Plan: [Project Goal]

**Created**: [Date]
**Estimated Time**: [Total time from plan.json]

## Goal
[User's goal statement]

## Tech Stack
[List technologies mentioned in requirements]

## Epics

### Epic 1: [Epic Name]
**Description**: [Epic description]
**Estimated Time**: [Sum of all story times]

#### Story 1.1: [Story Name]
**Description**: [Story description]
**Tasks**:
1. [Task 1 name] - [@agent-name] - [time estimate]
2. [Task 2 name] - [@agent-name] - [time estimate]

#### Story 1.2: [Story Name]
**Description**: [Story description]
**Tasks**:
1. [Task 1 name] - [@agent-name] - [time estimate]
2. [Task 2 name] - [@agent-name] - [time estimate]

### Epic 2: [Epic Name]
[... repeat structure ...]

## Agents Involved
- **@product-manager**: Requirements validation
- **@api-developer**: Backend implementation
- **@frontend-developer**: UI development
- **@test-runner**: Testing
- **@doc-writer**: Documentation

## Dependencies
[List any major dependencies between epics/stories]

## Next Steps
Ready to execute? Run: `/titanium:work`
```

## Step 6: Store Plan in Pieces

Store the plan in Pieces LTM for future reference:

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Implementation plan for [project name/goal]",
  summary: "Plan created with [X] epics, [Y] stories, [Z] tasks. Agents: [list agents]. Estimated time: [total time]. Key features: [brief list of main epics]. vibe-check validation: [summary of validation results]",
  files: [
    ".titanium/plan.json",
    ".titanium/plan.md",
    ".titanium/requirements.md"
  ],
  project: "$(pwd)"
)
```

**Example**:
```
mcp__Pieces__create_pieces_memory(
  summary_description: "Implementation plan for JWT authentication system",
  summary: "Plan created with 2 epics, 5 stories, 12 tasks. Agents: @product-manager, @api-developer, @frontend-developer, @test-runner, @security-scanner. Estimated time: 4 hours. Key features: JWT middleware with refresh tokens, login/register/reset endpoints, frontend auth forms, comprehensive testing. vibe-check validation: Plan structure is sound, recommended argon2 for password hashing, suggested rate limiting on auth endpoints.",
  files: [
    ".titanium/plan.json",
    ".titanium/plan.md",
    ".titanium/requirements.md"
  ],
  project: "/Users/username/projects/my-app"
)
```

## Step 7: Present Plan to User

Format the output in a clear, organized way:

```
📋 Implementation Plan Created

🎯 Goal: [User's goal]

📦 Structure:
- [X] epics
- [Y] stories
- [Z] implementation tasks

⏱️  Estimated Time: [total time]

🤖 Agents Involved:
- @agent-name (role description)
- @agent-name (role description)
- [... list all agents ...]

📁 Plan saved to:
- .titanium/plan.json (structured data)
- .titanium/plan.md (readable format)

✅ vibe-check validated: [Brief summary of validation results]

📝 Key Epics:
1. [Epic 1 name] - [time estimate]
2. [Epic 2 name] - [time estimate]
[... list all epics ...]

---

Ready to execute this plan?

Run: /titanium:work

This will orchestrate the implementation using the plan,
with voice announcements and quality gates throughout.
```

## Important Guidelines

**Always:**
- ✅ Use the `plan_parser` MCP tool (don't try to generate plans manually)
- ✅ Validate with vibe-check before finalizing
- ✅ Store the plan in Pieces
- ✅ Create both JSON (for machines) and Markdown (for humans)
- ✅ Get user approval before they proceed to /titanium:work
- ✅ Be specific about agent roles in the summary

**Never:**
- ❌ Skip vibe-check validation
- ❌ Generate plans without using the `plan_parser` tool
- ❌ Proceed to implementation without user approval
- ❌ Ignore vibe-check concerns
- ❌ Create plans without clear task assignments

## Error Handling

**If ANTHROPIC_API_KEY is missing:**
```
Error: The plan_parser tool needs an Anthropic API key to generate plans.

Please add your API key to ~/.env:
  echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' >> ~/.env
  chmod 600 ~/.env

Then restart Claude Code and try again.
```

**If vibe-check is not available:**
```
Warning: vibe-check MCP is not available. Proceeding without quality validation.

Consider setting up vibe-check for AI-powered quality gates:
  1. Create ~/.vibe-check/.env
  2. Add at least one API key (GEMINI_API_KEY, OPENAI_API_KEY, or OPENROUTER_API_KEY)
  3. Restart Claude Code
```

**If requirements are unclear:**
```
The requirements need more detail. Let me ask some questions:

1. [Specific question about tech stack]
2. [Specific question about features]
3. [Specific question about constraints]

Once I have this information, I'll create a detailed plan.
```

**If plan generation fails:**
```
The plan generation failed. This could be due to:
- Invalid requirements format
- API rate limits
- Network issues

Let me try again with simplified requirements.
[Retry with more basic prompt]
```

## Example Usage

**Example 1: With BMAD PRD file**
```
User: /titanium:plan ~/bmad/output/user-auth-prd.md

Claude:
- Reads PRD file
- Calls plan_parser tool
- Reviews generated plan
- Validates with vibe-check
- Creates plan.md
- Stores in Pieces
- Presents formatted summary to user
```

**Example 2: With inline description**
```
User: /titanium:plan

Claude: "What would you like to implement?"

User: "Add a search feature to filter products by name and category"

Claude:
- Writes description to .titanium/requirements.md
- Asks: "What's your tech stack?"
User: "React frontend, Node.js backend with PostgreSQL"
- Calls plan_parser tool with complete requirements
- Generates plan with appropriate tech stack
- Validates with vibe-check
- Presents plan to user
```

**Example 3: Complex feature with multiple clarifications**
```
User: /titanium:plan "Build a payment processing system"

Claude: "I need more details:
1. Which payment provider? (Stripe, PayPal, etc.)
2. What types of payments? (One-time, subscriptions, both?)
3. Currency support? (Single, multiple?)
4. Security requirements? (PCI compliance needed?)
5. Refund handling?"

User: "Stripe, one-time payments only, USD, yes PCI compliance, yes refunds"

Claude:
- Writes complete requirements
- Generates comprehensive plan
- vibe-check raises concern about PCI compliance complexity
- Adjusts plan to include @security-scanner more heavily
- Re-validates with vibe-check
- Presents approved plan
```

## Voice Feedback

The voice hooks will automatically announce:
- "Starting plan generation" (when script is called)
- "Plan created with [X] epics" (when complete)
- "vibe-check validation complete" (after validation)

No additional voice calls needed - the hooks handle this automatically.

## Next Command

After creating the plan, the user should run:
```
/titanium:work
```

This will execute the plan with orchestrated agent coordination.
