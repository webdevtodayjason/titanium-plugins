# Titanium Toolkit - Testing Guide

**Version**: 2.1.0
**Last Updated**: October 15, 2025

Quick guide for testing Titanium Toolkit commands and workflows.

---

## Prerequisites

Before testing, verify installation:

```bash
./verify-installation.sh
```

Should show: "🎉 All checks passed!"

---

## Cross-Platform Compatibility

**Titanium Toolkit works on**:
- ✅ macOS (tested)
- ✅ Linux
- ✅ Windows WSL2
- ✅ Windows (native)

**Path handling**:
- Commands use `$(pwd)` - shell-expanded to absolute path
- Utilities use `pathlib.Path` - cross-platform path objects
- UV works on all platforms
- No hardcoded paths or platform-specific code

**When testing**: Use same commands on any OS - paths handled automatically!

---

## Quick Smoke Tests

### Test 1: Brief Generation (30 seconds)

```bash
cd /tmp/test-brief
/bmad:brief "Social network for developers"
```

**Expected**:
- Creates `bmad-backlog/product-brief.md`
- Contains all sections (Executive Summary, Problem Statement, etc.)
- Voice: "Product brief complete"

**Verify**:
```bash
ls bmad-backlog/product-brief.md
grep "Executive Summary" bmad-backlog/product-brief.md
```

---

### Test 2: Implementation Plan (1 minute)

```bash
cd /tmp/test-plan
/titanium:plan "Add user authentication with JWT"
```

**Expected**:
- Creates `.titanium/plan.json` and `.titanium/plan.md`
- Shows epic/story/task breakdown
- Assigns agents correctly
- Voice: "Plan created with X epics"

**Verify**:
```bash
ls .titanium/plan.json
cat .titanium/plan.md
```

---

### Test 3: Status Check (instant)

```bash
cd /tmp/test-plan
/titanium:status
```

**Expected**:
- Shows workflow state
- Queries Pieces for context
- Displays progress metrics

---

### Test 4: Research Prompt (instant)

```bash
cd /tmp/test-research
/bmad:research "authentication providers"
```

**Expected**:
- Creates `bmad-backlog/research/RESEARCH-authentication-providers-prompt.md`
- Creates `bmad-backlog/research/RESEARCH-authentication-providers-findings.md`
- Templates are comprehensive

**Verify**:
```bash
ls bmad-backlog/research/
cat bmad-backlog/research/RESEARCH-*-prompt.md | head -20
```

---

## Integration Tests

### Test 5: BMAD to Implementation (30 minutes)

```bash
# 1. Generate backlog
cd /tmp/full-integration-test
/bmad:start

# Answer questions:
# - Idea: "Todo app with AI categorization"
# - Problem: "People forget tasks"
# - Users: "Busy professionals"
# ... answer all questions

# 2. Verify backlog created
ls bmad-backlog/
# Should show: product-brief.md, prd/, architecture/, epics/, STORY-INDEX.md

# 3. Plan from epic
/titanium:plan bmad-backlog/epics/EPIC-001-foundation.md

# Expected: Plan created with tasks from epic stories

# 4. Check status
/titanium:status

# Expected: Shows planning phase complete
```

---

### Test 6: Complete BMAD Workflow (45 minutes)

```bash
cd /tmp/bmad-full-test
/bmad:start
```

**Interactive workflow steps**:
1. Choose mode (Interactive or YOLO)
2. Provide project idea
3. Answer clarifying questions
4. Review product brief
5. Review PRD and epic structure
6. (Optional) Complete any research prompts
7. Review architecture and tech stack
8. Wait for all epics to generate
9. Review story index

**Expected output**:
```
bmad-backlog/
├── product-brief.md
├── prd/
│   └── prd.md
├── architecture/
│   └── architecture.md
├── epics/
│   ├── EPIC-001-foundation.md
│   ├── EPIC-002-*.md
│   └── ... (3-6 epic files)
└── STORY-INDEX.md
```

**Verify**:
```bash
# Check all files exist
ls -R bmad-backlog/

# Check Epic 1 is Foundation
grep "EPIC-001" bmad-backlog/epics/EPIC-001-*.md

# Check story count
grep "Total User Stories" bmad-backlog/STORY-INDEX.md
```

---

## End-to-End Test

### Test 7: Idea to Working Code (full day)

```bash
# 1. Start fresh
mkdir my-test-app
cd my-test-app
git init

# 2. Generate backlog
/bmad:start
# Answer: "Contact form with email validation and file uploads"
# ~45 minutes

# 3. Plan first epic
/titanium:plan bmad-backlog/epics/EPIC-001-foundation.md
# ~2 minutes

# 4. Implement
/titanium:work
# ~2-4 hours depending on complexity

# 5. Review
/titanium:review
# ~5 minutes

# 6. Check final status
/titanium:status
# Should show: 100% complete

# 7. Verify code exists
ls src/
ls tests/
```

**Success criteria**:
- ✅ All documents generated
- ✅ Implementation plan created
- ✅ Code files created
- ✅ Tests passing
- ✅ Review report shows no critical issues

---

## Utility Tests

### Test workflow_state.py

