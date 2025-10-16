---
description: Execute a multi-phase development workflow with agent orchestration
---

# Titanium Work Command

You are orchestrating a complete development workflow. This command coordinates multiple agents, manages state transitions, validates quality at each step, and stores progress in Pieces LTM.

## Overview

This workflow has 5 phases:
1. **Pre-Flight**: Validate setup and check for existing plan
2. **Planning**: Create plan if needed (or use existing)
3. **Implementation**: Execute tasks sequentially with agents
4. **Review**: Quality check with parallel review agents
5. **Completion**: Finalize and summarize

Voice hooks will announce progress automatically throughout.

---

## Phase 1: Pre-Flight Checks

### 1.1 Determine Project Path

```bash
# Get current working directory
pwd
```

Use this as the project_path for all subsequent operations.

### 1.2 Check for Existing Plan

```bash
# Check if plan exists
ls .titanium/plan.json
```

**If plan.json exists**:
- Read it with Read tool
- Ask user: "I found an existing plan. Would you like to use it or create a new one?"
- If user says use existing → Skip to Phase 3 (Implementation)
- If user says create new → Continue to Phase 2 (Planning)

**If plan.json does NOT exist**:
- Ask user: "No plan found. Would you like to:
  1. Create a plan now (I'll ask what to implement)
  2. Cancel and run /titanium:plan first (recommended for complex projects)

  If you have project documentation or backlog, I recommend running /titanium:plan first to review and break down the work."
- If user chooses option 1 → Continue to Phase 2 (Planning)
- If user chooses option 2 → Exit and suggest running /titanium:plan

### 1.3 Initialize Workflow State

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/workflow_state.py init "$(pwd)" "development" "User's stated goal"
```

**Example**:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/workflow_state.py init "$(pwd)" "development" "Implement user authentication system"
```

This creates `.titanium/workflow-state.json` to track progress.

---

## Phase 2: Planning (Skip if plan exists)

### 2.1 Gather Requirements

**If user provided file path**:
```bash
# User might have run: /titanium:work ~/bmad/output/prd.md
```
- Use Read tool to read the file
- Copy content to `.titanium/requirements.md`

**If user provided inline description**:
```bash
# User might say: "I need to add search functionality"
```
- Write description to `.titanium/requirements.md`
- Ask clarifying questions if needed

**If user provided nothing**:
- Ask: "What would you like to implement?"
- Wait for response
- Write to `.titanium/requirements.md`

### 2.2 Generate Plan

Use the plan_parser.py utility:

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/plan_parser.py .titanium/requirements.md "$(pwd)"
```

This creates `.titanium/plan.json` with structured plan.

### 2.3 Review Plan

Read and display the plan:

```bash
# Read the generated plan
Read .titanium/plan.json
```

Present summary to user:
```
📋 Plan Generated

🎯 Goal: [goal from requirements]

📦 Structure:
- [X] epics
- [Y] stories
- [Z] tasks

⏱️  Estimated Time: [total time]

🤖 Agents: [list of agents]

Key Epics:
1. [Epic 1] - [time]
2. [Epic 2] - [time]
```

### 2.4 Validate with vibe-check

```
mcp__vibe-check__vibe_check(
  goal: "User's stated goal",
  plan: "Summary: [X] epics, [Y] stories, [Z] tasks. Agents: [list]. Key work: [main epics]",
  uncertainties: [
    "List any concerns about complexity",
    "Note any unclear requirements",
    "Mention any technical risks"
  ]
)
```

**Handle Response**:
- If vibe-check raises **concerns**:
  - Present concerns to user
  - Ask: "Should we adjust the plan or proceed?"
  - If adjust → Go back to 2.1, refine requirements
  - If proceed → Continue
- If vibe-check **approves**:
  - Continue to next step

### 2.5 Create TodoWrite List

Read `.titanium/plan.json` and create comprehensive todo list:

**Format**: For each task in the plan, create todo:
```
"[Epic]: [Story] - [Task] (Agent: @agent-name)"
```

**Example**:
```
[
  {"content": "User Auth: Requirements - Validate requirements (Agent: @product-manager)", "status": "pending"},
  {"content": "User Auth: Backend API - Create JWT middleware (Agent: @api-developer)", "status": "pending"},
  {"content": "User Auth: Backend API - Create login endpoint (Agent: @api-developer)", "status": "pending"},
  {"content": "User Auth: Frontend - Create login form (Agent: @frontend-developer)", "status": "pending"},
  {"content": "User Auth: Testing - Write integration tests (Agent: @test-runner)", "status": "pending"}
]
```

Use TodoWrite tool to create this list.

### 2.6 Update State

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "planning" "completed"
```

### 2.7 Store Plan in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Implementation plan for [project goal]",
  summary: "Plan created with [X] epics, [Y] stories, [Z] tasks. Agents: [list]. Estimated time: [total]. Key work: [describe main epics and key technical decisions]",
  files: [
    ".titanium/plan.json",
    ".titanium/plan.md",
    ".titanium/requirements.md"
  ],
  project: "$(pwd)"
)
```

### 2.8 Get User Approval

**IMPORTANT**: Do NOT proceed to implementation without explicit user approval.

Ask user:
```
Plan is ready. The workflow will now:
1. Execute [Z] tasks sequentially
2. Use [N] different agents
3. Take approximately [time]
4. Run quality checks after each phase

