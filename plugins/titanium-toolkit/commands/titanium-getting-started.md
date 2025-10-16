---
description: Learn how to use Titanium Toolkit for complete project workflows
---

# Titanium Toolkit - Getting Started Guide

Welcome to Titanium Toolkit! This guide explains the complete workflow from idea to implementation, including where documentation lives and what commands to use.

---

## Complete Project Workflow

### The Big Picture

```
Idea
  ↓
Project Documentation (backlog/)
  ↓
Implementation Plan (.titanium/)
  ↓
Code Implementation
  ↓
Quality Review
  ↓
Done!
```

**Each phase has specific commands and folder structures.**

---

## Phase 1: Project Documentation (Coming Soon!)

### Where Documentation Lives

**Folder**: `backlog/` or `bmad-backlog/` in your project root

```
your-project/
├── backlog/
│   ├── product-brief.md       # High-level vision
│   ├── prd.md                 # Product Requirements Document
│   ├── architecture.md        # Technical architecture
│   └── epics/
│       ├── epic-001.md        # Foundation Infrastructure
│       ├── epic-002.md        # User Management
│       └── ...
└── (source code will go here)
```

### Future Commands (In Development)

These BMAD document generation commands are coming:

**`/bmad:brief`** - Generate project brief
```bash
/bmad:brief "AI-powered precious metals research platform"
# → Creates backlog/product-brief.md
```

**`/bmad:prd`** - Generate Product Requirements Document
```bash
/bmad:prd
# → Reads product-brief.md
# → Creates backlog/prd.md with complete requirements
```

**`/bmad:epic`** - Generate epic breakdown
```bash
/bmad:epic "Foundation Infrastructure"
# → Creates backlog/epics/epic-001.md
# → Breaks down into user stories
```

**`/bmad:architecture`** - Generate technical architecture
```bash
/bmad:architecture
# → Reads PRD
# → Creates backlog/architecture.md
```

**Vision**: `/bmad:brief` → `/bmad:prd` → `/bmad:epic` → `/bmad:architecture` → Complete backlog!

**Status**: These commands are planned for future release. For now, you can:
- Create backlog/ folder manually
- Write documentation yourself
- Or use external BMAD-METHOD tool: `npx bmad-method`

---

## Phase 2: Implementation Planning

### Current State: Planning Commands Available Now

Once you have requirements (from backlog/ or your head), create an implementation plan:

**`/titanium:plan`** - Create implementation plan

```bash
# From backlog documentation
/titanium:plan backlog/epics/epic-001.md

# From inline description
/titanium:plan "Implement user authentication with JWT"

# From BMAD PRD (if using external BMAD tool)
/titanium:plan ~/bmad/output/project-prd.md
```

**What it creates**:
```
.titanium/
├── requirements.md        # Your input requirements
├── plan.json              # Structured plan (for Claude)
└── plan.md                # Human-readable plan (for you)
```

**What the plan includes**:
- Epics (major features)
- Stories (user functionality)
- Tasks (implementation steps)
- Agent assignments (@api-developer, @frontend-developer, etc.)
- Time estimates
- Dependencies between tasks

**Output example**:
```
📋 Implementation Plan Created

🎯 Goal: Implement Foundation Infrastructure

📦 Structure:
- 1 epic
- 4 stories
- 12 tasks

⏱️  Estimated Time: 3 hours

🤖 Agents:
- @devops-engineer (infrastructure)
- @api-developer (backend setup)
- @doc-writer (documentation)

Ready to execute? Run: /titanium:work
```

---

## Phase 3: Implementation

### Execute Your Plan

**`/titanium:work`** - Orchestrate complete implementation

```bash
# If you already ran /titanium:plan
/titanium:work

# Or create plan + execute in one step
/titanium:work "Implement user authentication"
```

**What happens**:

**Step 1: Planning** (if no plan exists)
- Asks what to implement
- Generates plan with GPT-4
- Shows you the plan
- **Waits for your approval**

**Step 2: Implementation**
- Creates todo list from plan
- Launches agents sequentially:
  - @product-manager validates requirements
  - @api-developer builds backend
  - @frontend-developer builds UI
  - @test-runner ensures quality
- Voice announces each step
- vibe-check validates after each task
- Stores progress in Pieces

**Step 3: Review**
- Launches 3 review agents in parallel:
  - @code-reviewer (code quality)
  - @security-scanner (security)
  - @tdd-specialist (test coverage)
- Creates review report
- Shows findings with file:line references