```bash
cd /tmp/test-utils

# Init
uv run ~/.claude/hooks/utils/workflow/workflow_state.py init "$(pwd)" "development" "Test"

# Verify
ls .titanium/workflow-state.json
cat .titanium/workflow-state.json

# Update
uv run ~/.claude/hooks/utils/workflow/workflow_state.py update_phase "$(pwd)" "implementation" "in_progress"

# Get
uv run ~/.claude/hooks/utils/workflow/workflow_state.py get "$(pwd)"

# Complete
uv run ~/.claude/hooks/utils/workflow/workflow_state.py complete "$(pwd)"
```

---

### Test plan_parser.py

```bash
cd /tmp/test-utils

# Create requirements
echo "Build a REST API for managing books" > requirements.md

# Parse
uv run ~/.claude/hooks/utils/workflow/plan_parser.py requirements.md "$(pwd)"

# Verify
ls .titanium/plan.json
cat .titanium/plan.json | jq '.epics'
```

---

### Test bmad_generator.py

```bash
cd /tmp/test-bmad

# Brief
uv run ~/.claude/hooks/utils/bmad/bmad_generator.py brief "AI chatbot" "$(pwd)"

# Verify
ls bmad-backlog/product-brief.md

# PRD
uv run ~/.claude/hooks/utils/bmad/bmad_generator.py prd bmad-backlog/product-brief.md "$(pwd)"

# Verify
ls bmad-backlog/prd/prd.md
grep "### Epic 1" bmad-backlog/prd/prd.md
```

---

### Test bmad_validator.py

```bash
cd /tmp/test-bmad

# Validate PRD
uv run ~/.claude/hooks/utils/bmad/bmad_validator.py prd bmad-backlog/prd/prd.md

# Expected: "✅ VALID - All required sections present"

# Validate all
uv run ~/.claude/hooks/utils/bmad/bmad_validator.py all bmad-backlog/

# Expected: Shows status for all documents
```

---

### Test research_generator.py

```bash
cd /tmp/test-research

# Generate prompt
uv run ~/.claude/hooks/utils/bmad/research_generator.py prompt "hosting platforms" "$(pwd)"

# Verify
ls bmad-backlog/research/RESEARCH-hosting-platforms-prompt.md

# Generate template
uv run ~/.claude/hooks/utils/bmad/research_generator.py template "hosting platforms" "$(pwd)"

# Verify
ls bmad-backlog/research/RESEARCH-hosting-platforms-findings.md
```

---

## Common Issues & Fixes

### Issue: "OPENAI_API_KEY not found"

```bash
# Check key
cat ~/.env | grep OPENAI_API_KEY

# If missing, add it
echo 'OPENAI_API_KEY=sk-your-key' >> ~/.env

# Restart Claude Code
```

---

### Issue: "uv: command not found"

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Restart terminal
```

---

### Issue: "Epic 1 is not Foundation"

**Expected**: Epic 1 should always be "Foundation" or "Infrastructure"

**If wrong**:
- PRD generation prompt emphasizes this
- Should self-correct
- If not, regenerate PRD with emphasis on foundation first

---

### Issue: Voice not working

```bash
# Test ElevenLabs
echo "Test" | uv run ~/.claude/hooks/utils/tts/elevenlabs_tts.py

# Test fallback
say "Test"
```

Voice is optional - fallback to `say` works without API key.

---

## Test Checklist

### Before Release

- [ ] All 13 commands installed
- [ ] All 5 utilities work standalone
- [ ] `/bmad:brief` generates valid brief
- [ ] `/bmad:start` completes full workflow
- [ ] `/titanium:plan` reads epic files
- [ ] `/titanium:work` implements from plan
- [ ] `/titanium:review` finds issues
- [ ] `/titanium:status` shows progress
- [ ] vibe-check integration works
- [ ] Pieces integration works
- [ ] Voice announcements work
- [ ] verify-installation.sh passes
- [ ] Example outputs match format

### Quick Validation

```bash
# Run full test suite
cd /Users/sem/code/titanium-plugins

# Test utilities
for script in plugins/titanium-toolkit/hooks/utils/**/*.py; do
  echo "Testing $script"
  uv run "$script" 2>&1 | head -3
done

# Test verification
./verify-installation.sh
```

---

## Success Criteria

**All tests pass if**:
- ✅ Documents generated match BMAD format
- ✅ Epic 1 is always Foundation
- ✅ All required sections present
- ✅ Cross-references work (PRD → Architecture → Epics)
- ✅ Integration works (/bmad → /titanium)
- ✅ Voice announces progress
- ✅ vibe-check validates quality
- ✅ Pieces stores memories
- ✅ No errors during generation
- ✅ File paths correct

---

## Performance Benchmarks

**Expected timings**:
- `/bmad:brief`: ~30 seconds
- `/bmad:prd`: ~1 minute
- `/bmad:architecture`: ~2 minutes (2-part generation)
- `/bmad:epic`: ~30 seconds per epic
- `/bmad:start`: ~45 minutes total (interactive)
- `/titanium:plan`: ~1 minute
- `/titanium:status`: <1 second

**Cost per workflow**:
- BMAD complete backlog: ~$0.22
- Titanium workflow: ~$0.10
- Total idea to code: ~$0.62

---

**Happy Testing!** 🚀