Proceed with implementation? (yes/no)
```

Wait for user confirmation before continuing.

---

## Phase 3: Implementation

### 3.1 Update State

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "implementation" "in_progress"
```

### 3.2 Execute Tasks Sequentially

**IMPORTANT**: Execute ONE task at a time, in order from your TodoWrite list.

**For EACH task**:

#### Step A: Mark Task as in_progress

Update TodoWrite to mark current task as "in_progress".

#### Step B: Parse Task Info

From the task string, extract:
- Epic name
- Story name
- Task name
- Agent name (the @agent-name part)

#### Step C: Launch Agent

Use Task tool to launch the appropriate agent:

```
Task(
  description: "[Task name]",
  prompt: "You are working on: [Epic] > [Story] > [Task]

Requirements context:
[Relevant requirements from .titanium/requirements.md]

Previous work:
[If this task has dependencies, summarize what was done]

Task details:
[Specific instructions for this task]

Success criteria:
- [What needs to be completed]
- [What files should be created/modified]
- [What tests should pass]

After completion:
- Run any relevant tests
- Verify the work meets requirements
- Report what was accomplished",
  subagent_type: "[agent-type without @]"
)
```

**Example**:
```
Task(
  description: "Create JWT middleware",
  prompt: "You are working on: User Authentication > Backend API > Create JWT middleware

Requirements context:
- Need JWT-based authentication
- Should support refresh tokens
- Use argon2 for password hashing
- Rate limiting required

Task details:
Create Express middleware for JWT authentication that:
- Verifies JWT tokens from Authorization header
- Handles token expiration
- Returns 401 for invalid/expired tokens
- Attaches user info to req.user

Files to create:
- src/middleware/auth.ts

Success criteria:
- Middleware function exported
- Handles all error cases
- Tests pass

After completion, report what files were created and what the middleware does.",
  subagent_type: "api-developer"
)
```

#### Step D: Wait for Agent Completion

The agent will execute the work. Voice hooks will automatically announce completion.

#### Step E: Quality Check

After agent completes:

1. **Run tests if applicable**:
   ```bash
   # If package.json has test script
   npm test

   # Or pytest for Python
   pytest

   # Or appropriate test command
   ```

2. **Use vibe-check to validate progress**:
   ```
   mcp__vibe-check__vibe_check(
     goal: "Overall project goal",
     plan: "Current epic and story context",
     progress: "Just completed: [task name]. Agent: [agent]. Result: [brief summary of what was done]",
     uncertainties: [
       "Note any issues encountered",
       "List any deviations from plan",
       "Mention any new concerns"
     ]
   )
   ```

3. **Handle vibe-check response**:
   - If concerns raised → Present to user, decide whether to proceed or fix
   - If approved → Continue

#### Step F: Mark Task Completed

**IMMEDIATELY** update TodoWrite to mark current task as "completed".