**Step 4: Completion**
- Presents summary
- Stores everything in Pieces
- You're done!

**Voice announcements throughout**:
- "Starting implementation phase"
- "API endpoints created, 8 tests passing"
- "Review complete: 1 security issue found"
- "Workflow complete!"

---

## Phase 4: Quality & Status

### Check Progress Anytime

**`/titanium:status`** - See where you are

```bash
/titanium:status
```

**Shows**:
- Current phase (planning/implementation/review/completed)
- Progress: 67% (8/12 tasks)
- Current task
- Time remaining
- Recent work from Pieces
- Next steps

**Use this**:
- Mid-workflow to check progress
- After lunch to remember where you were
- Next day to resume work
- Before meetings to report status

### Review Code Quality

**`/titanium:review`** - Run quality review

```bash
# Review recent changes
/titanium:review

# Review specific files
/titanium:review src/api/*.ts

# Review everything
/titanium:review --all
```

**What it does**:
- 3 agents review in parallel (fast!)
- Finds issues: Critical, Important, Nice-to-have
- Creates `.titanium/review-report.md`
- Shows actionable recommendations

**Use this**:
- After implementation
- Before committing
- Before pull requests
- Periodic code reviews

---

## Common Workflows

### Workflow 1: Brand New Project (No Documentation Yet)

**You have**: Just an idea
**Goal**: Build the project

**Steps**:

```bash
# 1. Create project directory
mkdir my-new-project
cd my-new-project
git init

# 2. (Future) Generate documentation with BMAD commands
# /bmad:brief "AI todo app with voice input"
# /bmad:prd
# /bmad:epic "Core Features"
# → Creates backlog/ with all documentation

# 3. (For now) Plan directly from idea
/titanium:plan "Build AI todo app with voice input and smart scheduling"

# 4. Execute
/titanium:work

# 5. Review
/titanium:review

# Done! Your project is implemented with tests.
```

**Timeline**: Can go from idea to working code in one session!

---

### Workflow 2: Existing Project with Backlog Documentation

**You have**: Project documentation in `backlog/` or similar
**Goal**: Implement next epic

**Steps**:

```bash
cd my-project

# 1. Plan from backlog
/titanium:plan backlog/epics/epic-003-user-profiles.md

# 2. Review the plan
# Claude shows: "3 stories, 8 tasks, 2 hours"

# 3. Approve and execute
/titanium:work

# 4. Review quality
/titanium:review

# Done!
```

**Timeline**: Each epic typically takes 2-6 hours depending on complexity.

---

### Workflow 3: Quick Feature Addition

**You have**: Working project
**Goal**: Add small feature quickly

**Steps**:

```bash
cd my-project

# One command - plan + execute
/titanium:work "Add search functionality to product catalog"

# Claude:
# - Creates quick plan (1 epic, 2 stories)
# - Shows you the plan
# - Asks approval
# - Implements
# - Reviews
# - Done!

# Timeline: 30 minutes to 1 hour
```

---

### Workflow 4: Bug Fix

**You have**: Bug to fix
**Goal**: Systematic fix with tests

**Steps**:

```bash
cd my-project

# Plan the fix
/titanium:plan "Fix: Login fails when email has uppercase letters"

# Execute
/titanium:work

# Claude:
# - @debugger reproduces bug
# - @api-developer fixes issue
# - @tdd-specialist adds test
# - Reviews fix
# - Done!

# Timeline: 15-30 minutes
```

---

### Workflow 5: Resume After Interruption

**You have**: Incomplete workflow
**Goal**: Continue where you left off

**Steps**:

```bash
# Next session, different day
cd my-project

# 1. Recover context
/catchup
# → Pieces: "You were implementing authentication. Backend complete..."

# 2. Check status
/titanium:status
# → Shows: "Phase: Implementation, 60% complete, Current: Register endpoint"

# 3. Continue work
/titanium:work
# → Resumes from current state
# → Completes remaining tasks
# → Done!
```

---

## Folder Structure Reference

### During Development

Your project will have these folders:

```
my-project/
├── backlog/                    # Project documentation (you create this)
│   ├── product-brief.md        # Vision and goals
│   ├── prd.md                  # Product requirements
│   ├── architecture.md         # Technical architecture
│   └── epics/
│       ├── epic-001.md         # Epic breakdowns
│       ├── epic-002.md
│       └── ...
│
├── .titanium/                  # Workflow state (created automatically)
│   ├── workflow-state.json     # Current workflow state
│   ├── plan.json               # Implementation plan
│   ├── plan.md                 # Readable plan
│   ├── requirements.md         # Input requirements
│   └── review-report.md        # Quality findings
│
├── src/                        # Your source code (created during /titanium:work)
│   ├── api/
│   ├── components/
│   └── ...
│
├── tests/                      # Your tests (created during /titanium:work)
│   └── ...
│
└── docs/                       # Technical docs (created during /titanium:work)
    └── ...
```

