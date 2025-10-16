---
description: Generate BMAD architecture document from PRD
---

# BMAD Architecture - Generate Technical Architecture

You are generating a comprehensive Architecture Document following BMAD methodology. This translates product requirements into technical design with code examples, schemas, and infrastructure plans.

## Purpose

Create detailed technical architecture that defines:
- System design and component architecture
- Technology stack decisions
- Database schemas (SQL)
- Infrastructure and deployment
- Security architecture
- Monitoring and observability

## Process

### Step 1: Check for PRD

```bash
ls bmad-backlog/prd/prd.md 2>/dev/null || echo "No PRD found"
```

**If PRD NOT found**:
```
❌ Error: PRD not found

Architecture generation requires a PRD.

Please run: /bmad:prd
(Or /bmad:start for complete guided workflow)
```
Stop here.

**If PRD exists**:
- Read it with Read tool
- Extract technical requirements
- Continue

### Step 2: Check for Research Findings

```bash
ls bmad-backlog/research/*.md 2>/dev/null || echo "No research found"
```

**If research findings exist**:
- Read all RESEARCH-*-findings.md files
- Extract recommendations (data vendors, auth providers, etc.)
- Use these in architecture

**If no research**:
- Architecture will make best recommendations
- Note to user: "No research findings. Making recommendations based on best practices."

### Step 3: Generate Architecture

Use bmad_generator.py utility:

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py architecture "bmad-backlog/prd/prd.md" "$(pwd)"
```

This creates `bmad-backlog/architecture/architecture.md` (1000-1500 lines).

**Generated in 2 parts** (GPT-4 token limits):
- Part 1: System Overview → Component Details
- Part 2: Data Architecture → Monitoring & Appendix

**Includes**:
- ASCII architecture diagrams
- Complete database schemas (SQL CREATE TABLE statements)
- Code examples (Python, TypeScript, etc.)
- Infrastructure configurations
- Security implementation code
- CI/CD pipeline YAML
- Monitoring metric examples
- Technology decisions table with rationale
- Cost estimates (MVP and Production)

### Step 4: Review Tech Stack with User

Extract and present tech stack:

```
🏗️  Architecture Generated!

Proposed Tech Stack:
- Frontend: {{framework from PRD or inferred}}
- Backend: {{framework from PRD or inferred}}
- Database: {{database from PRD or inferred}}
- Cache: {{Redis or similar}}
- Hosting: {{Railway/Vercel/etc for MVP}}

{{If research findings exist:}}
Based on your research:
- {{Decision 1 from research}}
- {{Decision 2 from research}}

Approve this stack, or specify alternatives?
```

**If user wants changes**:
- Note the changes
- Regenerate architecture with preferences
- Can run utility again with additional context

**If user approves**:
- Continue

### Step 5: Validate Architecture

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_validator.py architecture "bmad-backlog/architecture/architecture.md"
```

**Check validation results**:
- All required sections present
- Code examples included
- Cost estimates present
- Technology decisions documented

If validation fails, regenerate missing sections.

### Step 6: Validate with vibe-check

```
mcp__vibe-check__vibe_check(
  goal: "Create technical architecture for {{project}}",
  plan: "Generated architecture with: System design, tech stack ({{stack}}), database schemas, infrastructure plan, security architecture, deployment strategy",
  uncertainties: [
    "Is the tech stack appropriate for requirements?",
    "Are database schemas complete?",
    "Is infrastructure scalable?",
    "Any security gaps?"
  ]
)
```

**Process vibe-check feedback**:
- If architectural concerns → Present to user
- If recommendations → Incorporate into architecture
- If approved → Continue

### Step 7: Reference Research Findings

**If research documents exist**:
```
Cross-reference complete:
✅ Data vendor choice: {{vendor}} (from RESEARCH-data-vendors-findings.md)
✅ Auth provider: {{provider}} (from RESEARCH-auth-findings.md)
✅ Hosting: {{platform}} (from RESEARCH-hosting-findings.md)

All research findings incorporated into Technology Decisions table.
```

