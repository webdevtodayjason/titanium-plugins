# Titanium Toolkit

> AI-powered workflow orchestration for Claude Code with voice feedback

**The complete development workflow system: from requirements to tested implementation, with AI quality gates and voice announcements throughout.**

---

## What is Titanium Toolkit?

Titanium Toolkit orchestrates complete development workflows using AI agents. It breaks down requirements, coordinates 16 specialized agents, validates quality at every step, and keeps you informed with voice announcements.

**Think of it as your AI development conductor** - you provide the requirements, it orchestrates the implementation.

```
Requirements → Plan → Implementation → Review → Done
     ↓           ↓           ↓            ↓        ↓
  GPT-4      vibe-check   Agents    3 Reviewers  Pieces
```

---

## Quick Start (4 Steps)

### 1. Install UV (Required)

UV manages Python dependencies automatically. Install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify: `uv --version` (should show version 0.4.0+)

**Why UV?** All Python scripts use UV's inline dependency format - no pip install needed!

### 2. Install Plugin

```bash
/plugin marketplace add webdevtodayjason/titanium-plugins
/plugin install titanium-toolkit
```

**Restart Claude Code**

### 3. Add API Key

Create `~/.env` with your OpenAI API key:

```bash
echo 'OPENAI_API_KEY=sk-your-key-here' >> ~/.env
chmod 600 ~/.env
```

Get your key from: https://platform.openai.com/api-keys

### 4. Verify Installation (Recommended)

Test that everything is set up correctly:

```bash
# Download and run verification script
curl -o verify.sh https://raw.githubusercontent.com/webdevtodayjason/titanium-plugins/main/verify-installation.sh
chmod +x verify.sh
./verify.sh
```

Should show: "🎉 All checks passed!"

### 5. Run Your First Workflow

**Two options:**

**Option A: Plan First (Recommended for complex projects)**
```bash
/titanium:plan "Add a contact form with name, email, and message fields"
# → Creates .titanium/ directory
# → Generates implementation plan
# → Shows epics, stories, tasks
# → Asks for approval

/titanium:work
# → Uses the plan you just created
# → Orchestrates agents to implement
# → Voice announces progress
# → Done!
```

**Option B: Plan & Execute Together (Quick features)**
```bash
/titanium:work "Add a contact form with name, email, and message fields"
# → Creates plan inline
# → Asks for approval
# → Executes immediately
# → Done!
```

That's it! You now have a working contact form with tests.

**Note**: The `.titanium/` folder is created automatically by these commands. You don't create it manually.

---

## The Core Commands

### `/titanium:getting-started` - Learn the Workflow

New to Titanium Toolkit? Start here!

```bash
/titanium:getting-started
```

**Shows**:
- Complete workflow guide
- How to start new projects
- Folder structure (backlog/ and .titanium/)
- Common workflows and examples
- Decision trees for what command to use
- Quick reference card

**Use when**: First time using Titanium, or as a reference guide.

---

### `/titanium:plan` - Create Implementation Plan

Analyzes requirements and creates a detailed plan with epics, stories, tasks, and agent assignments.

```bash
# From file (e.g., BMAD PRD)
/titanium:plan ~/bmad/output/user-auth-prd.md

# Or describe inline
/titanium:plan "Add JWT authentication"
```

**What it does**:
- Uses GPT-4 to break down requirements
- Assigns tasks to appropriate agents
- Estimates time
- Validates with vibe-check AI
- Stores plan in Pieces LTM
- Saves to `.titanium/plan.json`

**Output**: "Plan created with 3 epics, 8 stories, 12 tasks. Estimated: 4 hours"

---

### `/titanium:work` - Execute Workflow

Orchestrates the complete implementation workflow with quality gates.

```bash
/titanium:work
# Uses existing plan from /titanium:plan

# Or create plan inline
/titanium:work "Add user authentication"
```

**What it does**:
1. **Planning** - Creates plan if needed (or uses existing)
2. **Implementation** - Executes tasks sequentially with agents
3. **Quality Gates** - vibe-check validates after each task
4. **Review** - 3 agents review in parallel
5. **Completion** - Stores everything in Pieces

**Agents orchestrated**:
- @product-manager validates requirements
- @api-developer builds backend
- @frontend-developer builds UI
- @test-runner ensures quality
- @code-reviewer, @security-scanner, @tdd-specialist review

