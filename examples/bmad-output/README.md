# BMAD Example Output

This folder contains example output from the BMAD document generation system.

**Generated from**: Simple idea: "Mobile puzzle game for learning math"
**Command used**: `/bmad:start` (simulated with utilities)
**Time**: ~2 minutes (GPT-4 generation)
**Cost**: ~$0.20

## Files

- `product-brief.md` - High-level vision and goals
- `prd/prd.md` - Complete Product Requirements Document (5 epics, comprehensive requirements)
- `epics/EPIC-001-foundation.md` - Foundation epic with user stories
- Architecture document (not included in examples due to size)

## What This Shows

**Product Brief**:
- Executive summary with vision
- Problem statement
- Target users (children + parents)
- MVP scope
- Technical considerations

**PRD**:
- 5 epics (Foundation, Adaptive Learning, Engaging Gameplay, Progress Tracking, Reward System)
- User stories organized by epic
- Feature requirements with acceptance criteria
- Technical/data/AI requirements
- Go-to-market strategy
- Risks and open questions

**Architecture** (not included - typically 1000-1500 lines):
- System overview
- Tech stack recommendations
- Component details with code examples
- Database schemas (SQL CREATE TABLE statements)
- Infrastructure and deployment plans
- Security architecture
- Monitoring and observability

**Epic** File:
- Epic header with metadata
- User stories in STORY-XXX-YY format
- Acceptance criteria checkboxes
- Technical notes

## How to Use

This shows you what `/bmad:start` will generate for your project.

**To generate your own BMAD backlog**:

1. In Claude Code, navigate to your project
2. Run the slash command: `/bmad:start`
3. Answer the interactive questions
4. Get similar comprehensive documentation for your project

**Note**: `/bmad:start` is a slash command in Claude Code (not a shell command). Type it in the Claude Code prompt.