### Step 8: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Technical architecture for {{project}}",
  summary: "Complete architecture document generated. Tech stack: {{stack summary}}. Database: {{database with key tables}}. Infrastructure: {{hosting}} for MVP, {{production plan}} for scale. Security: {{auth approach, rate limiting, encryption}}. Monitoring: {{metrics, logging}}. Cost estimate: ${{MVP cost}}/month MVP, ${{prod cost}}/month production. {{If research:}} Based on research findings: {{research summary}}. Ready for epic generation.",
  files: [
    "bmad-backlog/prd/prd.md",
    "bmad-backlog/architecture/architecture.md",
    "bmad-backlog/research/*.md" (if exists)
  ],
  project: "$(pwd)"
)
```

### Step 9: Present Summary

```
✅ Technical Architecture Complete!

📄 Location: bmad-backlog/architecture/architecture.md

🏗️  Architecture Summary:

Tech Stack:
- Frontend: {{framework}}
- Backend: {{framework}}
- Database: {{database}}
- Cache: {{Redis/etc}}
- Infrastructure: {{hosting}}

📐 Includes:
- Complete system design (ASCII diagrams)
- Database schemas ({{N}} tables with SQL)
- {{M}} code examples (Python, TypeScript, SQL)
- Security architecture (auth, rate limiting, encryption)
- Deployment strategy (CI/CD, migrations, blue-green)
- Monitoring plan (metrics, logging, tracing)
- Cost estimates (MVP: ${{X}}/mo, Production: ${{Y}}/mo)

📏 Document Size: ~{{line count}} lines

{{If research used:}}
✅ Based on research findings:
- {{Research-based decision 1}}
- {{Research-based decision 2}}

✅ vibe-check validated architecture

---

💡 Next Steps:

Option 1: Generate Epics (Recommended)
Run: /bmad:epic 1
(Generate each epic with detailed stories)

Or generate all at once:
Run: /bmad:start
(Will use this architecture to generate all epic files)

Option 2: Review Architecture first
Open: bmad-backlog/architecture/architecture.md
(Review database schemas, tech decisions, costs)

Ready to proceed?
```

## Error Handling

### If PRD Not Found

```
❌ PRD not found at bmad-backlog/prd/prd.md

Architecture generation requires a PRD to work from.

Please run: /bmad:prd
(Or /bmad:start for complete workflow)
```

### If OPENAI_API_KEY Missing

```
❌ Error: OPENAI_API_KEY not found

Architecture generation uses GPT-4 to create detailed technical design.

Add your key to ~/.env:
  echo 'OPENAI_API_KEY=sk-your-key' >> ~/.env
  chmod 600 ~/.env

Restart Claude Code and try again.
```

### If Generation Fails

```
❌ Architecture generation failed

Error: {{error message}}

This could be due to:
- API rate limits
- Network issues
- PRD format issues

Retry? (yes/no)
```

## Integration with Research

**If user completed research**:
```
I found research findings:
- RESEARCH-data-vendors-findings.md: Recommends {{vendor}}
- RESEARCH-auth-providers-findings.md: Recommends {{provider}}

I'll use these recommendations in the architecture.

Generating architecture with your research...
```

**In generated architecture**:
- Technology Decisions table cites research
- "See RESEARCH-data-vendors-findings.md for vendor analysis"
- Cost estimates use research pricing
- Implementation notes reference research

## Voice Feedback

Voice hooks announce:
- "Generating architecture" (when starting)
- "Architecture complete" (when done)

## Example Usage

**Example 1: After PRD**
```
User: /bmad:prd
[PRD generated]
User: /bmad:architecture

Claude:
- Reads PRD
- Generates architecture with FastAPI, PostgreSQL, Railway
- Shows tech stack
- Asks for approval
- Saves architecture
- "Architecture complete! Next: /bmad:epic 1"
```

**Example 2: With Research**
```
User: /bmad:prd
Claude: "I see you need data vendors. Generate research prompt?"
User: "yes"
[User completes research in ChatGPT]
User: /bmad:architecture

Claude:
- Reads PRD
- Reads RESEARCH-data-vendors-findings.md
- "Based on your research, using Zylalabs API"
- Generates architecture with researched options
- References research in tech decisions
```

**Cost**: ~$0.08 (GPT-4 for architecture generation)

---

**This command creates the complete technical blueprint for implementation!**
