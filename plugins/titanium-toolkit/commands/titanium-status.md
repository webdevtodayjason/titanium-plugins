---
description: Show current workflow progress and status
---

# Titanium Status Command

You are reporting on the current workflow state and progress. This command provides a comprehensive view of where the project stands, what's been completed, and what's remaining.

## Overview

This command will:
1. Check for active workflow state
2. Query Pieces for recent work
3. Analyze TodoWrite progress (if available)
4. Check for existing plan
5. Calculate progress metrics
6. Present formatted status report
7. Optionally provide voice summary

---

## Step 1: Check for Active Workflow

### Check Workflow State File

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/hooks/utils/workflow/workflow_state.py get "$(pwd)"
```

**If workflow exists**:
- Parse the JSON response
- Extract:
  - workflow_type
  - goal
  - status (planning/in_progress/completed/failed)
  - current_phase
  - started_at timestamp
  - phases history

**If no workflow exists**:
- Report: "No active workflow found in this project"
- Check for plan anyway (might be planning only)
- Query Pieces for any previous work

---

## Step 2: Query Pieces for Context

Use Pieces LTM to get recent work history:

```
mcp__Pieces__ask_pieces_ltm(
  question: "What work has been done in the last session on this project at [current directory]? What was being worked on? What was completed? What was left unfinished?",
  chat_llm: "claude-sonnet-4-5",
  topics: ["workflow", "implementation", "development"],
  application_sources: ["Code"]
)
```

**Extract from Pieces**:
- Recent activities
- What was completed
- What's in progress
- Any issues encountered
- Last known state

---

## Step 3: Check for Plan

```bash
# Check if plan exists
ls .titanium/plan.json
```

**If plan exists**:
- Read `.titanium/plan.json`
- Extract:
  - Total epics count
  - Total stories count
  - Total tasks count
  - Estimated total time
  - List of agents needed

**Calculate progress** (if TodoWrite is available):
- Count completed tasks vs total tasks
- Calculate percentage complete
- Identify current task (first pending task)

---

## Step 4: Analyze TodoWrite Progress (if in active session)

**Note**: TodoWrite state is session-specific. This step only works if we're in the same session that created the workflow.

If TodoWrite is available in current session:
- Count total tasks
- Count completed tasks
- Count pending tasks
- Identify current task (first in_progress task)
- Calculate progress percentage

If TodoWrite not available:
- Use plan.json task count as reference
- Note: "Progress tracking available only during active session"

---

## Step 5: Calculate Metrics

### Progress Metrics

**Overall Progress**:
```
progress_percentage = (completed_tasks / total_tasks) * 100
```

**Time Metrics**:
```
elapsed_time = current_time - workflow.started_at
remaining_tasks = total_tasks - completed_tasks
avg_time_per_task = elapsed_time / completed_tasks (if > 0)
estimated_remaining = avg_time_per_task * remaining_tasks
```

**Phase Progress**:
- Identify which phase is active
- List completed phases with timestamps
- Show phase transition history

---

## Step 6: Present Status Report

### Format: Comprehensive Status

```
📊 Titanium Workflow Status

═══════════════════════════════════════════════

🎯 Goal: [workflow.goal]

📍 Current Phase: [current_phase]
   Status: [status emoji] [status]

⏱️  Timeline:
   Started: [formatted timestamp] ([X] hours/days ago)
   [If completed: Completed: [timestamp]]
   [If in progress: Elapsed: [duration]]

───────────────────────────────────────────────

📈 Progress: [X]% Complete

✅ Completed: [X] tasks
⏳ Pending: [Y] tasks
🔄 Current: [current task name if known]

───────────────────────────────────────────────

📦 Project Structure:
   Epics: [X]
   Stories: [Y]
   Tasks: [Z]
   Total Estimated Time: [time]

🤖 Agents Used/Planned:
   [List agents with their roles]

───────────────────────────────────────────────

📝 Recent Work (from Pieces):

[Summary from Pieces query - what was done recently]

Key Accomplishments:
- [Item 1]
- [Item 2]
- [Item 3]

Current Focus:
[What's being worked on now or what's next]

───────────────────────────────────────────────

🔄 Phase History:

1. ✅ Planning - Completed ([duration])
2. 🔄 Implementation - In Progress (started [time ago])
3. ⏳ Review - Pending
4. ⏳ Completion - Pending

───────────────────────────────────────────────

⏰ Time Estimates:

Elapsed: [duration]
Est. Remaining: [duration] (based on current pace)
Original Estimate: [total from plan]

[If ahead/behind schedule: [emoji] [X]% [ahead/behind] schedule]

───────────────────────────────────────────────

📁 Key Files:

Created/Modified:
[List from Pieces or plan if available]

Configuration:
- Plan: .titanium/plan.json
- State: .titanium/workflow-state.json
[If exists: - Review: .titanium/review-report.md]

───────────────────────────────────────────────

💡 Next Steps:

[Based on current state, suggest what should happen next]

1. [Next action item]
2. [Second action item]
3. [Third action item]

───────────────────────────────────────────────

🔊 Voice Summary Available
Say "yes" for voice summary of current status
```

---

## Step 7: Status Variations by Phase

### If Phase: Planning

```
📊 Status: Planning Phase

🎯 Goal: [goal]

Current Activity:
- Analyzing requirements
- Generating implementation plan
- Validating with vibe-check

Next: Implementation phase will begin after plan approval
```

### If Phase: Implementation

```
📊 Status: Implementation In Progress

🎯 Goal: [goal]

Progress: [X]% ([completed]/[total] tasks)

Current Task: [task name]
Agent: [current agent]

Recently Completed:
- [Task 1] by @agent-1
- [Task 2] by @agent-2
- [Task 3] by @agent-3