Do NOT batch updates. Mark completed right after finishing.

#### Step G: Check for Epic Completion

If you just completed the last task of an epic:

1. **Store Epic Milestone in Pieces**:
   ```
   mcp__Pieces__create_pieces_memory(
     summary_description: "Completed Epic: [epic name]",
     summary: "Finished [epic name] with [N] stories and [M] tasks. Agents used: [list]. Key accomplishments: [what was built]. Files created/modified: [list key files]. Tests: [test results]. Time taken: [if known]",
     files: [
       "list all files created or modified in this epic"
     ],
     project: "$(pwd)"
   )
   ```

#### Step H: Continue to Next Task

Move to next task in TodoWrite list. Repeat steps A-G.

### 3.3 After All Tasks Complete

Once all implementation tasks are done, proceed to Phase 3.5 (CodeRabbit Analysis - if available) or Phase 4 (Review).

---

## Phase 3.5: CodeRabbit Analysis (Optional)

**This phase is optional** - only runs if CodeRabbit CLI is installed.

### 3.5.1 Check for CodeRabbit CLI

```bash
command -v coderabbit >/dev/null 2>&1 || echo "CodeRabbit not installed"
```

**If CodeRabbit NOT found**:
- Skip to Phase 4 (3-Agent Review)
- Workflow continues normally

**If CodeRabbit found**:
- Continue to 3.5.2

### 3.5.2 Offer CodeRabbit Analysis

```
🤖 CodeRabbit CLI Detected

Run CodeRabbit analysis before review?

CodeRabbit catches:
- Race conditions in concurrent code
- Memory leaks and resource leaks
- Security vulnerabilities
- Logic errors and edge cases
- Performance issues

Duration: 7-30 minutes (runs in background)
Cost: Uses your CodeRabbit account (free or paid tier)

Run CodeRabbit? (yes/no)
```

**If no**: Skip to Phase 4 (3-Agent Review)
**If yes**: Continue

### 3.5.3 Run CodeRabbit in Background

```bash
# Run with --prompt-only for AI-optimized output
coderabbit --prompt-only --type uncommitted
```

Use Bash tool with `run_in_background: true`

Show user:
```
🤖 CodeRabbit Analyzing...

Running in background (7-30 minutes typical).
I'll check progress periodically.

You can ask "Is CodeRabbit done?" anytime.
```

### 3.5.4 Wait for Completion

Check periodically (every 2-3 minutes) using BashOutput tool.

Show progress updates:
```
CodeRabbit analyzing... (5 minutes elapsed)
CodeRabbit analyzing... (10 minutes elapsed)
CodeRabbit analyzing... (15 minutes elapsed)
```

When complete:
```
✅ CodeRabbit analysis complete! ([X] minutes)
```

### 3.5.5 Parse and Present Findings

Read CodeRabbit --prompt-only output.

Present summary:
```
🤖 CodeRabbit Findings

📊 Issues Detected:
- 🔴 Critical: [X]
- 🟠 High: [Y]
- 🟡 Medium: [Z]
- 🟢 Low: [W]

Critical Issues:
1. Race condition in src/auth.ts:45
   - Shared state access without synchronization
   - Fix: Add mutex or use atomic operations

2. Memory leak in src/websocket.ts:123
   - Event listener not removed on disconnect
   - Fix: Add cleanup in disconnect handler

High Priority Issues:
1. SQL injection in src/api/users.ts:67
   - User input in raw SQL query
   - Fix: Use parameterized queries

[List all critical and high issues]

Would you like me to fix these?
1. Fix critical and high (recommended)
2. Fix critical only
3. Skip fixes, just document
4. Cancel
```

### 3.5.6 Apply Fixes (if requested)

**For each critical/high issue**:
1. Locate the problematic code (file:line from CodeRabbit)
2. Read CodeRabbit's suggested fix
3. Implement the fix
4. Run relevant tests
5. Mark as fixed in TodoWrite