**Voice announcements**:
- "Starting implementation phase"
- "API endpoints created, 8 tests passing"
- "Frontend complete, building..."
- "Review complete: 1 security issue found"

---

### `/titanium:review` - Quality Review

Runs comprehensive code review with 3 specialized agents in parallel.

```bash
/titanium:review
# Reviews recent changes

/titanium:review src/api/*.ts
# Reviews specific files
```

**What it does**:
- @code-reviewer checks quality and best practices
- @security-scanner finds vulnerabilities
- @tdd-specialist analyzes test coverage
- All run simultaneously (fast!)
- Creates `.titanium/review-report.md`
- Categorizes: Critical, Important, Nice-to-have

**Output**: "Review complete: 1 critical, 3 important, 5 minor issues"

---

### `/titanium:status` - Check Progress

Shows current workflow state and progress.

```bash
/titanium:status
# Shows current progress

/titanium:status --voice
# Spoken summary (future)
```

**What it shows**:
- Current phase (planning/implementation/review/completed)
- Progress: 67% (8/12 tasks complete)
- Current task: "Create login form component"
- Estimated time remaining
- Recent work from Pieces
- Next steps

Works across sessions - resume anytime with `/catchup`.

---

## Complete Workflow Example

```bash
# Morning: Start new feature
/titanium:plan "Add user profile page with avatar upload"
# → Plan created: 2 epics, 5 stories, 10 tasks

/titanium:work
# → Implementation starts
# → Voice: "Starting implementation phase"
# → @api-developer creates profile API
# → Voice: "Profile API created, 6 tests passing"
# → @frontend-developer builds profile page
# → Voice: "Profile page complete"
# → vibe-check validates each step
# → Review agents run automatically
# → Voice: "Review complete: all checks passed"
# → Workflow complete!

# Afternoon: Resume after lunch
/titanium:status
# → "Phase: Completed. All 10 tasks done. 100% complete."

# Next day: New session
/catchup
# → Pieces: "Yesterday you implemented user profile page with avatar upload..."

/titanium:status
# → Shows completed workflow details
```

Cost: ~$0.10 per workflow (GPT-4 + voice + vibe-check)

---

## Requirements

### Essential (Must Have)

