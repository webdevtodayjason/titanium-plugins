---
description: Run comprehensive multi-agent quality review
---

# Titanium Review Command

You are coordinating a comprehensive quality review of the codebase. This command launches multiple review agents in parallel, aggregates their findings, and creates a detailed review report.

## Overview

This review process:
1. Identifies what code to review
2. Launches 3 review agents in parallel
3. Aggregates and categorizes findings
4. Uses vibe-check for meta-review
5. Creates comprehensive review report
6. Stores findings in Pieces LTM
7. Presents actionable summary

---

## Step 1: Identify Review Scope

### Determine What to Review

**Option A: Recent Changes** (default)
```bash
git diff --name-only HEAD~1
```
Reviews files changed in last commit.

**Option B: Current Branch Changes**
```bash
git diff --name-only main...HEAD
```
Reviews all changes in current branch vs main.

**Option C: Specific Files** (if user specified)
```bash
# User might say: /titanium:review src/api/*.ts
```
Use the files/pattern user specified.

**Option D: All Code** (if user requested)
```bash
# Find all source files
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.rb" \) -not -path "*/node_modules/*" -not -path "*/venv/*"
```

### Build File List

Create list of files to review. Store in memory for agent prompts.

**Example**:
```
Files to review:
- src/api/auth.ts
- src/middleware/jwt.ts
- src/routes/users.ts
- tests/api/auth.test.ts
```

---

## Step 2: Launch Review Agents in Parallel

**CRITICAL**: Launch all three agents in a **SINGLE message** with multiple Task calls.

This enables parallel execution for faster reviews.

### Agent 1: Code Reviewer

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
```

### Agent 2: Security Scanner

```
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
- Remediation steps

Severity mapping for aggregation:
- Critical → Critical (must fix)
- High → Important (should fix)
- Medium → Nice-to-have (optional)
- Low → Nice-to-have (optional)"
```

### Agent 3: Test Coverage Specialist

```
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

---

## Step 3: Wait for All Agents

All three agents will run in parallel. Wait for all to complete before proceeding.

Voice hooks will announce: "Review agents completed"

---

## Step 4: Aggregate Findings

### Collect All Findings

Gather results from all three agents:
- Code quality findings from @code-reviewer
- Security findings from @security-scanner
- Test coverage findings from @tdd-specialist

### Categorize by Severity

**🔴 Critical Issues** (must fix before deployment):
- Security vulnerabilities (Critical/High)
- Code that will cause bugs or crashes
- Core functionality with no tests

**🟡 Important Issues** (should fix soon):
- Security issues (Medium)
- Code quality problems that impact maintainability
- Important features with incomplete tests
- Performance issues

**🟢 Nice-to-have** (optional improvements):
- Code style improvements
- Refactoring opportunities
- Additional test coverage
- Documentation gaps

### Count Issues

```
Total findings:
- Critical: [X]
- Important: [Y]
- Nice-to-have: [Z]

By source:
- Code quality: [N] findings
- Security: [M] findings
- Test coverage: [P] findings
```

---

## Step 5: Meta-Review with vibe-check

Use vibe-check to provide AI oversight of the review:

```
mcp__vibe-check__vibe_check(
  goal: "Quality review of codebase changes",
  plan: "Ran parallel review: @code-reviewer, @security-scanner, @tdd-specialist",
  progress: "Review complete. Findings: [X] critical, [Y] important, [Z] minor.

Critical issues found:
[List each critical issue briefly]

Important issues found:
[List each important issue briefly]

Test coverage: approximately [X]%",
  uncertainties: [
    "Are there systemic quality issues we're missing?",
    "Is the security approach sound?",
    "Are we testing the right things?",
    "Any architectural concerns?"
  ]
)
```

**Process vibe-check response**:
- If vibe-check identifies systemic issues → Include in recommendations
- If vibe-check suggests additional areas to review → Note in report
- Include vibe-check insights in final report

---

## Step 6: Create Review Report

Write comprehensive report to `.titanium/review-report.md`:

```markdown
# Quality Review Report

**Date**: [current date and time]
**Project**: [project name or goal if known]
**Reviewers**: @code-reviewer, @security-scanner, @tdd-specialist

## Executive Summary

- 🔴 Critical issues: [X]
- 🟡 Important issues: [Y]
- 🟢 Nice-to-have: [Z]
- 📊 Test coverage: ~[X]%

**Overall Assessment**: [Brief 1-2 sentence assessment]

---

## Critical Issues 🔴

### 1. [Issue Title]

**Category**: [Code Quality | Security | Testing]
**File**: `path/to/file.ext:line`
**Severity**: Critical

**Issue**:
[Clear description of what's wrong]

**Risk/Impact**:
[Why this is critical]

**Recommendation**:
```[language]
// Show example fix if applicable
[code example]
```

**Steps to Fix**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

### 2. [Next Critical Issue]
[... repeat structure ...]

---

## Important Issues 🟡

### 1. [Issue Title]

**Category**: [Code Quality | Security | Testing]
**File**: `path/to/file.ext:line`
**Severity**: Important

**Issue**:
[Description]

**Impact**:
[Why this matters]

**Recommendation**:
[How to address it]

---

### 2. [Next Important Issue]
[... repeat structure ...]

---

## Nice-to-have Improvements 🟢

### Code Quality
- [Improvement 1 with file reference]
- [Improvement 2 with file reference]

### Testing
- [Test improvement 1]
- [Test improvement 2]

### Documentation
- [Doc improvement 1]
- [Doc improvement 2]

---

## Test Coverage Analysis

**Overall Coverage**: ~[X]%

**Files with Insufficient Coverage** (<80%):
- `file1.ts` - ~[X]% coverage
- `file2.ts` - ~[Y]% coverage

**Untested Critical Functions**:
- `functionName()` in file.ts:line
- `anotherFunction()` in file.ts:line

**Missing Test Categories**:
- [ ] Error condition tests
- [ ] Edge case tests
- [ ] Integration tests
- [ ] E2E tests for critical flows

**Recommendations**:
1. [Priority test to add]
2. [Second priority test]
3. [Third priority test]

---

## Security Analysis

**Vulnerabilities Found**: [X]
**Security Best Practices Violations**: [Y]

**Key Security Concerns**:
1. [Concern 1]
2. [Concern 2]

**Security Recommendations**:
1. [Priority 1 security fix]
2. [Priority 2 security fix]

---

## vibe-check Meta-Review

[Paste vibe-check assessment here]

**Systemic Issues Identified**:
[Any patterns or systemic problems vibe-check identified]

**Additional Recommendations**:
[Any suggestions from vibe-check that weren't captured by agents]

---

## Recommendations Priority List

### Must Do (Critical):
1. [Critical fix 1] - File: `path/to/file.ext:line`
2. [Critical fix 2] - File: `path/to/file.ext:line`

### Should Do (Important):
1. [Important fix 1] - File: `path/to/file.ext:line`
2. [Important fix 2] - File: `path/to/file.ext:line`
3. [Important fix 3] - File: `path/to/file.ext:line`

### Nice to Do (Optional):
1. [Optional improvement 1]
2. [Optional improvement 2]

---

## Files Reviewed

Total files: [X]

**Source Files** ([N] files):
- path/to/file1.ext
- path/to/file2.ext

**Test Files** ([M] files):
- path/to/test1.test.ext
- path/to/test2.test.ext

---

## Next Steps

1. Address all critical issues immediately
2. Plan to fix important issues in next sprint
3. Consider nice-to-have improvements for tech debt backlog
4. Re-run review after fixes: `/titanium:review`
```

---

## Step 7: Store Review in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Quality review findings for [project/files]",
  summary: "Comprehensive quality review completed by @code-reviewer, @security-scanner, @tdd-specialist.

Findings:
- Critical issues: [X] - [briefly list each critical issue]
- Important issues: [Y] - [briefly describe categories]
- Nice-to-have: [Z]

Test coverage: approximately [X]%

Security assessment: [summary - no vulnerabilities / minor issues / concerns found]

Code quality assessment: [summary - excellent / good / needs improvement]

vibe-check meta-review: [brief summary of vibe-check insights]

Key recommendations:
1. [Top priority recommendation]
2. [Second priority]
3. [Third priority]

All findings documented in .titanium/review-report.md with file:line references and fix recommendations.",
  files: [
    ".titanium/review-report.md",
    "list all reviewed source files",
    "list all test files"
  ],
  project: "$(pwd)"
)
```

---

## Step 8: Present Summary to User

```
🔍 Quality Review Complete