Show progress:
```
Applying CodeRabbit fixes...

✅ Fixed: Race condition in auth.ts
   - Added mutex for shared state access
   - Tests passing

✅ Fixed: Memory leak in websocket.ts
   - Added event listener cleanup
   - Verified no leaks

✅ Fixed: SQL injection in users.ts
   - Converted to parameterized query
   - Tests passing

⏳ Fixing: Error handling in api.ts...
```

### 3.5.7 Optional Verification

After fixes applied:
```
CodeRabbit fixes complete!

Fixed: [X] critical, [Y] high priority issues

Re-run CodeRabbit to verify? (yes/no)
```

**If yes**:
```bash
coderabbit --prompt-only --type uncommitted
```

Check that:
- No new critical issues introduced
- Fixes resolved the original issues
- No regression

Show result:
```
✅ Verification complete!

Original issues: Resolved
New issues: None
Safe to proceed.
```

**If no**: Skip verification

### 3.5.8 Store CodeRabbit Findings

```
mcp__Pieces__create_pieces_memory(
  summary_description: "CodeRabbit analysis for [files]",
  summary: "CodeRabbit CLI analysis complete. Found: [X] critical, [Y] high, [Z] medium, [W] low issues. Critical issues: [list each]. High issues: [list each]. Fixes applied: [summary of fixes]. Duration: [X] minutes. Verified: [yes/no]. Ready for 3-agent review validation.",
  files: [
    "list all reviewed and fixed files"
  ],
  project: "$(pwd)"
)
```

### 3.5.9 Proceed to 3-Agent Review

```
CodeRabbit phase complete!

Proceeding to 3-agent review for validation...
```

Continue to Phase 4 (Review).

**Note**: 3-agent review will validate CodeRabbit fixes and catch anything CodeRabbit missed.

---

## Phase 4: Review

### 4.1 Update State

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "review" "in_progress"
```

### 4.2 Launch Review Agents in Parallel

**IMPORTANT**: Launch all three agents in a SINGLE message using multiple Task calls.

This enables them to run concurrently:

```
[Task 1]: @code-reviewer
Prompt: "Review all code changes for quality, readability, and best practices.

Focus on:
- Code quality and maintainability
- DRY principles
- SOLID principles
- Error handling
- Code organization
- Comments and documentation

Files to review: [list all modified files]

Provide findings categorized by severity:
- Critical: Must fix before deployment
- Important: Should fix soon
- Nice-to-have: Optional improvements

For each finding, specify:
- File and line number
- Issue description
- Recommendation"

[Task 2]: @security-scanner
Prompt: "Scan for security vulnerabilities and security best practices.

Focus on:
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization issues
- Secrets in code
- Dependency vulnerabilities
- HTTPS enforcement
- Rate limiting

Files to review: [list all modified files]

Provide findings with:
- Severity (Critical/High/Medium/Low)
- Vulnerability type
- File and line number
- Risk description
- Remediation steps"

[Task 3]: @tdd-specialist
Prompt: "Check test coverage and test quality.

Focus on:
- Test coverage percentage
- Edge cases covered
- Integration tests
- Unit tests
- E2E tests (if applicable)
- Test quality and assertions
- Mock usage
- Test organization

Files to review: [list all test files and source files]

Provide findings on:
- Coverage gaps
- Missing test cases
- Test quality issues
- Recommendations for improvement"
```

### 4.3 Wait for All Agents

Wait for all three review agents to complete (they run in parallel).

### 4.4 Aggregate Findings

Collect and organize all findings:

**Categories**:
- 🔴 **Critical** (must fix)
- 🟡 **Important** (should fix)
- 🟢 **Nice-to-have** (optional)

**For each finding**:
- Source: Which agent found it
- File: file.path:line
- Issue: Description
- Fix: Recommendation

### 4.5 Meta-Review with vibe-check

```
mcp__vibe-check__vibe_check(
  goal: "Original project goal",
  plan: "What was implemented",
  progress: "Implementation complete. Review findings: [X] critical, [Y] important, [Z] minor issues. Details: [summarize key findings]",
  uncertainties: [
    "Are there systemic issues we're missing?",
    "Is the implementation approach sound?",
    "Any architectural concerns?"
  ]
)
```

### 4.6 Create Review Report

Write `.titanium/review-report.md`:

```markdown
# Quality Review Report