- **Claude Code** 2.0.14+
- **Python** 3.11+
- **uv** - Python package manager ([install guide](https://docs.astral.sh/uv/))
- **OpenAI API Key** - For GPT-4 planning ($0.01 per plan)

### Recommended (Better Experience)

- **ElevenLabs API Key** - For voice announcements ($0.09 per workflow)
  - Fallback: Uses macOS `say` if not available
- **Pieces OS + CLI** - For memory and context ([installation guide](./docs/PIECES_INSTALLATION.md))
- **vibe-check** - For AI quality gates (almost free with Gemini)
- **CodeRabbit CLI** - For deep static analysis (race conditions, memory leaks)
  - Install: `curl -fsSL https://cli.coderabbit.ai/install.sh | sh`
  - Catches issues agents might miss
  - Free and paid tiers available

### Optional (Enhanced Features)

- **Node.js** 20+ - For some MCP servers
- **Git** - For review scope detection

---

## API Keys Setup

### Required: OpenAI (GPT-4 for planning)

```bash
# Add to ~/.env
echo 'OPENAI_API_KEY=sk-your-key-here' >> ~/.env
chmod 600 ~/.env
```

Get key: https://platform.openai.com/api-keys

### Recommended: ElevenLabs (Voice)

```bash
# Add to ~/.env
echo 'ELEVENLABS_API_KEY=your-key-here' >> ~/.env
```

Get key: https://elevenlabs.io/app/settings/api-keys

Without this, voice uses macOS `say` (still works, just different voice).

### Recommended: vibe-check (Quality Gates)

```bash
# Create separate config
mkdir -p ~/.vibe-check
echo 'GEMINI_API_KEY=your-key-here' >> ~/.vibe-check/.env
chmod 600 ~/.vibe-check/.env
```

Get key: https://ai.google.dev/gemini-api/docs/api-key

Without this, workflows still run but skip quality validation.

---

## The 16 Builder Agents

When `/titanium:work` runs, it uses these specialized agents:

**Development**:
- @api-developer - Backend APIs
- @frontend-developer - UI/UX
- @devops-engineer - Deployment

**Quality**:
- @code-reviewer - Code quality
- @debugger - Error analysis
- @test-runner - Test execution
- @tdd-specialist - Test writing
- @security-scanner - Security

**Documentation**:
- @doc-writer - Technical docs
- @api-documenter - API specs

**Planning**:
- @product-manager - Requirements
- @project-planner - Task breakdown
- @meta-agent - Create agents

**Specialized**:
- @refactor - Code improvement
- @marketing-writer - Marketing content
- @shadcn-ui-builder - UI components

You can also use agents directly: `@api-developer "Create a REST API for users"`

---

## Voice Announcements

Titanium Toolkit announces progress in real-time:

- "Starting implementation phase"
- "API endpoints created, 8 tests passing"
- "Frontend complete, building..."
- "Review complete: 1 security issue in auth.ts:45"
- "Workflow complete!"

Uses ElevenLabs "Sarah" voice (or macOS `say` as fallback).

---

## Workflow States & Files

During workflows, Titanium creates:

```
your-project/
└── .titanium/
    ├── workflow-state.json    # Current workflow state
    ├── plan.json              # Structured plan (epics, stories, tasks)
    ├── plan.md                # Human-readable plan
    ├── requirements.md        # Input requirements
    └── review-report.md       # Quality review findings
```

These files persist across sessions - resume work anytime!

---

## Advanced Features

### Pieces Integration

Titanium stores everything in Pieces LTM:
- Implementation plans
- Epic completions
- Review findings
- Session summaries

Resume context instantly:
```bash
/catchup
# → "You were implementing authentication. Backend complete, working on frontend forms..."
```

### vibe-check Quality Gates

AI oversight prevents mistakes:
- Validates plan before execution
- Checks progress after each task
- Catches issues early
- Suggests improvements

### CodeRabbit Deep Analysis

Static analysis that catches subtle issues:
- Race conditions in concurrent code
- Memory and resource leaks
- Security vulnerabilities
- Logic errors and edge cases
- Runs between implementation and review
- Optional but recommended

### MCP Servers

Titanium includes 8 MCP servers for enhanced capabilities:
- **Pieces** - Long-term memory
- **vibe-check** - Quality gates
- **ElevenLabs** - Voice tools
- **shadcn-ui** - UI components
- **playwright** - Browser testing
- **context7** - Library docs
- **pypi** - Python packages
- **youtube-transcript** - Video transcripts

Most work automatically through the `.mcp.json` configuration included with the plugin.

---

## BMAD Document Generation

**Built-in BMAD methodology** for creating project documentation - no external BMAD installation needed!

### Start a Brand New Project

```bash
# Empty folder → Complete backlog in 45 minutes
/bmad:start
```

**Interactive workflow creates**:
- Product Brief (vision and goals)
- PRD (comprehensive requirements)
- Architecture (technical design with code)
- Epic files (user stories with acceptance criteria)
- Story Index (summary for sprint planning)

**Output**: Complete `bmad-backlog/` folder ready for implementation.

### The BMAD Commands

**`/bmad:start`** - Complete guided workflow
- Creates all documents in one session
- Interactive questions guide you
- 30-45 minutes
- Cost: ~$0.22

**`/bmad:brief`** - Product brief only
**`/bmad:prd`** - PRD only
**`/bmad:architecture`** - Architecture only
**`/bmad:epic`** - Single epic (add new or regenerate)
**`/bmad:index`** - Story index summary
**`/bmad:research`** - Research prompt generator

### Complete Workflow

```
Empty folder → /bmad:start → /titanium:plan → /titanium:work → Production Code
   (0 min)        (45 min)       (2 min)          (15 hours)         (1 week)
```

**Cost**: $0.22 (BMAD) + $0.40 (implementation) = **~$0.62 for complete MVP**

---

## Troubleshooting

### "uv: command not found"

UV is required to run Python scripts. Install it:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your terminal or add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Verify
uv --version
```

Restart Claude Code after installing UV.

### "OPENAI_API_KEY not found"

```bash
# Check if key is set
cat ~/.env | grep OPENAI_API_KEY

# If missing, add it
echo 'OPENAI_API_KEY=sk-your-key-here' >> ~/.env
```

Restart Claude Code after adding.

### "Voice not working"

Voice is optional. Check:
```bash
# Try ElevenLabs key
cat ~/.env | grep ELEVENLABS_API_KEY

# Or use macOS say (works without key)
say "Test"
```

Voice announcements use macOS `say` as fallback automatically.

### "vibe-check not available"

vibe-check is optional but recommended:
```bash
# Check vibe-check config
cat ~/.vibe-check/.env

# Add at least one API key
mkdir -p ~/.vibe-check
echo 'GEMINI_API_KEY=your-key' >> ~/.vibe-check/.env
```

Workflows work without vibe-check, just skip quality validation.

### "Pieces not found"

Pieces is optional but recommended:
1. Install Pieces OS from https://pieces.app
2. Install CLI: `pip3 install pieces-cli`
3. Run: `pieces mcp setup claude_code --stdio`
4. Restart Claude Code

Workflows work without Pieces, just no memory storage.

For more help, see [Troubleshooting Guide](./docs/ORCHESTRATION_PLAN.md#troubleshooting-guide).

---

## Documentation

### Workflow & Architecture
- **[Getting Started Guide](./docs/ORCHESTRATION_PLAN.md#complete-user-journey)** - Your first workflow
- **[Complete System Architecture](./docs/ORCHESTRATION_PLAN.md)** - Full technical details
- **[Troubleshooting Guide](./docs/ORCHESTRATION_PLAN.md#troubleshooting-guide)** - Common issues

### BMAD System
- **[BMAD Generation Guide](./docs/BMAD_GENERATION_PLAN.md)** - Complete BMAD documentation system
- **[BMAD Research System](./docs/BMAD_RESEARCH_SYSTEM.md)** - Vendor/API evaluation workflow
- **[BMAD Quick Start](./docs/BMAD_QUICKSTART.md)** - External BMAD tool (optional, not needed)

### Setup & Installation
- **[Dependencies Guide](./docs/DEPENDENCIES.md)** - UV and Python requirements
- **[Pieces Installation Guide](./docs/PIECES_INSTALLATION.md)** - Pieces LTM setup
- **[Verification Script](./verify-installation.sh)** - Test your installation

---

## How It Works

### Traditional Development
```
You: "Add authentication"
Claude: [implements one thing at a time, you guide each step]
```

### With Titanium Toolkit
```
You: /titanium:work "Add authentication"

Claude orchestrates:
✅ @product-manager validates requirements
✅ @api-developer creates JWT middleware + 3 endpoints
✅ @frontend-developer builds login/register forms
✅ @test-runner writes 12 integration tests
✅ @security-scanner finds 1 SQL injection → fixed
✅ All tests passing → Done!

Voice announces each step. vibe-check validates quality.
Pieces remembers everything for next session.
```

**One command. Complete feature. Professional quality.**

---

## Contributing

We welcome contributions!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Test thoroughly
5. Submit pull request

See [CLAUDE.md](./CLAUDE.md) for development guidelines.

---

## Support

- **Issues**: https://github.com/webdevtodayjason/titanium-plugins/issues
- **Discussions**: https://github.com/webdevtodayjason/titanium-plugins/discussions

---

## Credits

Created by **Jason Brashear** - [Titanium Computing](https://titaniumcomputing.com)

**Inspired by**:
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) - Requirements framework
- [Every's Compounding Engineering](https://github.com/EveryInc/every-marketplace) - Workflow patterns

**Powered by**:
- [Claude Code](https://claude.ai/code) by Anthropic
- [ElevenLabs](https://elevenlabs.io) - Voice synthesis
- [OpenAI GPT-4](https://openai.com) - Plan generation
- [Pieces](https://pieces.app) - Long-term memory
- [vibe-check](https://github.com/PV-Bhat/vibe-check-mcp-server) - AI quality gates

---

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

## What's New in v2.1.0

**Complete Workflow Orchestration** ✅:
- `/titanium:plan` - AI-powered planning
- `/titanium:work` - Full workflow execution
- `/titanium:review` - Parallel quality review
- `/titanium:status` - Progress tracking
- `/titanium:getting-started` - Complete workflow guide

**BMAD Document Generation** ✅:
- `/bmad:start` - Complete guided backlog generation
- `/bmad:brief` - Product brief
- `/bmad:prd` - Product Requirements Document
- `/bmad:architecture` - Technical architecture
- `/bmad:epic` - Epic files with user stories
- `/bmad:index` - Story index summary
- `/bmad:research` - Research prompt generator

**Complete idea-to-code workflow**: Empty folder → Working MVP in 1 week for ~$0.62

---

**Ready to orchestrate?** Install now and run `/bmad:start` to create your project!