📊 Summary:
- 🔴 [X] Critical Issues
- 🟡 [Y] Important Issues
- 🟢 [Z] Nice-to-have Improvements
- 📈 Test Coverage: ~[X]%

📄 Full Report: .titanium/review-report.md

---

⚠️  Critical Issues (must fix):

1. [Issue 1 title]
   File: `path/to/file.ext:line`
   [Brief description]

2. [Issue 2 title]
   File: `path/to/file.ext:line`
   [Brief description]

[... list all critical issues ...]

---

💡 Top Recommendations:

1. [Priority 1 action item]
2. [Priority 2 action item]
3. [Priority 3 action item]

---

🤖 vibe-check Assessment:
[Brief quote or summary from vibe-check]

---

Would you like me to:
1. Fix the critical issues now
2. Create GitHub issues for these findings
3. Provide more details on any specific issue
4. Skip and continue (not recommended if critical issues exist)
```

### Handle User Response

**If user wants fixes**:
- Address critical issues one by one
- After each fix, run relevant tests
- Re-run review to verify fixes
- Update review report

**If user wants GitHub issues**:
- Create issues for each critical and important finding
- Include all details from review report
- Provide issue URLs

**If user wants more details**:
- Read specific sections of review report
- Explain the issue and fix in more detail

**If user says continue**:
- Acknowledge and complete
- Remind that issues are documented in review report

---

## Error Handling

### If No Files to Review

```
⚠️  No files found to review.

This could mean:
- No changes since last commit
- Working directory is clean
- Specified files don't exist

Would you like to:
1. Review all source files
2. Specify which files to review
3. Cancel review
```

### If Review Agents Fail

```
❌ Review failed

Agent @[agent-name] encountered an error: [error]

Continuing with other review agents...

[Proceed with available results]
```

### If vibe-check Not Available

```
Note: vibe-check MCP is not available. Proceeding without meta-review.

To enable AI-powered meta-review:
1. Create ~/.vibe-check/.env
2. Add API key (GEMINI_API_KEY, OPENAI_API_KEY, or OPENROUTER_API_KEY)
3. Restart Claude Code
```

---

## Integration with Workflow

**After /titanium:work**:
```
User: /titanium:work
[... implementation completes ...]
User: /titanium:review
[... review runs ...]
```

**Standalone Usage**:
```
User: /titanium:review
# Reviews recent changes
```

**With File Specification**:
```
User: /titanium:review src/api/*.ts
# Reviews only specified files
```

**Before Committing**:
```
User: I'm about to commit. Can you review my changes?
Claude: /titanium:review
[... review runs on uncommitted changes ...]
```

---

## Voice Feedback

Voice hooks automatically announce:
- "Starting quality review" (at start)
- "Review agents completed" (after parallel execution)
- "Review complete: [X] issues found" (at end)

No additional voice calls needed.

---

## Example Outputs

### Example 1: No Issues Found

```
🔍 Quality Review Complete

📊 Summary:
- 🔴 0 Critical Issues
- 🟡 0 Important Issues
- 🟢 3 Nice-to-have Improvements
- 📈 Test Coverage: ~92%

✅ No critical or important issues found!

💡 Optional Improvements:
1. Consider extracting duplicated validation logic in auth.ts and users.ts
2. Add JSDoc comments to public API methods
3. Increase test coverage for edge cases in payment module

Code quality: Excellent
Security: No vulnerabilities found
Testing: Comprehensive coverage

📄 Full details: .titanium/review-report.md
```

### Example 2: Critical Issues Found

```
🔍 Quality Review Complete

📊 Summary:
- 🔴 2 Critical Issues
- 🟡 5 Important Issues
- 🟢 12 Nice-to-have Improvements
- 📈 Test Coverage: ~65%

⚠️  CRITICAL ISSUES (must fix):

1. SQL Injection Vulnerability
   File: `src/api/users.ts:45`
   User input concatenated directly into SQL query
   Risk: Attacker could read/modify database

2. Missing Authentication Check
   File: `src/api/admin.ts:23`
   Admin endpoint has no auth middleware
   Risk: Unauthorized access to admin functions

💡 MUST DO:
1. Use parameterized queries for all SQL
2. Add authentication middleware to admin routes
3. Add tests for authentication flows

Would you like me to fix these critical issues now?
```

---

**This command provides comprehensive multi-agent quality review with actionable findings and clear priorities.**