**Date**: [current date]
**Project**: [project goal]
**Reviewers**: @code-reviewer, @security-scanner, @tdd-specialist

## Summary

- 🔴 Critical issues: [X]
- 🟡 Important issues: [Y]
- 🟢 Nice-to-have: [Z]

## Critical Issues 🔴

### [Issue 1 Title]
**File**: `path/to/file.ts:line`
**Source**: @security-scanner
**Severity**: Critical

**Description**:
[What the issue is]

**Risk**:
[Why it's critical]

**Recommendation**:
[How to fix it]

---

### [Issue 2 Title]
[... repeat structure ...]

## Important Issues 🟡

[... same structure ...]

## Nice-to-have 🟢

[... same structure ...]

## vibe-check Meta-Review

[Summary from vibe-check about overall quality]

## Test Coverage

**Overall Coverage**: [X]%
**Files with <80% coverage**: [list]
**Missing test cases**: [list]

## Recommendations

1. [Priority 1 recommendation]
2. [Priority 2 recommendation]
3. [Priority 3 recommendation]
```

### 4.7 Store Review in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Quality review findings for [project]",
  summary: "Review complete: [X] critical, [Y] important, [Z] minor issues. Critical issues: [list them briefly]. Important issues: [list them]. Test coverage: [X]%. vibe-check assessment: [summary]. Overall quality: [assessment]",
  files: [
    ".titanium/review-report.md",
    "list all reviewed files"
  ],
  project: "$(pwd)"
)
```

### 4.8 Present Summary

```
🔍 Quality Review Complete

🔴 [X] Critical Issues
🟡 [Y] Important Issues
🟢 [Z] Nice-to-have Improvements

📄 Full Report: .titanium/review-report.md

⚠️  Action Required:
[List critical issues with file:line]

💡 Recommendations:
1. [Top recommendation]
2. [Second recommendation]

Would you like me to fix the critical issues now?
```

**If user says yes**:
- Address critical issues one by one
- Re-run tests after each fix
- Update review report

**If user says no**:
- Proceed to Phase 5 (Completion)

---

## Phase 5: Completion

### 5.1 Mark Workflow Complete

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/workflow/workflow_state.py complete "$(pwd)"
```

### 5.2 Create Final Session Memory

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Completed: [project goal]",
  summary: "Full workflow summary:

Goal: [original goal]

What was built:
[List main features/components]

Epics completed: [X]
Stories completed: [Y]
Tasks completed: [Z]
Time taken: [if known]

Agents used:
[List agents and their contributions]

Quality review:
- Critical issues: [X] ([status: fixed/pending])
- Important issues: [Y]
- Test coverage: [X]%

Files created/modified:
[List key files]

Key technical decisions:
[List important decisions made during implementation]

Next steps:
[Suggest what should happen next]",
  files: [
    "list ALL project files that were part of this workflow"
  ],
  project: "$(pwd)",
  externalLinks: [
    "Any GitHub branches/PRs if created"
  ]
)
```

### 5.3 Present Completion Summary

```
✅ Workflow Complete!

🎯 Goal: [original goal]

📦 Delivered:
- [X] epics
- [Y] stories
- [Z] tasks completed

🤖 Agents Used:
- [Agent 1]: [what they did]
- [Agent 2]: [what they did]
[... list all agents ...]

📊 Quality:
- Tests: [X]% coverage
- Critical issues: [X] ([fixed/pending])
- Important issues: [Y]

📁 Key Files:
- [file 1]
- [file 2]
[... list main files ...]

📝 Documentation:
- Plan: .titanium/plan.md
- Review: .titanium/review-report.md
- State: .titanium/workflow-state.json

🎉 All work stored in Pieces for future reference!

---

Next Steps:
1. [Suggestion 1]
2. [Suggestion 2]
3. Run /titanium:status anytime to check progress
```

---

## Important Guidelines

### Always

- ✅ Use TodoWrite to track every task
- ✅ Execute tasks ONE at a time (sequential)
- ✅ Mark tasks completed IMMEDIATELY after finishing
- ✅ Use vibe-check after each task and epic
- ✅ Store milestones in Pieces after each epic
- ✅ Get user approval after planning phase
- ✅ Launch review agents in parallel (single message, multiple Tasks)
- ✅ Use workflow_state.py to track phases
- ✅ Handle errors gracefully - inform user of issues

### Never

- ❌ Skip vibe-check quality gates
- ❌ Execute multiple implementation tasks in parallel
- ❌ Batch todo updates - mark completed immediately
- ❌ Proceed to implementation without user approval
- ❌ Skip storing epic milestones in Pieces
- ❌ Ignore vibe-check concerns - always present to user
- ❌ Launch review agents sequentially - always parallel

---

## Error Handling

### If Agent Fails

```
Agent @[agent-name] encountered an error while [task].

Error: [error message]

Options:
1. Retry the task
2. Skip and continue
3. Modify approach and retry

What would you like to do?
```

### If vibe-check Raises Concerns

```
⚠️  vibe-check identified concerns:

[List concerns from vibe-check]

Recommendations:
[List suggestions from vibe-check]

Would you like to:
1. Address these concerns now
2. Proceed anyway (not recommended)
3. Adjust the approach
```

### If Tests Fail

```
❌ Tests failed after [task]

Failed tests:
[List failed tests]

Error output:
[Show errors]

I can:
1. Analyze and fix the failing tests
2. Continue anyway (not recommended)
3. Roll back this change

What would you like to do?
```

### If Missing API Keys

```
Error: Required API key missing

This workflow needs:
- OPENAI_API_KEY (for plan generation)
- ELEVENLABS_API_KEY (for voice announcements - optional but recommended)

For vibe-check quality gates (recommended):
- GEMINI_API_KEY or OPENAI_API_KEY in ~/.vibe-check/.env

Please add the required keys to ~/.env and restart Claude Code.
```

---

## Voice Feedback

Voice hooks automatically announce:
- "Starting [phase] phase" (at each phase transition)
- "[Agent] completed [task]" (after each agent)
- "[X] tasks remaining" (periodically)
- "Quality review complete: [findings count]" (after review)
- "Workflow complete" (at end)

No additional voice calls needed - hooks handle this.

---

## Example Usage

### Example 1: With Existing Plan

```
User: /titanium:work

Claude:
- Checks for .titanium/plan.json
- Found existing plan
- "I found a plan with 3 epics, 8 stories. Use this plan?"
User: "Yes"
- Skips planning phase
- Creates TodoWrite list from plan
- Starts implementation
- Executes tasks sequentially with agents
- Voice announces progress throughout
- Runs review at end
- Presents completion summary
```

### Example 2: Without Plan

```
User: /titanium:work "Add search functionality to products"

Claude:
- No plan found
- Writes requirements to .titanium/requirements.md
- Asks clarifying questions about tech stack
User: "React frontend, Node backend, Elasticsearch"
- Generates plan with plan_parser.py
- Validates with vibe-check
- Presents plan
- "Proceed with implementation?"
User: "Yes"
- Creates TodoWrite list
- Executes implementation
- [... continues through all phases ...]
```

### Example 3: From BMAD PRD

```
User: /titanium:work ~/bmad/output/user-auth-prd.md

Claude:
- Reads PRD file
- Generates plan from PRD
- Validates with vibe-check
- vibe-check: "Plan looks good, recommend adding rate limiting"
- Adjusts plan to include rate limiting
- Presents updated plan
- "Proceed?"
User: "Yes"
- Executes full workflow
- [... 4 hours of orchestrated work ...]
- Review finds 1 security issue
- Fixes security issue
- "Workflow complete!"
```

---

## Integration with Other Commands

**After /titanium:work**:
- Run `/titanium:status` to check final state
- Run `/catchup` in next session to resume context
- Run `/titanium:review` again if you make more changes

**Before /titanium:work**:
- Run `/titanium:plan` first if you want to review the plan separately
- Or let /titanium:work create the plan inline

---

**This command orchestrates the complete development workflow from requirements to reviewed implementation, with AI quality gates and voice feedback throughout.**
