# BMAD Quick Start Guide

Complete guide for using BMAD-METHOD to create PRDs and integrate them with your Titanium Toolkit workflow.

## What is BMAD?

**BMAD (Breakthrough Method for Agile AI-Driven Development)** is a structured methodology for creating comprehensive project requirements, PRDs, and user stories using AI-assisted workflows.

**Use BMAD for:**
- Product Requirements Documents (PRDs)
- Epic breakdowns
- User story generation
- Technical specifications
- Project planning and analysis

## Prerequisites

- **Node.js** 20+
- **Claude Code** installed
- **Disk Space**: ~200MB for BMAD installation

## Step 1: Install BMAD

Install BMAD in your home directory for easy access across all projects:

```bash
# Navigate to home directory
cd ~

# Install BMAD using npx
npx bmad-method install --directory ~/bmad --ide claude-code
```

**Installation Options:**
- `--directory ~/bmad` - Installs BMAD in your home folder
- `--ide claude-code` - Configures for Claude Code integration

The installer will:
1. Download BMAD agents and workflows
2. Configure for Claude Code
3. Set up the BMAD directory structure

**Installation Time**: ~2-3 minutes

## Step 2: Understanding BMAD Structure

After installation, your `~/bmad` directory contains:

```
~/bmad/
├── agents/           # BMAD specialized agents
│   ├── pm/          # Product Manager agent
│   ├── sm/          # Scrum Master agent
│   ├── dev/         # Developer agent
│   └── qa/          # QA agent
├── workflows/        # BMAD workflow templates
├── output/          # Generated PRDs and docs
└── config/          # BMAD configuration
```

## Step 3: Create Your First PRD

### Start a New Project

```bash
# Navigate to BMAD directory
cd ~/bmad

# Start Claude Code in BMAD directory
claude
```

### Use BMAD Agents

BMAD provides specialized slash commands (if configured) or you can use the agents directly:

**Method 1: Using BMAD Commands (if available)**
```bash
# Start with Product Manager
/pm Create a PRD for a user authentication system with social login

# The PM agent will guide you through:
# - Project overview
# - User stories
# - Requirements
# - Success criteria
```

**Method 2: Direct Conversation**
```bash
I need to create a PRD for [your project idea]. Help me define:
- Project goals and objectives
- Target users
- Core features
- Technical requirements
- Success metrics
```

### BMAD Will Guide You Through:

1. **Analysis Phase** (Optional):
   - Brainstorming
   - Initial research
   - Problem definition

2. **Planning Phase** (Required):
   - Determines project complexity (Levels 0-4)
   - Generates appropriate documentation
   - Creates user stories and epics

3. **Output Generation**:
   - PRD document saved to `~/bmad/output/`
   - Epic breakdowns (for complex projects)
   - User stories with acceptance criteria

## Step 4: Using BMAD Output with Titanium Toolkit

Once BMAD generates your PRD, integrate it into your development workflow:

### Navigate to Your Project

```bash
# Go to your project directory
cd ~/code/your-project
```

### Execute PRD with /work Command

Use compounding-engineering's `/work` command to execute the BMAD-generated PRD:

```bash
# Execute the PRD
/compounding-engineering:work ~/bmad/output/your-project-prd.md
```

**What happens:**
1. `/work` analyzes the PRD
2. Creates comprehensive todo list
3. Sets up git worktree for isolated development
4. Titanium Toolkit's 16 builder agents implement features
5. Voice announcements keep you informed
6. Creates PR when complete

### The Complete Flow

```
BMAD (~/bmad)
  ↓
Generate PRD
  ↓
~/bmad/output/project-prd.md
  ↓
/compounding-engineering:work ~/bmad/output/project-prd.md
  ↓
Titanium Toolkit builders implement
  ↓
compounding-engineering reviewers validate
  ↓
PR created
```

## Step 5: BMAD Project Complexity Levels

BMAD adapts documentation to project complexity:

### Level 0: Simple Tasks
- **Output**: Basic tech spec
- **Example**: "Add a new API endpoint"
- **Time**: 15-30 minutes

### Level 1-2: Standard Features
- **Output**: Minimal PRD with user stories
- **Example**: "Build user authentication system"
- **Time**: 1-4 hours

### Level 3-4: Complex Projects
- **Output**: Comprehensive PRD with epic breakdowns
- **Example**: "Build multi-tenant SaaS platform"
- **Time**: 1-2 days of planning

BMAD automatically determines the appropriate level based on your project description.

## Example Workflow

Here's a complete example from requirements to implementation:

### 1. Create PRD with BMAD

```bash
cd ~/bmad
claude

# In Claude:
Create a PRD for a task management application with:
- User authentication
- Task creation and editing
- Team collaboration
- Real-time updates
- Mobile-responsive UI
```

BMAD will generate:
- `~/bmad/output/task-management-prd.md`
- User stories
- Epic breakdowns
- Technical requirements

### 2. Review the PRD

```bash
# Read the generated PRD
cat ~/bmad/output/task-management-prd.md
```

Review and edit as needed using your text editor.

### 3. Execute with Titanium Toolkit

```bash
# Navigate to your project
cd ~/code/task-manager

# Execute the PRD
/compounding-engineering:work ~/bmad/output/task-management-prd.md
```

**What happens:**
1. Creates feature branch
2. Sets up worktree
3. Breaks down PRD into tasks
4. @api-developer builds backend
5. @frontend-developer builds UI
6. @test-runner validates
7. Voice announces progress
8. Creates PR with all changes

### 4. Review & Iterate

```bash
# Run comprehensive review
/compounding-engineering:review

# Specialized reviewers check:
# - @security-sentinel for vulnerabilities
# - @performance-oracle for bottlenecks
# - @architecture-strategist for design
```