### Folder Purposes

**`backlog/`** (you create):
- High-level project documentation
- Product requirements
- Epic breakdowns
- Architecture decisions
- **Lives forever** - your project's source of truth

**`.titanium/`** (created automatically):
- Workflow execution data
- Implementation plans
- Review reports
- **Created per workflow** - can be regenerated

**`src/`**, **`tests/`**, **`docs/`** (created during implementation):
- Your actual code
- **Created by agents** during `/titanium:work`

---

## The 5 Commands

### 1. `/titanium:getting-started` (This Guide)
**Use when**: Learning the system
**Shows**: Complete workflow guide

### 2. `/titanium:plan`
**Use when**: Starting new work
**Creates**: Implementation plan from requirements
**Input**: File path or inline description

### 3. `/titanium:work`
**Use when**: Ready to implement
**Does**: Complete orchestration from plan to tested code
**Can include**: Inline planning if no plan exists

### 4. `/titanium:review`
**Use when**: Code review needed
**Does**: 3-agent parallel quality review
**Output**: Review report with findings

### 5. `/titanium:status`
**Use when**: Checking progress
**Shows**: Current state, progress %, next steps
**Works**: Across sessions

### 6. `/catchup` (Pieces Integration)
**Use when**: Resuming work in new session
**Shows**: Context from previous sessions
**Requires**: Pieces OS + CLI

---

## Starting a Brand New Project

### Option A: With BMAD Documentation (Future)

When BMAD commands are available:

```bash
# 1. Create project
mkdir my-new-app
cd my-new-app
git init

# 2. Generate documentation
/bmad:brief "Social media app for developers"
# → Creates backlog/product-brief.md

/bmad:prd
# → Creates backlog/prd.md

/bmad:epic "User Profiles"
/bmad:epic "Feed System"
/bmad:epic "Real-time Chat"
# → Creates backlog/epics/*.md

/bmad:architecture
# → Creates backlog/architecture.md

# 3. Implement first epic
/titanium:plan backlog/epics/epic-001.md
/titanium:work

# 4. Continue with more epics
/titanium:plan backlog/epics/epic-002.md
/titanium:work

# etc...
```

### Option B: Without BMAD (Available Now)

If you don't have documentation yet:

```bash
# 1. Create project
mkdir my-new-app
cd my-new-app
git init

# 2. Create backlog folder manually
mkdir backlog

# 3. Write your PRD (can be simple)
cat > backlog/prd.md << 'EOF'
# My Todo App

## Vision
AI-powered todo app with voice input and smart scheduling.

## Core Features
- Voice input for tasks
- AI categorization
- Smart scheduling suggestions
- Calendar integration

## Tech Stack
- React + TypeScript frontend
- Node.js + Express backend
- PostgreSQL database
EOF

# 4. Plan implementation
/titanium:plan backlog/prd.md

# 5. Execute
/titanium:work

# Done! You have a working app.
```

### Option C: Skip Documentation Entirely (Quick Projects)

For small projects or experiments:

```bash
# 1. Create project
mkdir quick-experiment
cd quick-experiment
git init

# 2. Just describe what you want
/titanium:work "Build a REST API for managing books with title, author, ISBN"

# Claude:
# - Creates plan inline
# - Implements
# - Tests
# - Done!

# Timeline: 30 minutes - 1 hour
```

---

## Starting with Existing Project

### If You Already Have Code

```bash
cd existing-project

# 1. Create backlog documentation (optional but recommended)
mkdir backlog
cat > backlog/next-features.md << 'EOF'
# Next Features

## User Authentication
- JWT-based auth
- Login/register
- Password reset
EOF

# 2. Plan from backlog
/titanium:plan backlog/next-features.md

# 3. Execute
/titanium:work

# Adds features to existing codebase
```

### If You Have Backlog Documentation Already

```bash
cd my-project
# You have: backlog/epics/epic-003.md

# 1. Plan next epic
/titanium:plan backlog/epics/epic-003.md

# 2. Execute
/titanium:work

# Continues building on existing code
```

---

## Daily Development Workflow

