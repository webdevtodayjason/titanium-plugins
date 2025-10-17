---
description: Generate BMAD architecture document from PRD
---

# BMAD Architecture - Generate Technical Architecture

Use the architect subagent to create comprehensive technical architecture for this project following BMAD methodology.

## Task Delegation

First check if the PRD exists, then launch the architect subagent to handle the complete architecture generation workflow.

## Process

### Step 1: Verify Prerequisites

Check that PRD exists before delegating to architect:

```bash
ls bmad-backlog/prd/prd.md 2>/dev/null || echo "PRD not found"
```

**If PRD NOT found**:
```
❌ Error: PRD not found at bmad-backlog/prd/prd.md

Architecture generation requires a PRD to work from.

Please run: /titanium-toolkit:bmad-prd first
(Or /titanium-toolkit:bmad-start for complete guided workflow)
```

Stop here - do not launch architect without PRD.

**If PRD exists**: Continue to Step 2.

### Step 2: Launch Architect Subagent

Use the Task tool to launch the architect subagent in its own context window:

```
Task(
  description: "Generate BMAD architecture",
  prompt: "Create comprehensive technical architecture document following BMAD methodology.

Input:
- PRD: bmad-backlog/prd/prd.md
- Research findings: bmad-backlog/research/*.md (if any exist)

Output:
- Architecture document: bmad-backlog/architecture/architecture.md

Requirements:
1. Read the PRD to understand requirements
2. Check for research findings and incorporate recommendations
3. Generate architecture using bmad_generator MCP tool
4. Review tech stack with user and get approval
5. Validate architecture using bmad_validator MCP tool
6. Run vibe-check to validate architectural decisions
7. Store result in Pieces for future reference
8. Present summary with next steps

**IMPORTANT**: Keep your summary response BRIEF (under 500 tokens). Just return:
- Confirmation architecture is complete
- Proposed tech stack (2-3 sentences)
- MVP cost estimate
- Any critical decisions made

DO NOT include the full architecture content in your response - it's already saved to the file.

Follow your complete architecture workflow from the bmad-methodology skill.

Project path: $(pwd)",
  subagent_type: "architect"
)
```

The architect subagent will handle:
- Reading PRD and research findings
- Generating architecture document (1000-1500 lines)
- Tech stack selection and user approval
- Validation (structural and vibe-check)
- Pieces storage
- Summary presentation

### Step 3: Return Results

The architect will return a summary when complete. Present this to the user.

## What the Architect Creates

The architect subagent generates `bmad-backlog/architecture/architecture.md` containing:

- **System Overview**: High-level architecture diagram (ASCII), component descriptions
- **Technology Stack**: Complete stack with rationale for each choice
- **Component Details**: Detailed design for each system component
- **Database Design**: Complete SQL schemas with CREATE TABLE statements
- **API Design**: Endpoint specifications with request/response examples
- **Security Architecture**: Auth, rate limiting, encryption, security controls
- **Infrastructure**: Deployment strategy, scaling plan, CI/CD pipeline
- **Monitoring**: Metrics, logging, tracing, alerting specifications
- **Cost Analysis**: MVP costs and production projections
- **Technology Decisions Table**: Each tech choice with rationale

## Integration with Research

If research findings exist in `bmad-backlog/research/`, the architect will:
- Read all RESEARCH-*-findings.md files
- Extract vendor/technology recommendations
- Incorporate into architecture decisions
- Reference research in Technology Decisions table
- Use research pricing in cost estimates

## Voice Feedback

Voice hooks announce:
- "Generating architecture" (when starting)
- "Architecture complete" (when finished)

## Cost

Typical cost: ~$0.08 per architecture generation (Claude Sonnet 4.5 API usage in bmad_generator tool)

---

**This command delegates to the architect subagent who creates the complete technical blueprint!**
