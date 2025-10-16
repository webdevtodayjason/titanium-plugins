---
description: Run CodeRabbit CLI analysis on uncommitted changes
---

# CodeRabbit Review Command

You are running CodeRabbit CLI analysis to catch race conditions, memory leaks, security vulnerabilities, and logic errors in uncommitted code changes.

## Purpose

CodeRabbit CLI provides AI-powered static analysis that detects:
- Race conditions in concurrent code
- Memory leaks and resource leaks
- Security vulnerabilities
- Logic errors and edge cases
- Performance issues
- Code quality problems

This complements the 3-agent review by finding issues that require deep static analysis.

## Prerequisites

**CodeRabbit CLI must be installed**:

Check installation:
```bash
command -v coderabbit >/dev/null 2>&1 || echo "Not installed"
```

**If not installed**:
```
❌ CodeRabbit CLI not found

CodeRabbit CLI is optional but provides enhanced code analysis.

To install:
  curl -fsSL https://cli.coderabbit.ai/install.sh | sh
  source ~/.zshrc  # or your shell rc file

Then authenticate:
  coderabbit auth login

See: https://docs.coderabbit.ai/cli/overview

Skip CodeRabbit and continue? (yes/no)
```

If skip: Exit
If install: Wait for user to install, then continue

## Process

### Step 1: Check Authentication

```bash
coderabbit auth status
```

**If not authenticated**:
```
⚠️  CodeRabbit not authenticated

For enhanced reviews (with team learnings):
  coderabbit auth login

Continue without authentication? (yes/no)
```

Authentication is optional but provides better reviews (Pro feature).

### Step 2: Choose Review Mode

Ask user:
```
CodeRabbit Review Mode:

1. **AI-Optimized** (--prompt-only)
   - Token-efficient output
   - Optimized for Claude to parse
   - Quick fix application
   - Recommended for workflows

2. **Detailed** (--plain)
   - Human-readable detailed output
   - Comprehensive explanations
   - Good for learning
   - More verbose

Which mode? (1 or 2)
```

Store choice.

### Step 3: Determine Review Scope

**Default**: Uncommitted changes only

**Options**:
```
What should CodeRabbit review?

1. Uncommitted changes only (default)
2. All changes vs main branch
3. All changes vs specific branch

Scope:
```

**Map to flags**:
- Option 1: `--type uncommitted`
- Option 2: `--base main`
- Option 3: `--base [branch name]`

### Step 4: Run CodeRabbit in Background

**For AI-Optimized mode**:
```bash
# Run in background (can take 7-30 minutes)
coderabbit --prompt-only --type uncommitted
```

**For Detailed mode**:
```bash
coderabbit --plain --type uncommitted
```

Use Bash tool with `run_in_background: true`

Show user:
```
🤖 CodeRabbit Analysis Running...

This will take 7-30 minutes depending on code size.
Running in background - you can continue working.

I'll check progress periodically.
```

### Step 5: Wait for Completion

Check periodically with BashOutput tool:
```bash
# Check if CodeRabbit completed
# Look for completion markers in output
```

Every 2-3 minutes, show:
```
CodeRabbit analyzing... ([X] minutes elapsed)
```

When complete:
```
✅ CodeRabbit analysis complete!
```

### Step 6: Parse Findings

**If --prompt-only mode**:
- Read structured output
- Extract issues by severity:
  - Critical
  - High
  - Medium
  - Low

**If --plain mode**:
- Show full output to user
- Ask if they want Claude to fix issues

### Step 7: Present Findings

```
🤖 CodeRabbit Analysis Complete

⏱️  Duration: [X] minutes

📊 Findings:
- 🔴 Critical: [X] issues
- 🟠 High: [Y] issues
- 🟡 Medium: [Z] issues
- 🟢 Low: [W] issues

Critical Issues:
1. Race condition in auth.ts:45
   Issue: Shared state access without lock
   Fix: Add mutex or use atomic operations

2. Memory leak in websocket.ts:123
   Issue: Event listener not removed on disconnect
   Fix: Add cleanup in disconnect handler

[List all critical and high issues]

Would you like me to fix these issues?
1. Fix critical and high priority (recommended)
2. Fix critical only
3. Show me the issues, I'll fix manually
4. Skip (not recommended)
```