### Morning

```bash
# 1. Resume context
/catchup
# → Pieces: "Yesterday you implemented authentication backend..."

# 2. Check status
/titanium:status
# → "Phase: Implementation, 60% complete, Current: Login form"

# 3. Continue work
/titanium:work
# → Resumes from current state
```

### Midday

```bash
# Check progress
/titanium:status
# → "80% complete, 2 tasks remaining"
```

### End of Day

```bash
# Final check
/titanium:status
# → "100% complete, ready for review"

/titanium:review
# → Quality review runs
# → "1 security issue found in auth.ts:45"

# Fix the issue
# Claude fixes it

# Commit
git add .
git commit -m "feat: Add user authentication"

# Session ends
# Voice: "I implemented user authentication with JWT, fixed one security issue, all tests passing"
```

### Next Morning

```bash
# New session
/catchup
# → "Yesterday: Completed authentication. All tests passing. Ready for next epic."

/titanium:plan backlog/epics/epic-002.md
# → Plan next feature
```

---

## Command Decision Tree

**Starting a new project?**
```
Do you have documentation?
├─ Yes (backlog/*.md exists)
│  └─ /titanium:plan backlog/epics/epic-001.md
│     └─ /titanium:work
│
└─ No (just an idea)
   ├─ Simple project?
   │  └─ /titanium:work "description"
   │
   └─ Complex project?
      ├─ (Future) /bmad:prd → /bmad:epic → /titanium:plan
      └─ (Now) Write backlog/*.md manually → /titanium:plan
```

**Adding to existing project?**
```
Do you have a plan?
├─ Yes (.titanium/plan.json exists)
│  └─ /titanium:work
│
└─ No
   └─ /titanium:plan "feature description"
      └─ /titanium:work
```

**Need to review code?**
```
/titanium:review
```

**Lost track of progress?**
```
/catchup        # Get context from Pieces
/titanium:status # See current state
```

---

## Recommended Folder Structure

### For Serious Projects

```
my-project/
├── backlog/                           # Documentation (manual or /bmad:*)
│   ├── product-brief.md              # Vision
│   ├── prd.md                        # Requirements
│   ├── architecture.md               # Technical decisions
│   └── epics/
│       ├── epic-001-foundation.md
│       ├── epic-002-auth.md
│       └── epic-003-profiles.md
│
├── .titanium/                        # Workflow state (auto-created)
│   ├── workflow-state.json
│   ├── plan.json
│   └── review-report.md
│
├── src/                               # Source code
├── tests/                             # Tests
├── docs/                              # Technical docs
├── .env.example                       # Example env vars
├── README.md                          # Project readme
└── package.json                       # Dependencies
```

### For Quick Projects

```
quick-project/
├── .titanium/         # Auto-created by /titanium:plan or /titanium:work
├── src/               # Your code
└── tests/             # Your tests
```

No backlog/ needed for simple projects!

---

## Best Practices

### 1. Start with Planning

**Recommended**:
```bash
/titanium:plan "feature description"
/titanium:work
```

**Why**: See the plan before execution, understand scope, get time estimates.

### 2. Review Before Committing

**Recommended**:
```bash
/titanium:review
# Fix any critical issues
git commit
```

**Why**: Catch issues early, maintain quality.

### 3. Use Backlog for Documentation

**Create**:
```
backlog/
├── prd.md
└── epics/
    └── *.md
```

**Why**: Organized documentation, easy to plan from, version controlled.

### 4. Check Status Regularly

**During long workflows**:
```bash
/titanium:status
```

**Why**: Stay informed, know what's next, track time.

### 5. Use /catchup Between Sessions

**Every new session**:
```bash
/catchup
```

**Why**: Never lose context, resume instantly.

---

## What You Don't Need

❌ Don't need to create `.titanium/` folder manually
❌ Don't need to write plan.json yourself
❌ Don't need to install Python packages (UV handles it)
❌ Don't need to manage agents manually
❌ Don't need to coordinate workflows yourself

**Titanium does all of this for you!**

---

## Tips & Tricks

### Tip 1: Keep Backlog Documentation Simple

Your `backlog/prd.md` can be very simple:

```markdown
# Project: Todo App

## Goal
Personal todo app with AI assistance

## Features
- Add/edit/delete todos
- Voice input
- AI categorization
- Due date suggestions

## Tech Stack
- React frontend
- Node.js backend
- SQLite database
```

That's enough! `/titanium:plan` will break it down.

### Tip 2: Iterate on Plans

