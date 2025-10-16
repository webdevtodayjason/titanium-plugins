# Titanium Toolkit Orchestration System - Complete Implementation Plan

**Version**: 2.0.0
**Status**: Planning Phase
**Author**: Jason Brashear, Titanium Computing
**Date**: October 2025

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [Technical Constraints](#technical-constraints)
4. [System Architecture](#system-architecture)
5. [Component Specifications](#component-specifications)
6. [Implementation Timeline](#implementation-timeline)
7. [Testing Strategy](#testing-strategy)
8. [User Workflows](#user-workflows)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Future Enhancements](#future-enhancements)

---

## Executive Summary

### What We're Building

A complete workflow orchestration system for titanium-toolkit that transforms it from a collection of 16 standalone agents into a unified development workflow engine.

### Key Features

- **4 New Slash Commands**: `/titanium:plan`, `/titanium:work`, `/titanium:review`, `/titanium:status`
- **UV Utility Scripts**: File-based state management and AI-powered planning
- **MCP Integration**: vibe-check for quality gates, Pieces for memory
- **Voice Feedback**: Real-time announcements throughout workflow
- **BMAD Compatible**: Works with BMAD-generated PRDs

### Installation

Users install via the standard plugin marketplace:

```bash
/plugin marketplace add webdevtodayjason/titanium-plugins
/plugin install titanium-toolkit
```

No database, no external services, no complex setup required.

---

## The Problem We're Solving

### Current State

**What Titanium Toolkit Has:**
- ✅ 16 specialized builder agents
- ✅ 4 voice hooks (PostToolUse, Stop, SubagentStop, Notification)
- ✅ 8 MCP servers configured
- ✅ Utility modules for TTS and LLM calls
- ✅ 1 command: `/catchup`

**What's Missing:**
- ❌ NO workflow orchestration system
- ❌ NO commands to coordinate multi-agent workflows
- ❌ NO task breakdown and sequencing logic
- ❌ NO state management for tracking progress
- ❌ Relies on external `compounding-engineering` plugin for `/work` command

### The Gap Analysis

**compounding-engineering provides:**
- `/work` - Executes PRD with agent orchestration
- `/review` - Multi-agent parallel review
- `/plan` - Project planning
- Git worktree isolation
- Agent sequencing logic
- Task breakdown from PRD

**BMAD-METHOD teaches us:**
- Document-driven workflow (PRD → Stories → Implementation)
- Configuration files for project structure
- Story files as handoff mechanism between agents
- Sequential agent phases with fresh contexts
- Workflow definitions (YAML)
- Explicit status tracking with user approval

**Titanium needs:**
1. Workflow orchestration commands (slash commands)
2. Task breakdown and sequencing logic (utility scripts)
3. Agent coordination system (via Claude following instructions)
4. Project state management (file-based JSON)
5. Quality gates with AI oversight (vibe-check integration)

---

## Technical Constraints

### What Claude Code Plugins CAN Do

✅ **Slash Commands**: Markdown files with instructions for Claude
- Located in `commands/*.md`
- Contain instructions that Claude follows
- Can call utility scripts via bash
- Claude uses built-in tools (TodoWrite, Task, Read, Write, etc.)

✅ **Agents**: Markdown files defining specialized behavior
- Located in `agents/*.md`
- Define agent capabilities and instructions
- Launched via Task tool from Claude

✅ **Hooks**: Python scripts that run at lifecycle events
- Located in `hooks/*.py`
- Triggered by: PostToolUse, Stop, SubagentStop, Notification
- Can read stdin (JSON context from Claude)
- Can call external APIs, write logs, play sounds

✅ **UV Scripts**: Standalone Python utilities with inline dependencies
- Use `#!/usr/bin/env -S uv run --script` shebang
- Declare dependencies inline with `# /// script`
- Can be called from hooks or slash commands
- Can read/write files, call APIs, process data

✅ **MCP Servers**: External tool integrations
- Configured in `.mcp.json`
- Provide tools Claude can call directly
- Examples: vibe-check, Pieces, ElevenLabs, context7

✅ **File-Based Storage**: JSON/text files for state
- `.titanium/workflow-state.json` - Current workflow state
- `.titanium/plan.json` - Structured plan data
- `logs/*.json` - Activity logs

### What Claude Code Plugins CANNOT Do

❌ **Databases**: No SQLite, PostgreSQL, etc.
- Workaround: Use JSON files

❌ **Custom Orchestration Engines**: No custom code execution framework
- Workaround: Claude follows markdown instructions

❌ **New Hook Types**: Limited to 4 hook types (PostToolUse, Stop, SubagentStop, Notification)
- Workaround: Call utility scripts from hooks or commands

❌ **Workflow YAML Parsers**: No custom workflow engines
- Workaround: Use GPT-4 to parse requirements into JSON plans

❌ **Background Services**: No long-running daemons
- Workaround: All execution happens during Claude sessions

❌ **Custom Tool Types**: Can only use Claude's built-in tools + MCP
- Workaround: Wrap functionality in utility scripts

### Key Architectural Decisions

1. **Instructions, Not Code**: Orchestration happens through markdown instructions that Claude follows
2. **File-Based State**: JSON files instead of database
3. **UV for Utilities**: Standalone scripts with dependencies
4. **Claude Does the Work**: Commands tell Claude HOW to coordinate, Claude executes using built-in tools
5. **MCP for Intelligence**: vibe-check for quality gates, Pieces for memory

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interaction                          │
│                    /titanium:plan                                │
│                    /titanium:work                                │
│                    /titanium:review                              │
│                    /titanium:status                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code (Orchestrator)                    │
│  • Reads markdown command instructions                           │
│  • Uses built-in tools: TodoWrite, Task, memory, Read, Write    │
│  • Calls utility scripts via Bash                                │
│  • Launches agents via Task tool                                │
│  • Calls MCP tools: vibe-check, Pieces                          │
└────┬────────────────────┬─────────────────┬─────────────────────┘
     │                    │                 │
     ↓                    ↓                 ↓
┌──────────┐      ┌──────────────┐    ┌──────────────┐
│ UV Utils │      │  MCP Servers │    │ Voice Hooks  │
│          │      │              │    │              │
│ workflow │      │ vibe-check   │    │ post_tool_   │
│ _state   │      │ Pieces       │    │ use.py       │
│          │      │ ElevenLabs   │    │              │
│ plan_    │      │ context7     │    │ stop.py      │
│ parser   │      │              │    │              │
└────┬─────┘      └──────┬───────┘    └──────┬───────┘
     │                   │                   │
     ↓                   ↓                   ↓
┌─────────────────────────────────────────────────────────────────┐
│                       File System Storage                        │
│  • .titanium/workflow-state.json (workflow state)               │
│  • .titanium/plan.json (structured plan)                        │
│  • .titanium/plan.md (readable plan)                            │
│  • .titanium/requirements.md (input requirements)               │
│  • .titanium/review-report.md (review findings)                 │
│  • logs/voice_announcements.json (voice logs)                   │
│  • logs/quality_gates.json (quality gate results)               │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Requirements (PRD/User Input)
    ↓
/titanium:plan (command)
    ↓
plan_parser.py (GPT-4 breaks down into structure)
    ↓
.titanium/plan.json (structured data)
    ↓
vibe-check (validate plan quality)
    ↓
Pieces (store plan)
    ↓
/titanium:work (command)
    ↓
workflow_state.py (initialize state)
    ↓
Claude creates TodoWrite list from plan
    ↓
For each task:
    ├─ Launch agent via Task tool
    ├─ Agent executes work
    ├─ vibe-check validates progress
    ├─ Mark todo completed
    └─ Update workflow state
    ↓
/titanium:review (command)
    ↓
Launch review agents in parallel
    ↓
Aggregate findings
    ↓
vibe-check meta-review
    ↓
Create review report
    ↓
Store in Pieces
    ↓
Present to user
```

### State Management

**Workflow State** (`.titanium/workflow-state.json`):
```json
{
  "workflow_type": "development",
  "goal": "Implement user authentication",
  "status": "in_progress",
  "started_at": "2025-10-15T14:30:00Z",
  "current_phase": "implementation",
  "phases": [
    {
      "name": "planning",
      "status": "completed",
      "started_at": "2025-10-15T14:30:00Z",
      "completed_at": "2025-10-15T14:35:00Z"
    },
    {
      "name": "implementation",
      "status": "in_progress",
      "started_at": "2025-10-15T14:35:00Z"
    }
  ],
  "completed_tasks": ["Epic 1: Story 1 - Task 1"],
  "pending_tasks": ["Epic 1: Story 1 - Task 2", "Epic 1: Story 1 - Task 3"]
}
```

**Plan Structure** (`.titanium/plan.json`):
```json
{
  "epics": [
    {
      "name": "User Authentication",
      "description": "Complete authentication system",
      "stories": [
        {
          "name": "User Login",
          "description": "As a user, I can log in with email/password",
          "tasks": [
            {
              "name": "Create JWT middleware",
              "agent": "@api-developer",
              "estimated_time": "30m",
              "dependencies": []
            },
            {
              "name": "Implement login endpoint",
              "agent": "@api-developer",
              "estimated_time": "45m",
              "dependencies": ["Create JWT middleware"]
            }
          ]
        }
      ]
    }
  ],
  "agents_needed": ["@api-developer", "@frontend-developer", "@test-runner"],
  "estimated_total_time": "4h"
}
```

---

## Component Specifications

### 1. Utility Scripts

#### 1.1 workflow_state.py

**Location**: `plugins/titanium-toolkit/hooks/utils/workflow/workflow_state.py`

**Purpose**: Manage workflow state via file-based JSON storage

**Dependencies**:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///
```

**Commands**:

```bash
# Initialize new workflow
uv run workflow_state.py init "$(pwd)" "development" "Implement user auth"

# Update current phase
uv run workflow_state.py update_phase "$(pwd)" "implementation" "in_progress"

# Get current state
uv run workflow_state.py get "$(pwd)"

# Mark workflow complete
uv run workflow_state.py complete "$(pwd)"
```

**State File**: `.titanium/workflow-state.json`

**Functions**:

1. `init_workflow(project_path, workflow_type, goal)` → Creates new workflow state
2. `update_phase(project_path, phase_name, status)` → Updates current phase
3. `get_state(project_path)` → Returns current state dict
4. `complete_workflow(project_path)` → Marks workflow as done

**Example Output**:
```json
{
  "workflow_type": "development",
  "goal": "Implement user authentication",
  "status": "planning",
  "started_at": "2025-10-15T14:30:00Z",
  "current_phase": "planning",
  "phases": [],
  "completed_tasks": [],
  "pending_tasks": []
}
```

**Implementation Details**:
- Creates `.titanium/` directory if it doesn't exist
- Stores ISO 8601 timestamps
- Phases: `planning`, `implementation`, `review`, `completed`
- Thread-safe file operations (atomic writes)

---

#### 1.2 plan_parser.py

**Location**: `plugins/titanium-toolkit/hooks/utils/workflow/plan_parser.py`

**Purpose**: Use GPT-4 to break down requirements into structured implementation plan

**Dependencies**:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "openai",
# ]
# ///
```

**Commands**:

```bash
# Parse requirements file into plan
uv run plan_parser.py .titanium/requirements.md "$(pwd)"
```

**Input**: Requirements markdown file
**Output**:
- `.titanium/plan.json` (structured data)
- JSON to stdout

**Functions**:

1. `parse_requirements_to_plan(requirements_text, project_path)` → Generates plan using GPT-4

**GPT-4 Prompt Structure**:
```
Analyze these requirements and create a structured implementation plan.

Requirements:
{requirements_text}

Create a JSON plan with this structure:
{
  "epics": [...],
  "agents_needed": [...],
  "estimated_total_time": "..."
}

Use these available agents:
- @product-manager (requirements validation)
- @api-developer (backend APIs)
- @frontend-developer (UI/UX)
[...etc]

Return ONLY valid JSON, no explanations.
```

**Model Used**: `gpt-4o`
**Temperature**: `0.3` (deterministic planning)
**Max Tokens**: `2000`

**Example Output**:
```json
{
  "epics": [
    {
      "name": "Backend API",
      "description": "RESTful API with authentication",
      "stories": [
        {
          "name": "JWT Middleware",
          "description": "Create JWT authentication middleware",
          "tasks": [
            {
              "name": "Install JWT library",
              "agent": "@api-developer",
              "estimated_time": "15m",
              "dependencies": []
            },
            {
              "name": "Create auth middleware",
              "agent": "@api-developer",
              "estimated_time": "30m",
              "dependencies": ["Install JWT library"]
            }
          ]
        }
      ]
    }
  ],
  "agents_needed": ["@api-developer", "@test-runner"],
  "estimated_total_time": "3h"
}
```

**Error Handling**:
- Validates JSON output from GPT-4
- Strips markdown code fences if present
- Falls back to simple structure if parsing fails

---

### 2. Slash Commands

#### 2.1 /titanium:plan

**File**: `plugins/titanium-toolkit/commands/titanium-plan.md`

**Purpose**: Analyze requirements and create detailed implementation plan

**Front Matter**:
```yaml
---
description: Analyze requirements and create detailed implementation plan
---
```

**Workflow**:

1. **Gather Requirements**
   - If user provides file path → Read it
   - If user provides inline description → Write to `.titanium/requirements.md`
   - Ask clarifying questions if needed

2. **Generate Structured Plan**
   ```bash
   uv run hooks/utils/workflow/plan_parser.py .titanium/requirements.md "$(pwd)"
   ```

3. **Review Plan**
   - Read `.titanium/plan.json`
   - Verify agent assignments are appropriate
   - Check for logical dependencies

4. **Validate with vibe-check**
   ```
   mcp__vibe-check__vibe_check(
     goal: "User's stated goal from requirements",
     plan: "Summary of the generated plan",
     uncertainties: ["Any concerns"]
   )
   ```

5. **Revise if Needed**
   - If vibe-check raises concerns → Adjust and re-parse
   - Validate again until approved

6. **Create Readable Format**
   - Write `.titanium/plan.md` with formatted plan
   - Include: goals, phases, timeline, agent assignments

7. **Store in Pieces**
   ```
   mcp__Pieces__create_pieces_memory(
     summary_description: "Implementation plan for [project]",
     summary: "Plan with X epics, Y stories, Z tasks...",
     files: [".titanium/plan.json", ".titanium/plan.md", ".titanium/requirements.md"],
     project: "$(pwd)"
   )
   ```

8. **Present to User**
   - Show high-level structure
   - Provide time estimates
   - List agents involved
   - Ask for approval

**Output Format**:
```
📋 Implementation Plan Created

🎯 Goal: Implement user authentication

📦 Structure:
- 2 epics
- 5 stories
- 12 implementation tasks

⏱️ Estimated Time: 4 hours

🤖 Agents Involved:
- @product-manager (requirements)
- @api-developer (backend)
- @frontend-developer (UI)
- @test-runner (testing)

📁 Plan saved to:
- .titanium/plan.json (structured data)
- .titanium/plan.md (readable format)

✅ vibe-check validated: Plan structure is sound, dependencies are clear

Ready to execute? Run: /titanium:work
```

**Usage Examples**:

```bash
# With BMAD PRD file
/titanium:plan ~/bmad/output/user-auth-prd.md

# With inline description
/titanium:plan
User: "I need to add JWT authentication with login, register, and password reset"

# With GitHub issue
/titanium:plan https://github.com/org/repo/issues/123
```

---

#### 2.2 /titanium:work

**File**: `plugins/titanium-toolkit/commands/titanium-work.md`

**Purpose**: Execute a multi-phase development workflow with agent orchestration

**Front Matter**:
```yaml
---
description: Execute a multi-phase development workflow with agent orchestration
---
```

**Workflow Phases**:

##### Phase 1: Pre-Flight Checks

1. **Determine Project Path**: Use current working directory
2. **Check for Existing Plan**: Look for `.titanium/plan.json`
3. **Initialize Workflow State**:
   ```bash
   uv run hooks/utils/workflow/workflow_state.py init "$(pwd)" "development" "User's goal"
   ```

##### Phase 2: Planning (if no plan exists)

1. **Read or Create Requirements**:
   - If user provided file → Read it
   - If inline → Write to `.titanium/requirements.md`

2. **Parse Requirements**:
   ```bash
   uv run hooks/utils/workflow/plan_parser.py .titanium/requirements.md "$(pwd)"
   ```

3. **Validate with vibe-check**:
   ```
   mcp__vibe-check__vibe_check(
     goal: "User's goal",
     plan: "Summary from plan.json",
     uncertainties: ["Any concerns"]
   )
   ```

4. **Create TodoWrite List**:
   - Read `.titanium/plan.json`
   - Create todo for each task
   - Format: `"Epic: Story - Task (Agent: @agent-name)"`

5. **Update State**:
   ```bash
   uv run hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "planning" "completed"
   ```

6. **Store in Pieces**:
   ```
   mcp__Pieces__create_pieces_memory(
     summary_description: "Implementation plan",
     summary: "Complete breakdown...",
     files: [".titanium/plan.json", ".titanium/requirements.md"],
     project: "$(pwd)"
   )
   ```

7. **Get User Approval** before proceeding to implementation

##### Phase 3: Implementation

1. **Update State**:
   ```bash
   uv run hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "implementation" "in_progress"
   ```

2. **For Each Task** (sequential execution):

   a. **Mark in_progress** in TodoWrite

   b. **Identify Agent** from task metadata in plan

   c. **Launch Agent**:
      ```
      Task(
        description: "Task name",
        prompt: "Detailed instructions with context",
        subagent_type: "agent-type"
      )
      ```

   d. **Wait for Completion** (one agent at a time)

   e. **Quality Check**:
      - Run tests if applicable
      - Call vibe-check:
        ```
        mcp__vibe-check__vibe_check(
          goal: "Overall goal",
          plan: "Current task",
          progress: "What was accomplished"
        )
        ```
      - If concerns → Address before proceeding

   f. **Mark Completed** immediately in TodoWrite

   g. **Store Progress** (after each epic):
      ```
      mcp__Pieces__create_pieces_memory(
        summary_description: "Completed [epic name]",
        summary: "Details...",
        files: [modified files],
        project: "$(pwd)"
      )
      ```

##### Phase 4: Review

1. **Update State**:
   ```bash
   uv run hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "review" "in_progress"
   ```

2. **Launch Review Agents in Parallel** (single message, multiple Task calls):
   ```
   [Task 1]: @code-reviewer - "Review all changes"
   [Task 2]: @security-scanner - "Scan for vulnerabilities"
   [Task 3]: @tdd-specialist - "Check test coverage"
   ```

3. **Aggregate Findings**:
   - Collect results from all agents
   - Categorize by severity (critical, important, nice-to-have)
   - Create `.titanium/review-report.md`

4. **Final vibe-check**:
   ```
   mcp__vibe-check__vibe_check(
     goal: "Original goal",
     plan: "What was planned",
     progress: "What was completed + review findings"
   )
   ```

5. **Store Review**:
   ```
   mcp__Pieces__create_pieces_memory(
     summary_description: "Quality review findings",
     summary: "X critical, Y important, Z minor issues...",
     files: [".titanium/review-report.md", reviewed files]
   )
   ```

##### Phase 5: Completion

1. **Mark Complete**:
   ```bash
   uv run hooks/utils/workflow/workflow_state.py complete "$(pwd)"
   ```

2. **Final Pieces Memory**:
   ```
   mcp__Pieces__create_pieces_memory(
     summary_description: "Completed: [goal]",
     summary: "Full workflow summary...",
     files: [all project files],
     project: "$(pwd)"
   )
   ```

3. **Present Summary**:
   - What was accomplished
   - Review findings (if any issues)
   - Suggested next steps

**Important Rules**:
- ✅ ALWAYS use TodoWrite for tracking
- ✅ NEVER skip vibe-check quality gates
- ✅ ALWAYS launch agents sequentially (one at a time)
- ✅ Mark todos completed IMMEDIATELY after finishing
- ✅ Use workflow_state.py to track phases
- ✅ Store major milestones in Pieces
- ✅ Voice hooks automatically announce progress
- ✅ Get user approval after planning before implementation

**Usage Examples**:

```bash
# With existing plan
/titanium:work

# With new requirements
/titanium:work
User: "I need to add user authentication with JWT"

# From BMAD PRD
/titanium:work ~/bmad/output/prd.md
```

---

#### 2.3 /titanium:review

**File**: `plugins/titanium-toolkit/commands/titanium-review.md`

**Purpose**: Run comprehensive multi-agent quality review

**Front Matter**:
```yaml
---
description: Run comprehensive multi-agent quality review
---
```

**Workflow**:

1. **Identify Review Scope**
   - Check recent git changes: `git diff --name-only HEAD~1`
   - Or review all code if specified by user
   - Get list of files to review

2. **Launch Review Agents in Parallel**

   Send **single message** with **multiple Task calls**:

   ```
   [Task 1]: @code-reviewer
   Prompt: "Review code for quality, readability, best practices. Focus on: [files]"

   [Task 2]: @security-scanner
   Prompt: "Scan for security vulnerabilities. Focus on: [files]"

   [Task 3]: @tdd-specialist
   Prompt: "Check test coverage and quality. Verify tests for: [files]"
   ```

3. **Wait for All Agents** (they run concurrently)

4. **Aggregate Findings**

   Collect results and categorize:

   - 🔴 **Critical** (must fix before deployment)
     - Security vulnerabilities
     - Breaking changes
     - Data loss risks

   - 🟡 **Important** (should fix soon)
     - Code smells
     - Missing tests
     - Performance issues

   - 🟢 **Nice-to-have** (optional improvements)
     - Refactoring opportunities
     - Documentation gaps
     - Style inconsistencies

5. **Meta-Review with vibe-check**
   ```
   mcp__vibe-check__vibe_check(
     goal: "Quality review of implementation",
     plan: "Ran code-reviewer, security-scanner, tdd-specialist",
     progress: "Findings: [summary]",
     uncertainties: ["Are there systemic issues?"]
   )
   ```

6. **Create Review Report**

   Write `.titanium/review-report.md`:

   ```markdown
   # Quality Review Report

   **Date**: 2025-10-15
   **Reviewers**: @code-reviewer, @security-scanner, @tdd-specialist
   **Files Reviewed**: 12 files

   ## Summary
   - Critical issues: 1
   - Important issues: 3
   - Nice-to-have: 5

   ## Critical Issues 🔴

   ### SQL Injection Vulnerability
   **File**: `src/api/users.ts:45`
   **Severity**: Critical
   **Description**: User input not sanitized before SQL query
   **Recommendation**: Use parameterized queries

   ## Important Issues 🟡

   ### Missing Error Handling
   **File**: `src/api/auth.ts:23`
   **Severity**: Important
   **Description**: No try-catch around async operation
   **Recommendation**: Add error handling

   ### Insufficient Test Coverage
   **File**: `src/services/payment.ts`
   **Severity**: Important
   **Description**: Critical payment logic has no tests
   **Recommendation**: Add unit tests for edge cases

   ## Nice-to-have 🟢

   ### Extract Duplicated Logic
   **Files**: `src/api/users.ts`, `src/api/products.ts`
   **Description**: Similar validation logic duplicated
   **Recommendation**: Extract to shared utility function

   ## vibe-check Meta-Review

   "The critical SQL injection vulnerability needs immediate attention.
   The missing error handling in auth.ts could cause runtime crashes.
   Test coverage gaps are concerning for payment logic. Overall code
   quality is good, but security and testing need improvement."
   ```

7. **Store in Pieces**
   ```
   mcp__Pieces__create_pieces_memory(
     summary_description: "Quality review findings",
     summary: "Review complete: 1 critical, 3 important, 5 minor. Critical: SQL injection in users.ts:45",
     files: [".titanium/review-report.md", all reviewed files],
     project: "$(pwd)"
   )
   ```

8. **Present Summary**

   Voice announcement + formatted output:

   ```
   🔍 Quality Review Complete

   🔴 1 Critical Issue
   🟡 3 Important Issues
   🟢 5 Nice-to-have Improvements

   📄 Report: .titanium/review-report.md

   ⚠️  Action Required:
   1. Fix SQL injection in src/api/users.ts:45
   2. Add error handling to src/api/auth.ts:23
   3. Add tests for src/services/payment.ts
   ```

**Review Agent Roles**:

- **@code-reviewer**: Code quality, readability, best practices, DRY, SOLID
- **@security-scanner**: Security vulnerabilities, input validation, auth issues
- **@tdd-specialist**: Test coverage, test quality, edge cases

**Usage Examples**:

```bash
# Review recent changes
/titanium:review

# Review specific files
/titanium:review src/api/*.ts

# Review entire codebase
/titanium:review --all
```

---

#### 2.4 /titanium:status

**File**: `plugins/titanium-toolkit/commands/titanium-status.md`

**Purpose**: Show current workflow progress and status

**Front Matter**:
```yaml
---
description: Show current workflow progress and status
---
```

**Workflow**:

1. **Check for Active Workflow**
   ```bash
   uv run hooks/utils/workflow/workflow_state.py get "$(pwd)"
   ```
   Reads `.titanium/workflow-state.json`

2. **If Workflow Exists** → Show status

3. **Query Pieces for Context**
   ```
   mcp__Pieces__ask_pieces_ltm(
     question: "What work has been done in the last session on this project at $(pwd)?",
     chat_llm: "claude-sonnet-4-5"
   )
   ```

4. **Check for Plan**
   - Read `.titanium/plan.json` if exists
   - Calculate epic/story progress
   - Identify current task

5. **Present Status Report**

   ```
   📊 Workflow Status

   🎯 Goal: Implement user authentication
   📍 Phase: Implementation (in progress)
   ⏱️  Started: Oct 15, 2025 at 2:30 PM

   ✅ Completed: 8 tasks
   ⏳ Pending: 4 tasks
   🔄 Current: "Create login form component"

   📈 Progress: 67% complete
   ⏰ Est. Remaining: 1.5 hours

   📝 Recent Work (from Pieces):
   "Completed backend API with JWT authentication.
   All endpoints tested and passing. Currently working
   on frontend login form component."

   🤖 Active Agent: @frontend-developer

   Next Steps:
   - Complete login form component (current)
   - Add password reset flow
   - Write E2E tests
   - Run quality review
   ```

6. **Offer Voice Summary**
   - Ask user if they want status spoken
   - Use concise summary for TTS

**Status Calculation**:

```python
total_tasks = len(completed_tasks) + len(pending_tasks)
progress_pct = (len(completed_tasks) / total_tasks) * 100

remaining_time = sum(task['estimated_time'] for task in pending_tasks)
```

**Usage Examples**:

```bash
# Check current status
/titanium:status

# Get voice summary
/titanium:status --voice

# Show detailed breakdown
/titanium:status --verbose
```

---

### 3. Voice Hooks (Enhancements)

#### 3.1 post_tool_use_elevenlabs.py (Enhanced)

**Current Behavior**:
- Announces tool completions (Write, Edit, Task)
- Skips certain tools (TodoWrite, Grep, Read, etc.)
- Uses GPT-5 nano for summaries

**Enhancements Needed**:

1. **Detect Agent Launches**
   - When Task tool launches an agent
   - Announce: "Launching @api-developer for backend implementation"

2. **Detect Workflow Phase Changes**
   - When workflow_state.py is called
   - Announce: "Starting implementation phase"

3. **More Specific Announcements**
   - Current: "Agent task completed"
   - Enhanced: "API endpoints created and tested"

**Implementation**:

```python
# In get_simple_summary()
if tool_name == "Task":
    # Extract more context
    subagent = tool_input.get("subagent_type", "")
    desc = tool_input.get("description", "")

    if subagent:
        return f"Launching {subagent} for {desc}"

    # Check tool_response for completion info
    if tool_response and "output" in tool_response:
        output = tool_response["output"]
        # Parse output for meaningful summary
        if "completed" in output.lower():
            return f"{subagent} completed {desc}"
```

**No Changes to Hook Triggers** - Still uses PostToolUse event

---

#### 3.2 workflow_phase.py (New Hook)

**Location**: `plugins/titanium-toolkit/hooks/workflow_phase.py`

**Purpose**: Announce workflow phase transitions

**Trigger**: Called manually from workflow commands (not a new hook type)

**Usage**:
```bash
# From /titanium:work command
uv run hooks/workflow_phase.py "planning"
uv run hooks/workflow_phase.py "implementation"
uv run hooks/workflow_phase.py "review"
uv run hooks/workflow_phase.py "completed"
```

**Dependencies**:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///
```

**Functions**:

```python
def announce_phase(phase_name):
    """Announce workflow phase transition with voice"""

    messages = {
        "planning": "Starting planning phase",
        "implementation": "Beginning implementation",
        "review": "Starting quality review",
        "completed": "Workflow complete"
    }

    message = messages.get(phase_name, f"{phase_name} phase")

    # Try ElevenLabs via TTS script
    script_dir = Path(__file__).parent
    tts_script = script_dir / "utils" / "tts" / "elevenlabs_tts.py"

    try:
        subprocess.run(
            ["uv", "run", str(tts_script), message],
            capture_output=True,
            timeout=10
        )
    except:
        # Fallback to macOS say
        subprocess.run(["say", message], timeout=5)
```

**Logging**:
```python
# Log phase transitions
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "phase": phase_name,
    "message": message
}

log_file = Path.home() / "logs" / "workflow_phases.json"
log_file.parent.mkdir(parents=True, exist_ok=True)

with open(log_file, "a") as f:
    f.write(json.dumps(log_entry) + "\n")
```

---

### 4. MCP Integration

#### 4.1 vibe-check Integration

**When to Use vibe-check**:

1. **After Plan Generation** (`/titanium:plan`)
   - Validate plan structure
   - Check for complexity issues
   - Identify missing considerations

2. **After Each Agent** (`/titanium:work`)
   - Validate progress against plan
   - Check for deviations
   - Identify blockers

3. **After Each Epic** (`/titanium:work`)
   - Validate epic completion
   - Check for integration issues
   - Assess readiness for next epic

4. **After Review** (`/titanium:review`)
   - Meta-review of findings
   - Identify systemic issues
   - Validate completeness

**Example Call**:
```
mcp__vibe-check__vibe_check(
  goal: "Implement JWT authentication system",
  plan: "Create middleware, login/register endpoints, password reset",
  progress: "Completed JWT middleware and login endpoint",
  uncertainties: [
    "Should we use bcrypt or argon2 for password hashing?",
    "Need to decide on token refresh strategy"
  ]
)
```

**Response Handling**:
```
vibe_result = {
  "concerns": [
    "Consider using argon2 - more resistant to GPU attacks",
    "Token refresh strategy should be decided before register endpoint"
  ],
  "suggestions": [
    "Add rate limiting to prevent brute force",
    "Consider adding 2FA support in the architecture"
  ]
}

# If concerns exist → Address before proceeding
if vibe_result['concerns']:
    # Pause workflow
    # Present concerns to user
    # Get approval to proceed or adjust approach
```

**Configuration** (in `~/.vibe-check/.env`):
```bash
GEMINI_API_KEY=your_key_here
DEFAULT_LLM_PROVIDER=gemini
```

---

#### 4.2 Pieces Integration

**When to Use Pieces**:

1. **After Plan Creation** (`/titanium:plan`)
   - Store structured plan
   - Store requirements document
   - Create searchable memory

2. **After Each Epic** (`/titanium:work`)
   - Store milestone completion
   - Save modified files
   - Document decisions made

3. **After Review** (`/titanium:review`)
   - Store review findings
   - Save review report
   - Track issues discovered

4. **At Workflow Completion** (`/titanium:work`)
   - Store final summary
   - Save all project files
   - Create comprehensive memory

5. **For Context Recovery** (`/catchup`)
   - Query previous work
   - Resume interrupted sessions
   - Understand project history

**Example Calls**:

**Store Plan**:
```
mcp__Pieces__create_pieces_memory(
  summary_description: "Implementation plan for user authentication",
  summary: "Plan created with 2 epics, 5 stories, 12 tasks. Agents: @api-developer, @frontend-developer, @test-runner. Estimated time: 4 hours. Key decisions: Using JWT with refresh tokens, argon2 for password hashing, rate limiting on auth endpoints.",
  files: [
    ".titanium/plan.json",
    ".titanium/plan.md",
    ".titanium/requirements.md"
  ],
  project: "/Users/sem/projects/my-app"
)
```

**Store Epic Completion**:
```
mcp__Pieces__create_pieces_memory(
  summary_description: "Completed Epic: Backend Authentication API",
  summary: "Implemented JWT authentication system with login, register, and password reset endpoints. All endpoints tested and passing. Used argon2 for password hashing. Added rate limiting middleware. 15 tests created, all passing.",
  files: [
    "src/middleware/auth.ts",
    "src/api/auth/login.ts",
    "src/api/auth/register.ts",
    "src/api/auth/reset-password.ts",
    "tests/auth/*.test.ts"
  ],
  project: "/Users/sem/projects/my-app",
  externalLinks: [
    "https://github.com/org/repo/compare/main...feature/auth"
  ]
)
```

**Query Context**:
```
mcp__Pieces__ask_pieces_ltm(
  question: "What authentication work has been completed on this project?",
  chat_llm: "claude-sonnet-4-5",
  topics: ["authentication", "JWT", "security"],
  application_sources: ["Code"]
)
```

**Configuration** (requires Pieces OS + CLI):
```bash
# Install Pieces OS
# Download from https://pieces.app

# Install Pieces CLI
pip3 install --upgrade pieces-cli

# Configure MCP
pieces mcp setup claude_code --stdio

# Enable LTM in Pieces app settings
```

---

## Implementation Timeline

### Week 1: Foundation (Utility Scripts + Planning Command)

**Goals**:
- Create utility scripts for state management
- Create `/titanium:plan` command
- Test plan generation workflow

**Tasks**:

**Day 1-2: Utility Scripts**
- [ ] Create `hooks/utils/workflow/` directory
- [ ] Write `workflow_state.py` with all functions
- [ ] Write `plan_parser.py` with GPT-4 integration
- [ ] Test scripts standalone:
  ```bash
  # Test workflow_state.py
  uv run workflow_state.py init "$(pwd)" "test" "Test workflow"
  uv run workflow_state.py get "$(pwd)"
  uv run workflow_state.py update_phase "$(pwd)" "planning" "completed"
  uv run workflow_state.py complete "$(pwd)"

  # Test plan_parser.py
  echo "Create a user authentication system with JWT" > test-req.md
  uv run plan_parser.py test-req.md "$(pwd)"
  cat .titanium/plan.json
  ```

**Day 3-4: Planning Command**
- [ ] Create `commands/titanium-plan.md`
- [ ] Write detailed markdown instructions
- [ ] Test with sample requirements
- [ ] Verify vibe-check integration
- [ ] Verify Pieces storage
- [ ] Test with BMAD PRD files

**Day 5: Testing & Refinement**
- [ ] Test plan command with various inputs:
  - Simple requirements
  - Complex multi-epic projects
  - BMAD-generated PRDs
- [ ] Refine GPT-4 prompt for better plans
- [ ] Document plan.json schema
- [ ] Create example plans

**Deliverables**:
- ✅ `workflow_state.py` working
- ✅ `plan_parser.py` working
- ✅ `/titanium:plan` command functional
- ✅ Documentation for Week 1 components

---

### Week 2: Execution (Work Command)

**Goals**:
- Create `/titanium:work` command
- Test full orchestration flow
- Integrate quality gates
- Test memory integration

**Tasks**:

**Day 1-2: Work Command Structure**
- [ ] Create `commands/titanium-work.md`
- [ ] Write Phase 1: Pre-Flight Checks instructions
- [ ] Write Phase 2: Planning instructions
- [ ] Write Phase 3: Implementation instructions
- [ ] Write Phase 4: Review instructions
- [ ] Write Phase 5: Completion instructions

**Day 3: vibe-check Integration**
- [ ] Add vibe-check calls after plan generation
- [ ] Add vibe-check calls after each agent
- [ ] Add vibe-check calls after each epic
- [ ] Add vibe-check call for final review
- [ ] Test vibe-check responses and handling

**Day 4: Pieces Integration**
- [ ] Add Pieces memory after plan creation
- [ ] Add Pieces memory after each epic
- [ ] Add Pieces memory for review findings
- [ ] Add Pieces memory for final completion
- [ ] Test context recovery with `/catchup`

**Day 5: End-to-End Testing**
- [ ] Test simple workflow (1 epic, 2 stories)
- [ ] Test complex workflow (3 epics, 10 stories)
- [ ] Test with actual BMAD PRDs
- [ ] Verify TodoWrite tracking works
- [ ] Verify voice announcements work
- [ ] Verify state transitions work
- [ ] Document any issues

**Deliverables**:
- ✅ `/titanium:work` command functional
- ✅ Full workflow orchestration working
- ✅ vibe-check integrated
- ✅ Pieces integrated
- ✅ Voice announcements working

---

### Week 3: Review & Status (Supporting Commands)

**Goals**:
- Create `/titanium:review` command
- Create `/titanium:status` command
- Enhance voice hooks
- Test parallel agent execution

**Tasks**:

**Day 1-2: Review Command**
- [ ] Create `commands/titanium-review.md`
- [ ] Write parallel agent launch instructions
- [ ] Write findings aggregation instructions
- [ ] Write report generation instructions
- [ ] Test parallel execution:
  ```bash
  # Should launch all 3 agents at once
  /titanium:review
  ```
- [ ] Verify report format
- [ ] Test vibe-check meta-review

**Day 3: Status Command**
- [ ] Create `commands/titanium-status.md`
- [ ] Write state reading instructions
- [ ] Write Pieces query instructions
- [ ] Write progress calculation instructions
- [ ] Test status reporting:
  - During planning
  - During implementation
  - During review
  - After completion

**Day 4: Voice Hook Enhancements**
- [ ] Update `post_tool_use_elevenlabs.py`:
  - Detect agent launches
  - More specific announcements
  - Better Task tool handling
- [ ] Create `workflow_phase.py` hook
- [ ] Test phase announcements
- [ ] Test agent launch announcements

**Day 5: Integration Testing**
- [ ] Test complete workflow with all commands:
  ```bash
  /titanium:plan requirements.md
  /titanium:work
  /titanium:status
  /titanium:review
  /titanium:status
  ```
- [ ] Verify all voice announcements
- [ ] Verify all state transitions
- [ ] Verify all Pieces memories created
- [ ] Test error scenarios

**Deliverables**:
- ✅ `/titanium:review` command functional
- ✅ `/titanium:status` command functional
- ✅ Enhanced voice hooks
- ✅ Full integration tested

---

### Week 4: Documentation, Examples & Release

**Goals**:
- Write comprehensive documentation
- Create workflow examples
- Test across multiple projects
- Prepare for release

**Tasks**:

**Day 1: Documentation**
- [ ] Write `docs/ORCHESTRATION.md` (comprehensive guide)
- [ ] Write `docs/WORKFLOW_EXAMPLES.md`
- [ ] Write `docs/TROUBLESHOOTING.md`
- [ ] Update main `README.md` with new commands
- [ ] Update `plugins/titanium-toolkit/README.md`
- [ ] Document all utility scripts
- [ ] Document all slash commands
- [ ] Create architecture diagrams

**Day 2: Examples**
- [ ] Create `docs/examples/fullstack-feature.md`
- [ ] Create `docs/examples/bug-fix-workflow.md`
- [ ] Create `docs/examples/refactor-workflow.md`
- [ ] Create `docs/examples/api-development.md`
- [ ] Create sample PRDs for testing
- [ ] Record video walkthrough

**Day 3: Testing Across Projects**
- [ ] Test with Node.js/Express project
- [ ] Test with React/Next.js project
- [ ] Test with Python/FastAPI project
- [ ] Test with Ruby on Rails project
- [ ] Test with different project sizes:
  - Small (1-2 epics)
  - Medium (3-5 epics)
  - Large (6+ epics)
- [ ] Document any edge cases

**Day 4: Polish & Bug Fixes**
- [ ] Fix any bugs found during testing
- [ ] Improve error messages
- [ ] Improve voice announcement quality
- [ ] Optimize GPT-4 prompts
- [ ] Add input validation
- [ ] Add graceful error handling

**Day 5: Release Preparation**
- [ ] Update version to 2.0.0 in `plugin.json`
- [ ] Write CHANGELOG.md
- [ ] Create release notes
- [ ] Test installation from marketplace:
  ```bash
  /plugin marketplace add webdevtodayjason/titanium-plugins
  /plugin install titanium-toolkit
  ```
- [ ] Verify all features work after installation
- [ ] Tag release: `git tag v2.0.0`
- [ ] Push to GitHub
- [ ] Announce release

**Deliverables**:
- ✅ Complete documentation
- ✅ Working examples
- ✅ Tested across project types
- ✅ v2.0.0 released
- ✅ GitHub marketplace updated

---

## Testing Strategy

### Unit Testing

**Utility Scripts**:

```bash
# Test workflow_state.py
cd plugins/titanium-toolkit/hooks/utils/workflow

# Test init
uv run workflow_state.py init "/tmp/test-project" "development" "Test goal"
# Expected: .titanium/workflow-state.json created

# Test get
uv run workflow_state.py get "/tmp/test-project"
# Expected: JSON output with initial state

# Test update_phase
uv run workflow_state.py update_phase "/tmp/test-project" "implementation" "in_progress"
# Expected: Updated JSON with new phase

# Test complete
uv run workflow_state.py complete "/tmp/test-project"
# Expected: JSON with completed status
```

```bash
# Test plan_parser.py
echo "Create a user authentication system with JWT, including login, register, and password reset features" > /tmp/test-req.md

uv run plan_parser.py /tmp/test-req.md "/tmp/test-project"
# Expected: .titanium/plan.json created with epics/stories/tasks
# Expected: Valid JSON structure
# Expected: Agent assignments present
```

### Integration Testing

**Test Scenarios**:

1. **Simple Workflow** (30 min)
   ```
   Requirements: "Add a contact form with name, email, message fields"
   Expected: 1 epic, 2 stories, 5 tasks
   Agents: @frontend-developer, @test-runner
   ```

2. **Medium Workflow** (2 hours)
   ```
   Requirements: "Add user authentication with JWT"
   Expected: 2 epics, 5 stories, 12 tasks
   Agents: @api-developer, @frontend-developer, @test-runner, @security-scanner
   ```

3. **Complex Workflow** (4 hours)
   ```
   Requirements: "Build complete e-commerce checkout flow"
   Expected: 3 epics, 10 stories, 25 tasks
   Agents: @api-developer, @frontend-developer, @devops-engineer, @test-runner, @security-scanner, @doc-writer
   ```

### End-to-End Testing

**Complete Workflow Test**:

```bash
# 1. Create test project
mkdir /tmp/test-auth-system
cd /tmp/test-auth-system
git init

# 2. Create requirements
cat > requirements.md << 'EOF'
# User Authentication System

## Requirements
- JWT-based authentication
- Login endpoint (POST /api/auth/login)
- Register endpoint (POST /api/auth/register)
- Password reset flow (email + token)
- Refresh token mechanism
- Rate limiting on auth endpoints

## Tech Stack
- Node.js + Express
- PostgreSQL
- Jest for testing
EOF

# 3. Create plan
/titanium:plan requirements.md

# Verify:
# - .titanium/plan.json exists
# - Plan includes appropriate epics/stories
# - Agents assigned correctly
# - Time estimates reasonable
# - vibe-check passed

# 4. Execute workflow
/titanium:work

# Verify:
# - TodoWrite list created
# - Agents launched sequentially
# - Voice announcements for each agent
# - vibe-check called after each agent
# - Tasks marked completed
# - Pieces memories created
# - Code files created

# 5. Check status mid-workflow
/titanium:status

# Verify:
# - Shows current phase
# - Shows completed vs pending tasks
# - Shows progress percentage
# - Queries Pieces correctly

# 6. Run review
/titanium:review

# Verify:
# - Three agents launched in parallel
# - Review report created
# - Findings categorized by severity
# - vibe-check meta-review
# - Pieces memory created

# 7. Check final status
/titanium:status

# Verify:
# - Shows completed status
# - Shows 100% progress
# - Shows review findings summary

# 8. Test context recovery
# (New session)
/catchup

# Verify:
# - Pieces returns project summary
# - Shows what was completed
# - Shows where we left off
```

### Error Scenario Testing

**Test Error Handling**:

1. **Missing OpenAI API Key**
   ```bash
   unset OPENAI_API_KEY
   /titanium:plan requirements.md
   # Expected: Clear error message, fallback behavior
   ```

2. **Invalid Requirements**
   ```bash
   echo "Invalid" > requirements.md
   /titanium:plan requirements.md
   # Expected: GPT-4 requests clarification or makes best effort
   ```

3. **Agent Failure**
   ```bash
   # Simulate agent failure during /titanium:work
   # Expected: Workflow pauses, reports error, allows retry
   ```

4. **vibe-check Concerns**
   ```bash
   # When vibe-check raises concerns
   # Expected: Workflow pauses, presents concerns, asks for user decision
   ```

5. **No Git Repository**
   ```bash
   cd /tmp/no-git-project
   /titanium:work
   # Expected: Works anyway, no git-dependent features
   ```

---

## User Workflows

### Workflow 1: BMAD PRD to Implementation

**Scenario**: User has created PRD using BMAD-METHOD

**Steps**:

```bash
# 1. User creates PRD with BMAD
cd ~/projects/new-feature
npx bmad-method

# Result: ~/bmad/output/feature-prd.md created

# 2. User creates plan from PRD
claude
/titanium:plan ~/bmad/output/feature-prd.md

# Claude:
# - Reads PRD
# - Calls plan_parser.py with GPT-4
# - Generates structured plan
# - Validates with vibe-check
# - Stores in Pieces
# - Presents plan to user

User: "Looks good, proceed"

# 3. User executes workflow
/titanium:work

# Claude:
# - Creates TodoWrite list from plan
# - Launches @product-manager to validate requirements
# - Voice: "Requirements validated, moving to backend"
# - Launches @api-developer for backend
# - Voice: "API endpoints created, 12 tests passing"
# - vibe-check: "Progress looks good, continue"
# - Launches @frontend-developer for UI
# - Voice: "3 components created, building..."
# - Launches @test-runner
# - Voice: "All tests passing, ready for review"
# - Creates review report
# - Presents summary

# 4. User checks quality
/titanium:review

# Claude:
# - Launches @code-reviewer, @security-scanner, @tdd-specialist in parallel
# - Aggregates findings
# - vibe-check meta-review
# - Creates .titanium/review-report.md
# - Voice: "Review complete: 1 security issue found"

# 5. User fixes issue
User: "Fix the security issue in auth.ts"

# Claude:
# - Reads review report
# - Identifies issue
# - Makes fix
# - Re-runs tests

# 6. User commits
/git commit

# Session ends, voice summary:
# "I implemented the authentication feature with JWT,
# including login, register, and password reset.
# Fixed one security issue. All tests passing."
```

---

### Workflow 2: Quick Feature Addition

**Scenario**: User wants to add a small feature quickly

**Steps**:

```bash
# 1. User describes feature inline
claude
/titanium:plan

User: "Add a search bar to the header that filters products by name"

# Claude:
# - Writes requirements to .titanium/requirements.md
# - Generates plan with plan_parser.py
# - Simple plan: 1 epic, 2 stories, 5 tasks
# - vibe-check validates
# - Presents to user

# 2. Execute immediately
/titanium:work

# Claude:
# - Quick implementation (15-20 min)
# - @frontend-developer creates search component
# - @test-runner adds tests
# - Voice announcements throughout
# - Completes workflow

# 3. Check status
/titanium:status

# Shows:
# - 100% complete
# - 5/5 tasks done
# - Ready for review
```

---

### Workflow 3: Bug Fix Workflow

**Scenario**: User encounters bug and wants systematic fix

**Steps**:

```bash
# 1. User describes bug
/titanium:plan

User: "Fix: Login fails with 500 error when email contains uppercase letters"

# Claude:
# - Creates plan:
#   Epic: Bug Fix - Login Email Case
#   Stories:
#   - Reproduce bug
#   - Identify root cause
#   - Implement fix
#   - Add tests
# - vibe-check validates approach

# 2. Execute fix
/titanium:work

# Claude:
# - @debugger reproduces issue
# - @debugger identifies: email comparison case-sensitive
# - @api-developer fixes: converts email to lowercase
# - @tdd-specialist adds test case
# - Voice: "Bug fixed, test added"

# 3. Verify fix
/titanium:review

# Claude:
# - Reviews fix
# - Confirms no regression
# - Voice: "Fix verified, no issues found"
```

---

### Workflow 4: Refactoring Project

**Scenario**: User wants to refactor codebase

**Steps**:

```bash
# 1. User describes refactoring goal
/titanium:plan

User: "Refactor authentication code to use new repository pattern"

# Claude:
# - Creates plan:
#   Epic 1: Create repository abstractions
#   Epic 2: Migrate existing code
#   Epic 3: Update tests
# - Estimates 3 hours
# - vibe-check: "Good approach, ensure backward compatibility"

# 2. Execute refactoring
/titanium:work

# Claude:
# - @refactor creates repository interfaces
# - @refactor migrates auth service
# - @test-runner updates tests
# - Voice announcements throughout
# - vibe-check after each epic
# - Ensures backward compatibility

# 3. Review quality
/titanium:review

# Claude:
# - @code-reviewer checks refactoring
# - @test-runner verifies coverage maintained
# - Voice: "Refactoring complete, all tests passing"
```

---

### Workflow 5: Resume After Interruption

**Scenario**: User's session was interrupted, needs to resume

**Steps**:

```bash
# 1. New session, user wants context
claude
/catchup

# Claude queries Pieces:
# "You were implementing user authentication.
# Completed: JWT middleware, login endpoint.
# In progress: Register endpoint (80% done).
# Next: Password reset flow.
# Open file: src/api/auth/register.ts"

# 2. Check detailed status
/titanium:status

# Shows:
# - Phase: Implementation
# - Progress: 60% (6/10 tasks)
# - Current task: "Create register endpoint"
# - Next: "Add password reset"

# 3. Continue workflow
/titanium:work

# Claude:
# - Reads workflow state
# - Continues from current task
# - Completes remaining work
```

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: "OPENAI_API_KEY not found"

**Symptoms**:
- `/titanium:plan` fails with API key error
- plan_parser.py exits with error

**Solution**:
```bash
# Add API key to ~/.env
echo 'OPENAI_API_KEY=sk-your-key-here' >> ~/.env
chmod 600 ~/.env

# Or set temporarily
export OPENAI_API_KEY=sk-your-key-here
```

**Prevention**: Document API key requirement in README

---

#### Issue 2: "vibe-check not responding"

**Symptoms**:
- vibe-check MCP calls timeout
- Workflow pauses indefinitely

**Solution**:
```bash
# Check vibe-check config
cat ~/.vibe-check/.env

# Ensure at least one API key is set
echo 'GEMINI_API_KEY=your-key' >> ~/.vibe-check/.env
# OR
echo 'OPENAI_API_KEY=your-key' >> ~/.vibe-check/.env

# Restart Claude Code
```

**Prevention**: Add vibe-check validation to `/titanium:plan`

---

#### Issue 3: "Pieces not found"

**Symptoms**:
- `/catchup` fails
- Pieces MCP calls fail

**Solution**:
```bash
# Ensure Pieces OS is running
open -a "Pieces OS"

# Verify Pieces CLI installed
pieces --version

# If not installed:
pip3 install --upgrade pieces-cli

# Configure MCP
pieces mcp setup claude_code --stdio

# Verify connection
claude mcp list
# Should show: Pieces: ✓ Connected
```

**Prevention**: Add Pieces check to workflow commands

---

#### Issue 4: "Plan generation produces invalid JSON"

**Symptoms**:
- plan_parser.py crashes
- `.titanium/plan.json` is malformed

**Solution**:
```bash
# Check plan_parser.py output
uv run hooks/utils/workflow/plan_parser.py requirements.md "$(pwd)" 2>&1

# If GPT-4 response is invalid:
# - Check requirements.md for clarity
# - Simplify requirements
# - Re-run plan_parser.py

# Manual fix:
# Edit .titanium/plan.json to fix JSON syntax
```

**Prevention**: Add JSON validation to plan_parser.py

---

#### Issue 5: "Agents not launching"

**Symptoms**:
- `/titanium:work` stalls
- No agent activity

**Solution**:
```bash
# Check if Task tool is working
# In Claude session, test:
@api-developer "Hello, can you respond?"

# If agent doesn't respond:
# - Check plugin installation
# - Verify agents/ directory exists
# - Restart Claude Code

# Check agent files
ls plugins/titanium-toolkit/agents/
# Should show 16 agent .md files
```

**Prevention**: Add agent availability check to `/titanium:work`

---

#### Issue 6: "Voice announcements not working"

**Symptoms**:
- No voice feedback
- Silent workflow execution

**Solution**:
```bash
# Test ElevenLabs directly
uv run plugins/titanium-toolkit/hooks/utils/tts/elevenlabs_tts.py "Test message"

# If fails, check API key
echo $ELEVENLABS_API_KEY

# Test fallback (macOS)
say "Test message"

# If say works but ElevenLabs doesn't:
# - Check ELEVENLABS_API_KEY in ~/.env
# - Check account credits at elevenlabs.io

# Disable voice (if needed)
# Remove PostToolUse hook from hooks.json temporarily
```

**Prevention**: Add TTS test to installation docs

---

#### Issue 7: "Workflow state corrupted"

**Symptoms**:
- `/titanium:status` shows wrong information
- State file exists but is invalid

**Solution**:
```bash
# Check state file
cat .titanium/workflow-state.json

# If corrupted, reset:
rm .titanium/workflow-state.json

# Re-initialize
uv run hooks/utils/workflow/workflow_state.py init "$(pwd)" "development" "Resume work"

# Restore from Pieces
/catchup
# Use Pieces context to understand where you were
```

**Prevention**: Add state validation to workflow_state.py

---

#### Issue 8: "Review report empty"

**Symptoms**:
- `/titanium:review` completes but report is empty
- No findings reported

**Solution**:
```bash
# Check if review agents ran
cat .titanium/review-report.md

# If truly empty:
# - No issues found (good!)
# - Or agents didn't run properly

# Test agents manually
@code-reviewer "Review src/api/auth.ts"

# If agent works, re-run review
/titanium:review
```

**Prevention**: Add validation that review agents completed

---

### Debug Mode

**Enable Verbose Logging**:

Add to slash command instructions:
```markdown
Debug mode: Set TITANIUM_DEBUG=1 before workflow

This will:
- Log all utility script calls
- Log all vibe-check responses
- Log all Pieces operations
- Save detailed logs to logs/titanium-debug.log
```

**Implementation**:
```python
# In utility scripts
import os

DEBUG = os.getenv("TITANIUM_DEBUG") == "1"

if DEBUG:
    log_file = Path.home() / "logs" / "titanium-debug.log"
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
```

---

## Future Enhancements

### Phase 6: Advanced Features (Future)

#### 1. Git Worktree Isolation

**Goal**: Isolate workflow in separate git worktree

**Implementation**:
- Add `--worktree` flag to `/titanium:work`
- Create worktree: `git worktree add .titanium-work feature/branch-name`
- Execute workflow in worktree
- Merge back when complete

**Benefits**:
- Don't affect main working directory
- Easy rollback if workflow fails
- Safe experimentation

---

#### 2. Workflow Templates

**Goal**: Pre-defined workflows for common tasks

**Templates**:
- `fullstack-feature.yaml` - Complete feature with backend + frontend
- `bug-fix.yaml` - Systematic bug fixing workflow
- `refactor.yaml` - Code refactoring workflow
- `api-endpoint.yaml` - New API endpoint
- `ui-component.yaml` - New UI component

**Usage**:
```bash
/titanium:work --template fullstack-feature
```

---

#### 3. Custom Agent Definitions

**Goal**: Allow users to define project-specific agents

**Implementation**:
- Check `.titanium/agents/` directory
- Load custom agent definitions
- Merge with built-in agents
- Use in plan_parser.py

**Example** (`.titanium/agents/mobile-developer.md`):
```markdown
---
name: mobile-developer
description: React Native mobile development specialist
tools: Read, Write, Edit, Bash, Grep
---

You are an expert React Native mobile developer...
```

---

#### 4. Workflow Metrics

**Goal**: Track workflow performance and efficiency

**Metrics**:
- Actual time vs estimated time
- Agent success rates
- vibe-check concern frequency
- Review issue frequency by category

**Storage**: `.titanium/metrics.json`

**Visualization**:
```bash
/titanium:metrics

# Shows:
# - Average workflow time
# - Most used agents
# - Common bottlenecks
# - Quality trends
```

---

#### 5. CI/CD Integration

**Goal**: Run workflows in CI/CD pipelines

**Implementation**:
- Add `--ci` flag for non-interactive mode
- Skip user approval steps
- Use environment variables for configuration
- Output machine-readable results

**Example** (`.github/workflows/review.yml`):
```yaml
name: Code Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Titanium Review
        run: |
          claude --non-interactive /titanium:review --ci
      - name: Post Results
        uses: actions/github-script@v6
        with:
          script: |
            const review = require('./.titanium/review-report.json')
            // Post review findings as PR comments
```

---

#### 6. Multi-Project Workflows

**Goal**: Coordinate workflows across multiple related projects

**Use Cases**:
- Microservices architecture
- Frontend + Backend repositories
- Shared libraries

**Implementation**:
- `.titanium/projects.json` lists related projects
- Workflows can trigger workflows in other projects
- Cross-project Pieces queries

---

#### 7. Workflow Playback

**Goal**: Replay workflow steps for learning/debugging

**Implementation**:
- Log all tool calls during workflow
- Store in `.titanium/workflow-log.jsonl`
- Add `/titanium:replay` command
- Show step-by-step execution

**Benefits**:
- Understand what happened
- Debug workflow issues
- Learn from successful workflows

---

#### 8. Smart Planning with Project History

**Goal**: Use past workflows to improve planning

**Implementation**:
- Analyze past workflows from Pieces
- Learn actual time vs estimates
- Identify common patterns
- Suggest optimizations

**Example**:
```
plan_parser.py detects:
"User often implements auth. Last 3 auth workflows took 5h, 4.5h, 4.2h.
Adjusting estimate from 3h to 4.5h based on history."
```

---

## Appendix

### A. File Structure Reference

```
plugins/titanium-toolkit/
├── .claude-plugin/
│   └── plugin.json                                   # Plugin metadata, version 2.0.0
├── .mcp.json                                          # MCP server configs
├── agents/                                            # 16 builder agents
│   ├── api-developer.md
│   ├── api-documenter.md
│   ├── code-reviewer.md
│   ├── debugger.md
│   ├── devops-engineer.md
│   ├── doc-writer.md
│   ├── frontend-developer.md
│   ├── marketing-writer.md
│   ├── meta-agent.md
│   ├── product-manager.md
│   ├── project-planner.md
│   ├── refactor.md
│   ├── security-scanner.md
│   ├── shadcn-ui-builder.md
│   ├── tdd-specialist.md
│   └── test-runner.md
├── commands/
│   ├── catchup.md                                     # Context recovery (existing)
│   ├── titanium-plan.md                               # NEW: Task planning
│   ├── titanium-work.md                               # NEW: Workflow execution
│   ├── titanium-review.md                             # NEW: Quality review
│   └── titanium-status.md                             # NEW: Progress status
├── hooks/
│   ├── hooks.json                                     # Hook configuration
│   ├── post_tool_use_elevenlabs.py                    # Tool completion announcements
│   ├── stop.py                                        # Session summaries
│   ├── notification.py                                # User alerts
│   ├── subagent_stop.py                               # Agent completion
│   ├── workflow_phase.py                              # NEW: Phase announcements
│   └── utils/
│       ├── workflow/                                  # NEW: Workflow utilities
│       │   ├── workflow_state.py                      # State management
│       │   └── plan_parser.py                         # Plan generation
│       ├── tts/                                       # Text-to-speech utilities
│       │   ├── elevenlabs_tts.py
│       │   ├── openai_tts.py
│       │   ├── local_tts.py
│       │   └── elevenlabs_mcp.py
│       └── llm/                                       # LLM utilities
│           ├── oai.py
│           └── anth.py
├── docs/
│   ├── ORCHESTRATION.md                               # This document
│   ├── ORCHESTRATION_PLAN.md                          # Implementation plan
│   ├── WORKFLOW_EXAMPLES.md                           # Usage examples
│   ├── TROUBLESHOOTING.md                             # Common issues
│   └── examples/
│       ├── fullstack-feature.md
│       ├── bug-fix-workflow.md
│       ├── refactor-workflow.md
│       └── api-development.md
├── LICENSE                                            # MIT License
└── README.md                                          # Main documentation

User's Project Directory (after running workflows):
.titanium/
├── workflow-state.json                                # Current workflow state
├── plan.json                                          # Structured plan data
├── plan.md                                            # Readable plan
├── requirements.md                                    # Input requirements
└── review-report.md                                   # Quality review findings

logs/                                                   # User's home directory
├── voice_announcements.json                           # Voice activity log
├── quality_gates.json                                 # Quality gate results
├── workflow_phases.json                               # Phase transitions
└── titanium-debug.log                                 # Debug logs (if enabled)
```

---

### B. JSON Schemas

#### workflow-state.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["workflow_type", "goal", "status", "started_at", "current_phase"],
  "properties": {
    "workflow_type": {
      "type": "string",
      "enum": ["development", "bug-fix", "refactor", "review"]
    },
    "goal": {
      "type": "string",
      "description": "User's stated goal for this workflow"
    },
    "status": {
      "type": "string",
      "enum": ["planning", "in_progress", "completed", "failed"]
    },
    "started_at": {
      "type": "string",
      "format": "date-time"
    },
    "completed_at": {
      "type": "string",
      "format": "date-time"
    },
    "current_phase": {
      "type": "string",
      "enum": ["planning", "implementation", "review", "completed"]
    },
    "phases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "status", "started_at"],
        "properties": {
          "name": {
            "type": "string"
          },
          "status": {
            "type": "string",
            "enum": ["in_progress", "completed", "failed"]
          },
          "started_at": {
            "type": "string",
            "format": "date-time"
          },
          "completed_at": {
            "type": "string",
            "format": "date-time"
          }
        }
      }
    },
    "completed_tasks": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "pending_tasks": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

#### plan.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["epics", "agents_needed", "estimated_total_time"],
  "properties": {
    "epics": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "description", "stories"],
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "stories": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "description", "tasks"],
              "properties": {
                "name": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                },
                "tasks": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": ["name", "agent", "estimated_time"],
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "agent": {
                        "type": "string",
                        "pattern": "^@[a-z-]+$"
                      },
                      "estimated_time": {
                        "type": "string",
                        "pattern": "^[0-9]+(m|h)$"
                      },
                      "dependencies": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "agents_needed": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^@[a-z-]+$"
      }
    },
    "estimated_total_time": {
      "type": "string",
      "pattern": "^[0-9]+(m|h)$"
    }
  }
}
```

---

### C. Environment Variables Reference

**Required**:
- `OPENAI_API_KEY` - OpenAI API key for GPT-4 (plan parsing) and GPT-5 (voice summaries)
- `ELEVENLABS_API_KEY` - ElevenLabs API key for voice synthesis

**Optional**:
- `TITANIUM_DEBUG` - Set to `1` to enable verbose logging
- `ENGINEER_NAME` - Your name for personalized voice announcements

**vibe-check** (in `~/.vibe-check/.env`):
- `GEMINI_API_KEY` - Google Gemini API key
- `OPENAI_API_KEY` - OpenAI API key (alternative)
- `OPENROUTER_API_KEY` - OpenRouter API key (alternative)
- `DEFAULT_LLM_PROVIDER` - Default provider: `gemini`, `openai`, or `openrouter`

**Pieces** (no additional env vars needed):
- Requires Pieces OS running
- Requires Pieces CLI installed
- Configured via: `pieces mcp setup claude_code --stdio`

---

### D. API Rate Limits & Costs

**OpenAI GPT-4o**:
- Used by: `plan_parser.py`, `post_tool_use_elevenlabs.py`
- Rate limit: 10,000 requests/day (tier 1)
- Cost: $2.50 per 1M input tokens, $10 per 1M output tokens
- Typical plan parse: ~500 input tokens, ~1000 output tokens = $0.01
- Typical voice summary: ~100 input tokens, ~20 output tokens = $0.0003

**ElevenLabs**:
- Used by: Voice hooks, `elevenlabs_tts.py`
- Rate limit: Varies by subscription tier
- Cost: $0.30 per 1000 characters (standard voice)
- Typical announcement: ~30 characters = $0.009
- Fallback: macOS `say` (free, no API key needed)

**Google Gemini** (via vibe-check):
- Used by: vibe-check quality gates
- Rate limit: 60 requests/minute (free tier)
- Cost: Free tier available, or $0.05 per 1M tokens
- Typical vibe-check: ~200 tokens = $0.00001

**Pieces**:
- Used by: Context storage and retrieval
- Rate limit: None (local)
- Cost: Free for personal use

**Total Cost Estimate** (per workflow):
- Plan generation: $0.01
- Voice announcements (10x): $0.09
- vibe-check gates (5x): $0.0001
- **Total per workflow: ~$0.10**

---

### E. Support & Contributing

**Issues**:
- GitHub Issues: https://github.com/webdevtodayjason/titanium-plugins/issues

**Discussions**:
- GitHub Discussions: https://github.com/webdevtodayjason/titanium-plugins/discussions

**Contributing**:
1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Test thoroughly
5. Submit pull request

**Testing Your Changes**:
```bash
# 1. Create local test marketplace
mkdir -p ~/test-titanium-marketplace
cd ~/test-titanium-marketplace

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/titanium-plugins.git
cd titanium-plugins
git checkout feature/my-feature

# 3. Create marketplace manifest
cd ..
mkdir .claude-plugin
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "test-titanium",
  "owner": {"name": "Test User"},
  "plugins": [{
    "name": "titanium-toolkit",
    "source": "./titanium-plugins/plugins/titanium-toolkit",
    "description": "Test version"
  }]
}
EOF

# 4. Install in Claude Code
claude
/plugin marketplace add ~/test-titanium-marketplace
/plugin install titanium-toolkit@test-titanium

# 5. Test your changes
/titanium:plan
/titanium:work
/titanium:review
/titanium:status

# 6. Uninstall after testing
/plugin uninstall titanium-toolkit@test-titanium
```

**Code Style**:
- Python: Follow PEP 8
- Markdown: Use frontmatter for command metadata
- Comments: Explain WHY, not WHAT
- UV scripts: Include inline dependencies

**Commit Messages**:
```
type: Brief description (50 chars max)

Detailed explanation of what and why.
- Bullet points for multiple changes
- Reference issues: Fixes #123

type: feat, fix, docs, refactor, test, chore
```

---

### F. Credits & Inspiration

**Built Upon**:
- [Claude Code](https://claude.ai/code) by Anthropic
- [Every's Compounding Engineering](https://github.com/EveryInc/every-marketplace)
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- [Pieces for Developers](https://pieces.app)

**Voice System**:
- [ElevenLabs](https://elevenlabs.io) - High-quality TTS
- [OpenAI GPT-5](https://openai.com) - Intelligent summaries

**Quality Gates**:
- [vibe-check](https://github.com/PV-Bhat/vibe-check-mcp-server) - Meta-mentor AI

**Created by**:
- Jason Brashear
- Titanium Computing
- https://titaniumcomputing.com

---

### G. License

MIT License

Copyright (c) 2025 Jason Brashear, Titanium Computing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR DEALINGS IN THE
SOFTWARE.

---

**End of Document**

Version: 1.0
Last Updated: October 2025
Status: Planning Phase
Next Review: After Week 1 Implementation