Up Next:
- [Next task 1]
- [Next task 2]

Estimated Remaining: [time]
```

### If Phase: Review

```
📊 Status: Quality Review Phase

🎯 Goal: [goal]

Implementation: ✅ Complete ([X] tasks finished)

Current Activity:
- Running quality review
- @code-reviewer analyzing code
- @security-scanner checking vulnerabilities
- @tdd-specialist reviewing tests

Next: Address review findings, then complete workflow
```

### If Phase: Completed

```
📊 Status: Workflow Complete ✅

🎯 Goal: [goal]

Completion Summary:
- Started: [timestamp]
- Completed: [timestamp]
- Duration: [total time]

Deliverables:
- [X] epics completed
- [Y] stories delivered
- [Z] tasks finished

Final Metrics:
- Test Coverage: [X]%
- Quality Review: [findings summary]
- All work stored in Pieces ✅

Next: Run /catchup in future sessions to resume context
```

### If No Active Workflow

```
📊 Status: No Active Workflow

Current Directory: [pwd]

No .titanium/workflow-state.json found

Checking for plan...
[If plan exists: Plan found but not yet executed]
[If no plan: No plan found]

Checking Pieces for history...
[Results from Pieces query]

---

Ready to start a new workflow?

Run:
- /titanium:plan [requirements] - Create implementation plan
- /titanium:work [requirements] - Start full workflow
```

---

## Step 8: Voice Summary (Optional)

**If user requests voice summary or says "yes" to voice option**:

Create concise summary for TTS (under 100 words):

```
"Workflow status: [Phase], [X] percent complete.
[Completed count] tasks finished, [pending count] remaining.
Currently working on [current task or phase activity].
[Key recent accomplishment].
Estimated [time] remaining.
[Next major milestone or action]."
```

**Example**:
```
"Workflow status: Implementation phase, sixty-seven percent complete.
Eight tasks finished, four remaining.
Currently implementing the login form component with the frontend developer agent.
Just completed the backend authentication API with all tests passing.
Estimated one hour remaining.
Next, we'll run the quality review phase."
```

**Announce using existing TTS**:
- Voice hooks will handle the announcement
- No need to call TTS directly

---

## Integration with Workflow Commands

### After /titanium:plan

```
User: /titanium:plan [requirements]
[... plan created ...]
User: /titanium:status

Shows:
- Phase: Planning (completed)
- Plan details
- Ready for /titanium:work
```

### During /titanium:work

```
User: /titanium:work
[... implementation in progress ...]
User: /titanium:status

Shows:
- Phase: Implementation (in progress)
- Progress: X%
- Current task
- Time estimates
```

### After /titanium:work

```
User: /titanium:work
[... completes ...]
User: /titanium:status

Shows:
- Phase: Completed
- Summary of deliverables
- Quality metrics
```

### Next Session

```
User: (new session)
/titanium:status

Shows:
- Workflow state from file
- Pieces context from previous session
- Can resume work
```

---

## Error Handling

### If Workflow State File Corrupted

```
⚠️  Workflow state file exists but is corrupted

Attempting to recover from Pieces...
[Query Pieces for last known state]

[If recovery successful: Use Pieces data]
[If recovery fails: Report what's known, suggest starting fresh]
```

### If Pieces Not Available

```
Note: Pieces MCP not available. Status based on local files only.

To enable full context recovery:
1. Install Pieces OS (https://pieces.app)
2. Install Pieces CLI (pip3 install pieces-cli)
3. Configure MCP (pieces mcp setup claude_code --stdio)
4. Restart Claude Code
```

### If No Information Available

```
📊 Status: No Data Available

Current Directory: [pwd]

- No workflow state file (.titanium/workflow-state.json)
- No plan file (.titanium/plan.json)
- Pieces query returned no results

This appears to be a new project or no workflows have been run yet.

Ready to start? Run:
- /titanium:plan - Create implementation plan
- /titanium:work - Start full workflow
```

---

## Use Cases

### Use Case 1: Check Progress Mid-Workflow

```
User: How's the workflow going?
Claude: Let me check the status.
[Runs /titanium:status]
Claude: We're 60% through implementation. 6 of 10 tasks complete.
        Currently working on the frontend login form.
        About 2 hours remaining.
```

### Use Case 2: Resume After Interruption

```
User: (new session) What was I working on?
Claude: Let me check.
[Runs /titanium:status]
Claude: You were implementing user authentication.
        Phase: Implementation (in progress)
        Last completed: Backend API by @api-developer
        Next up: Frontend forms by @frontend-developer

        Would you like to continue with /titanium:work?
```

### Use Case 3: Check Before Review

```
User: Is implementation done? Can we review?
Claude: Let me check status.
[Runs /titanium:status]
Claude: Yes! Implementation is 100% complete.
        All 12 tasks finished.
        Ready for quality review.

        Run /titanium:review to start the review process.
```

### Use Case 4: Daily Standup Info

```
User: What did we accomplish yesterday?
Claude: Checking status and history...
[Runs /titanium:status + Pieces query]
Claude: Yesterday's work:
        - Completed Backend API epic (3 stories, 7 tasks)
        - @api-developer implemented JWT middleware
        - @api-developer created login/register endpoints
        - @test-runner wrote integration tests
        - All tests passing

        Today: Moving to Frontend epic
```

---

## Voice Feedback

Voice hooks may announce:
- "Status check complete" (after generating report)
- "[X] percent complete" (if voice summary requested)

---

## Advanced Features (Future)

Potential enhancements:
- Progress visualization (ASCII charts)
- Time series data (velocity over time)
- Agent performance metrics
- Quality trend tracking
- Burndown charts

---

**This command provides comprehensive workflow status with context from state files, Pieces LTM, and current session, enabling users to track progress and make informed decisions about next steps.**