```bash
/titanium:plan "Add authentication"
# Review the plan
# Not quite right?

# Create new plan
/titanium:plan "Add JWT authentication with refresh tokens and email verification"
# Better!

/titanium:work
```

Plans are cheap (~$0.01). Iterate until right.

### Tip 3: Use Status During Long Workflows

```bash
/titanium:work "Complex feature"
# ... 2 hours pass ...
/titanium:status
# "67% complete, 2 hours remaining"
```

Know when to take breaks!

### Tip 4: Store Backlog in Git

```bash
git add backlog/
git commit -m "docs: Add product backlog"
```

Version your documentation. See how it evolves.

### Tip 5: Use Review Standalone

```bash
# Before committing
/titanium:review

# Fix issues
/titanium:review  # Run again to verify
```

Can use review without running full workflow.

---

## Understanding Cost

**Per workflow** (~4 hour implementation):
- Plan generation (GPT-4): $0.01
- vibe-check gates (5x): $0.0005
- Voice announcements (10x): $0.09
- **Total: ~$0.10**

Very affordable! Less than a cup of coffee per feature.

**Optional**:
- Skip voice (use macOS say): Save $0.09
- Skip vibe-check: Save $0.0005 (but lose quality gates)

**Minimum cost**: $0.01 per workflow (GPT-4 planning only)

---

## When Things Go Wrong

### "No plan found" when running /titanium:work

**Solution**: Run `/titanium:plan` first, or provide description inline:
```bash
/titanium:work "what to implement"
```

### "OPENAI_API_KEY not found"

**Solution**: Add to ~/.env:
```bash
echo 'OPENAI_API_KEY=sk-your-key' >> ~/.env
```
Restart Claude Code.

### "Workflow stuck at X%"

**Solution**: Check status:
```bash
/titanium:status
```

If truly stuck, restart workflow:
```bash
rm -rf .titanium/
/titanium:work "description"
```

### "Review found critical issues"

**Solution**: Fix them!
```bash
# Claude can fix them for you
User: "Fix the SQL injection in users.ts:45"

# Or do manually, then review again
/titanium:review
```

---

## Getting Help

### Documentation
- **This Guide**: `/titanium:getting-started` (you are here!)
- **Full Architecture**: `docs/ORCHESTRATION_PLAN.md`
- **Dependencies**: `docs/DEPENDENCIES.md`

### Verification
```bash
# Run verification script
curl -o verify.sh https://raw.githubusercontent.com/webdevtodayjason/titanium-plugins/main/verify-installation.sh
chmod +x verify.sh
./verify.sh
```

### Support
- **Issues**: https://github.com/webdevtodayjason/titanium-plugins/issues
- **Discussions**: https://github.com/webdevtodayjason/titanium-plugins/discussions

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│ Titanium Toolkit Quick Reference                │
├─────────────────────────────────────────────────┤
│                                                  │
│ Get Started:                                     │
│   /titanium:getting-started                     │
│                                                  │
│ Plan Work:                                       │
│   /titanium:plan "what to build"                │
│   /titanium:plan backlog/epics/epic-001.md     │
│                                                  │
│ Execute:                                         │
│   /titanium:work                                │
│   /titanium:work "quick feature"               │
│                                                  │
│ Check Progress:                                  │
│   /titanium:status                              │
│   /catchup                                      │
│                                                  │
│ Review Quality:                                  │
│   /titanium:review                              │
│                                                  │
│ Folders:                                         │
│   backlog/      - Your documentation           │
│   .titanium/    - Workflow state (auto)        │
│   src/          - Code (created by agents)     │
│                                                  │
│ Files Created:                                   │
│   .titanium/plan.json       - Plan             │
│   .titanium/workflow-state.json - State        │
│   .titanium/review-report.md - Findings        │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## What's Next?

### Ready to Start?

**Simple project**:
```bash
/titanium:work "your idea here"
```

**Complex project**:
```bash
# 1. Create backlog documentation
mkdir backlog
# Write backlog/prd.md

# 2. Plan
/titanium:plan backlog/prd.md

# 3. Execute
/titanium:work
```

### Want BMAD Documentation Generation?

BMAD slash commands (`/bmad:prd`, `/bmad:epic`, etc.) are **coming soon**!

Meanwhile, you can:
- Write backlog/ docs manually (simple markdown)
- Use external BMAD tool: `npx bmad-method`
- Or skip documentation for simple projects

---

**You're ready to orchestrate! Pick a workflow above and start building.** 🚀