### Step 8: Apply Fixes (if requested)

**For each critical/high issue**:
1. Read the issue details
2. Locate the problematic code
3. Apply CodeRabbit's suggested fix
4. Run relevant tests
5. Mark as fixed

Show progress:
```
Fixing issues...
✅ Fixed race condition in auth.ts
✅ Fixed memory leak in websocket.ts
✅ Fixed SQL injection in users.ts
⏳ Fixing error handling in api.ts...
```

### Step 9: Optional Re-run

After fixes:
```
Fixes applied: [X] critical, [Y] high

Re-run CodeRabbit to verify fixes? (yes/no)
```

**If yes**:
```bash
coderabbit --prompt-only --type uncommitted
```

Check no new critical issues introduced.

### Step 10: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "CodeRabbit review findings for [files]",
  summary: "CodeRabbit CLI analysis complete. Findings: [X] critical, [Y] high, [Z] medium, [W] low. Critical issues: [list]. High issues: [list]. Fixes applied: [what was fixed]. Duration: [X] minutes. Verified: [yes/no].",
  files: [
    "list all reviewed files",
    ".titanium/coderabbit-report.md" (if created)
  ],
  project: "$(pwd)"
)
```

### Step 11: Present Summary

```
✅ CodeRabbit Review Complete!

📊 Summary:
- Duration: [X] minutes
- Files reviewed: [N]
- Issues found: [Total]
  - Critical: [X] ([fixed/pending])
  - High: [Y] ([fixed/pending])
  - Medium: [Z]
  - Low: [W]

✅ Critical issues: All fixed
✅ High priority: All fixed
⚠️  Medium/Low: Review manually if needed

💾 Findings stored in Pieces

---

Next steps:
1. Run tests to verify fixes
2. Run /titanium:review for additional validation
3. Or continue with your workflow
```

## Error Handling

### If CodeRabbit Not Installed

```
⚠️  CodeRabbit CLI not found

CodeRabbit is optional but provides enhanced static analysis.

Would you like to:
1. Install now (I'll guide you)
2. Skip and use 3-agent review only
3. Cancel

Choose:
```

### If CodeRabbit Times Out

```
⏰ CodeRabbit taking longer than expected

Analysis started [X] minutes ago.
Typical duration: 7-30 minutes.

Options:
1. Keep waiting
2. Cancel and proceed without CodeRabbit
3. Check CodeRabbit output so far

What would you like to do?
```

### If No Changes to Review

```
ℹ️  No uncommitted changes found

CodeRabbit needs changes to review.

Options:
1. Review all changes vs main branch
2. Specify different base branch
3. Cancel

Choose:
```

## Integration with Workflow

### Standalone Usage

```bash
/coderabbit:review
# Runs analysis
# Applies fixes
# Done
```

### Part of /titanium:work

```bash
/titanium:work
# ... implementation ...
# Phase 3.5: CodeRabbit (if installed)
# ... 3-agent review ...
# Complete
```

### Before Committing

```bash
# Before commit
/coderabbit:review
# Fix critical issues
# Then commit
```

## Voice Feedback

Voice hooks announce:
- "Running CodeRabbit analysis" (when starting)
- "CodeRabbit complete: [X] issues found" (when done)
- "Applying CodeRabbit fixes" (during fixes)
- "CodeRabbit fixes complete" (after fixes)

## Cost

**CodeRabbit pricing**:
- Free tier: Basic analysis, limited usage
- Pro: Enhanced reviews with learnings
- Enterprise: Custom limits

**Not included in titanium-toolkit pricing** - separate service.

---

**This command provides deep static analysis to catch issues agents might miss!**