### 5. Learn & Repeat

```bash
# Pieces captures everything
# Next session, start with:
/catchup

# See what was accomplished
# Resume where you left off
```

## BMAD Best Practices

### Start Conversations Clearly

✅ **Good:**
```
Create a PRD for an e-commerce checkout flow that supports:
- Credit card payments via Stripe
- Guest checkout option
- Order confirmation emails
- Inventory tracking
```

❌ **Too Vague:**
```
Make a shopping cart
```

### Review BMAD Output

Always review the generated PRD before using it:
- Verify requirements match your vision
- Add missing acceptance criteria
- Clarify ambiguous requirements
- Add technical constraints

### Iterate on PRDs

PRDs are living documents:
- Update as you learn during implementation
- Add discovered requirements
- Refine user stories based on feedback
- Keep the PRD in sync with implementation

## Advanced BMAD Features

### Epic Breakdown (Level 3-4 Projects)

For complex projects, BMAD creates epic breakdowns:

```bash
# BMAD generates:
~/bmad/output/
├── project-prd.md           # Main PRD
├── epic-1-authentication.md # Epic details
├── epic-2-data-model.md     # Epic details
└── epic-3-ui-framework.md   # Epic details
```

Execute epics individually:
```bash
/compounding-engineering:work ~/bmad/output/epic-1-authentication.md
```

### Solutioning Phase (Level 3-4)

For architectural decisions:

1. BMAD creates solution architecture docs
2. "Just-in-time" technical specifications
3. System design diagrams
4. Technology stack recommendations

### Implementation Phase

BMAD can guide story-based development:
- Story creation
- Context generation
- Development workflow
- Review process
- Retrospective

## Troubleshooting

### BMAD Installation Fails

**Check Node version:**
```bash
node --version  # Should be 20+
```

**Clean install:**
```bash
rm -rf ~/bmad
npx bmad-method install --directory ~/bmad --ide claude-code
```

### Can't Find BMAD Agents

BMAD agents are in `~/bmad/agents/`. To use them:

```bash
cd ~/bmad
claude
# Now BMAD agents are available in this directory
```

### PRD Output Not Found

Check the output directory:
```bash
ls -la ~/bmad/output/
```

BMAD saves all generated documents here.

### /work Command Can't Find PRD

Use absolute path:
```bash
/compounding-engineering:work /Users/yourname/bmad/output/project-prd.md
```

Or copy PRD to project:
```bash
cp ~/bmad/output/project-prd.md ~/code/your-project/PRD.md
/compounding-engineering:work ./PRD.md
```

## Integration with Titanium Toolkit

### Voice Announcements During PRD Execution

As Titanium Toolkit implements your BMAD PRD, you'll hear:

**During Implementation:**
- "Created authentication module"
- "Updated API endpoints"
- "Test runner passing"

**On Completion:**
- "I implemented the authentication system with social login, created API endpoints, added tests, and set up the database schema. Everything is ready for review."

### Context Retention with Pieces

After working on a BMAD-generated project:

```bash
/catchup
```

Pieces will show:
- The PRD you executed
- Features implemented
- Tests that were run
- Where you left off

## Complete Example: Building a Blog Platform

### 1. Create PRD

```bash
cd ~/bmad
claude

# Create PRD
Create a comprehensive PRD for a blog platform with:
- User authentication (email/password)
- Post creation with rich text editor
- Comment system
- Search functionality
- RSS feed
- SEO optimization
- Admin dashboard
```

### 2. BMAD Output

BMAD generates:
```
~/bmad/output/blog-platform-prd.md
```

Contains:
- Project overview
- User stories
- Epic breakdown
- Technical requirements
- Success criteria

### 3. Execute Implementation

```bash
cd ~/code/blog-platform
/compounding-engineering:work ~/bmad/output/blog-platform-prd.md
```

Titanium Toolkit:
- @api-developer creates backend API
- @frontend-developer builds UI
- @doc-writer generates documentation
- @test-runner ensures quality

### 4. Review

```bash
/compounding-engineering:review
```

Reviewer agents check code quality.

### 5. Deploy

```bash
# Use devops-engineer agent
@devops-engineer Set up deployment to Railway
```

## Tips for Success

### Combine with Pieces /catchup

Before starting BMAD session:
```bash
/catchup
```

See recent work and context. This helps BMAD understand your ongoing projects.

### Save PRDs to Your Project

Copy important PRDs to your project repository:

```bash
mkdir -p ~/code/your-project/docs/
cp ~/bmad/output/project-prd.md ~/code/your-project/docs/PRD.md
git add docs/PRD.md
git commit -m "docs: Add project PRD from BMAD"
```

### Use BMAD for Refinement

Already have requirements? Use BMAD to refine them:

```bash
# Copy existing docs to BMAD
cp ~/code/your-project/rough-requirements.md ~/bmad/input/

# Ask BMAD to refine
Transform this rough requirements document into a comprehensive PRD:
[paste content or reference file]
```

## Resources

- **BMAD Repository**: https://github.com/bmad-code-org/BMAD-METHOD
- **BMAD Documentation**: Check `~/bmad/` after installation
- **Titanium Toolkit**: https://github.com/webdevtodayjason/titanium-plugins
- **compounding-engineering**: Install via `/plugin marketplace add EveryInc/every-marketplace`

## Next Steps

1. ✅ Install BMAD (`npx bmad-method install`)
2. ✅ Create your first PRD
3. ✅ Execute with `/compounding-engineering:work`
4. ✅ Let Titanium Toolkit build
5. ✅ Review with compounding-engineering
6. ✅ Use `/catchup` to retain context

---

With BMAD + Titanium Toolkit + compounding-engineering, you have a complete development pipeline from requirements to deployment!
