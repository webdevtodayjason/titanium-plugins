# BMAD Document Generation System - Implementation Plan

**Version**: 1.0
**Status**: Planning Phase
**Author**: Jason Brashear, Titanium Computing
**Date**: October 2025

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Document Structure Analysis](#document-structure-analysis)
3. [Folder Structure](#folder-structure)
4. [The Guided Workflow](#the-guided-workflow)
5. [BMAD Slash Commands](#bmad-slash-commands)
6. [Utility Scripts](#utility-scripts)
7. [Implementation Timeline](#implementation-timeline)
8. [Integration with Orchestration](#integration-with-orchestration)
9. [Testing Strategy](#testing-strategy)
10. [Complete User Journey](#complete-user-journey)

---

## Executive Summary

### Vision

Complete the full development lifecycle in Titanium Toolkit:

```
Idea → BMAD Documents → Implementation Plan → Code → Review → Done
```

**Phase 7**: BMAD Document Generation (after Week 4 orchestration release)

### What We're Building

**6 BMAD Document Generation Commands**:
- `/bmad:start` - Guided workflow (creates all documents)
- `/bmad:brief` - Generate project brief
- `/bmad:prd` - Generate PRD
- `/bmad:architecture` - Generate architecture
- `/bmad:epic` - Generate single epic (add new OR regenerate)
- `/bmad:index` - Generate story index summary

**Complete Workflow**:
```bash
# Empty folder → Complete backlog in one session
/bmad:start
# → Creates bmad-backlog/ with brief, PRD, architecture, epics

# Then implement
/titanium:plan bmad-backlog/epics/epic-001.md
/titanium:work
```

---

## Document Structure Analysis

### From AuricBeat Example

**Folder Structure Observed**:
```
bmad/output/
├── prd.md                      # 549 lines, comprehensive
├── architecture.md             # 1,308 lines, extremely detailed
├── data-sources-research.md    # Custom addition
├── epics/                      # 11 epic files
│   ├── EPIC-001-foundation-infrastructure.md (484 lines)
│   ├── EPIC-002-data-ingestion.md
│   ├── EPIC-003-metals-dashboard.md
│   └── ... (11 total)
├── stories/                    # Individual story files
│   └── ...
└── qa/                         # QA assessments
    └── ...
```

### Document Structure Breakdown

#### 1. PRD (Product Requirements Document)

**Header**:
```markdown
# Product Requirements Document (PRD)
## {Project Name} - {Tagline}

**Document Version:** 1.0
**Last Updated:** {Date}
**Product Owner:** {Name}
**Status:** Draft
```

**Sections** (in order):
1. **Executive Summary**
   - Vision (1-2 paragraphs)
   - Mission (1 paragraph)

2. **Product Overview**
   - Target Users (Primary, Secondary, Tertiary)
   - Core Value Propositions (numbered list)
   - Competitive Positioning (vs competitors)

3. **Success Metrics**
   - North Star Metric
   - Key Performance Indicators
     - Product Metrics (Engagement, Feature Adoption)
     - Business Metrics (Growth, Revenue)
     - Domain-specific Metrics (AI Quality, etc.)

4. **Feature Requirements**
   - V1 MVP (12-16 Weeks)
     - Feature 1 (Priority, Requirements, Acceptance Criteria)
     - Feature 2, 3, etc.
   - V2 Pro Features (8-12 Weeks Post-MVP)
     - Feature 1, 2, etc.

5. **User Stories** (organized by Epic)
   - Epic 1: Story bullets
   - Epic 2: Story bullets
   - etc.

6. **Technical Requirements**
   - Performance targets
   - Scalability requirements
   - Security & Compliance
   - Availability SLAs
   - Browser Support

7. **Data Requirements**
   - Data Sources (detailed list)
   - Data Quality standards

8. **AI/ML Requirements** (if applicable)
   - Use Cases with model, input, output, quality
   - Guardrails
   - Evaluation metrics

9. **Design Requirements**
   - Design System (framework, theme)
   - Key Screens (descriptions)

10. **Go-to-Market Strategy**
    - Launch Phases
    - Pricing Strategy
    - Customer Acquisition

11. **Risks & Mitigation** (tables)
    - Technical Risks
    - Business Risks
    - Data/Legal Risks

12. **Open Questions** (numbered list)

13. **Appendix**
    - Glossary
    - References

**Footer**:
```markdown
**Document Status:** ✅ Ready for Technical Review
**Next Steps:** Architecture document, epic breakdown, data source selection
```

---

#### 2. Architecture Document

**Header**:
```markdown
# Architecture Document
## {Project Name} - {Tagline}

**Document Version:** 1.0
**Last Updated:** {Date}
**Architecture Owner:** {Name}
**Status:** Draft
```

**Sections** (in order):
1. **Table of Contents** (auto-generated links)

2. **System Overview**
   - Context (what the system does)
   - Key Requirements (from PRD)

3. **Architecture Principles** (numbered list of guiding principles)

4. **High-Level Architecture** (ASCII diagram of layers)

5. **Component Details**
   - Frontend (Stack, Features, File Structure)
   - Backend (Stack, Service Architecture, Patterns)
   - Data Ingestion (Workflows, DAGs)
   - Real-time Systems (if applicable)

6. **Data Architecture**
   - Database Schema (SQL with CREATE TABLE statements)
   - Time-Series Tables (if applicable)
   - Vector Store (if AI features)

7. **AI/ML Architecture** (if applicable)
   - LLM Infrastructure
   - Model Serving
   - RAG Pipeline
   - Event Extraction

8. **Infrastructure**
   - MVP Deployment (platform and config)
   - Production Deployment (platform and config)
   - Storage Strategy
   - Networking

9. **Security Architecture**
   - Authentication & Authorization (flows, code examples)
   - Rate Limiting (implementation)
   - Data Encryption
   - PII Handling

10. **Deployment Strategy**
    - CI/CD Pipeline (YAML examples)
    - Database Migrations (code examples)
    - Blue-Green / Canary deployment

11. **Monitoring & Observability**
    - Metrics (Prometheus examples)
    - Logging (structured logging examples)
    - Tracing (OpenTelemetry examples)
    - Alerting (rules)

12. **Appendix**
    - Technology Decisions (table with rationale)
    - Performance Benchmarks (targets)
    - Cost Estimates (monthly breakdown)

**Footer**:
```markdown
**Document Status:** ✅ Ready for Implementation
**Next Steps:** Epic breakdown, story writing, data source selection
```

---

#### 3. Epic Document

**Header**:
```markdown
# EPIC-{number}: {Epic Title}

**Epic Owner:** {Team or Person}
**Priority:** P0 (Must Have) | P1 (Should Have) | P2 (Nice to Have)
**Target Sprint:** Sprint {X-Y}
**Status:** 📋 Not Started | 🔄 In Progress | ✅ Complete
**Estimated Effort:** {X} story points
```

**Sections** (in order):
1. **Epic Description** (2-3 paragraphs explaining what and why)

2. **Business Value** (bullet list)

3. **Success Criteria** (checkboxes for epic-level goals)

4. **User Stories** (STORY-{epic}-{number} format)
   - Each story:
     ```markdown
     ### STORY-{epic}-{num}: {Title}
     **As a** {user type}
     **I want** {action}
     **So that** {benefit}

     **Acceptance Criteria:**
     - [ ] Criterion 1
     - [ ] Criterion 2

     **Technical Notes:**
     ```code examples, file structures, implementation hints```
     ```

5. **Dependencies**
   - **Blocks:** What this epic enables
   - **Blocked By:** What must be done first

6. **Risks & Mitigation** (table)

7. **Technical Debt** (checkbox list of known shortcuts)

8. **Related Epics** (links to related work)

9. **Definition of Done** (epic-level checklist)

**Footer**:
```markdown
**Last Updated:** {Date}
**Status History:**
- {Date}: Epic created
- {Date}: Story 1-5 completed
```

---

### Document Cross-References

**How Documents Link**:

1. **PRD** → **Architecture**:
   - PRD footer: "Next Steps: Architecture document"
   - Architecture reads PRD for requirements
   - Architecture translates features into technical design

2. **Architecture** → **Epics**:
   - Architecture footer: "Next Steps: Epic breakdown"
   - Epics reference Architecture in Technical Notes
   - Epics use tech stack from Architecture

3. **Epics** → **Stories** (within epic):
   - Each story references epic context
   - Stories pull technical details from Architecture
   - Stories maintain sequential dependency order

4. **All Documents** → **Implementation**:
   - titanium:plan reads Epic files
   - titanium:work uses Architecture for tech context
   - Agents reference all docs during implementation

---

## Folder Structure

### Option B: BMAD-Style (Chosen)

```
your-project/
├── bmad-backlog/                        # All project documentation
│   ├── product-brief.md                # High-level vision (optional)
│   ├── prd/
│   │   └── prd.md                      # Product Requirements Document
│   ├── architecture/
│   │   └── architecture.md             # Technical Architecture
│   └── epics/
│       ├── EPIC-001-foundation.md
│       ├── EPIC-002-feature-a.md
│       ├── EPIC-003-feature-b.md
│       └── ...
│
├── .titanium/                          # Workflow state (created later)
│   ├── workflow-state.json
│   ├── plan.json
│   └── review-report.md
│
└── src/                                # Source code (created during implementation)
    └── ...
```

**Rationale**:
- Matches BMAD-METHOD structure
- Clear separation of docs vs workflow vs code
- Subdirectories organize by document type
- Easy to navigate
- Familiar to BMAD users

---

## The Guided Workflow

### `/bmad:start` - Complete Guided Workflow

**User Journey**:

```
User: (empty project folder)
/bmad:start

Claude: "Welcome to BMAD document generation! I'll help you create complete project documentation.

What's your project idea at a high level?"

User: "AI-powered todo app with voice input and smart scheduling"

Claude: "Great! Let me create a Product Brief to capture this.

What problem does this solve for users?"

User: "People forget tasks and don't prioritize well"

Claude: "Who are the primary users?"

User: "Busy professionals and students"

[... interactive questions continue ...]

Claude creates:
✅ bmad-backlog/product-brief.md
✅ bmad-backlog/prd/prd.md
✅ bmad-backlog/architecture/architecture.md
✅ bmad-backlog/epics/EPIC-001-foundation.md
✅ bmad-backlog/epics/EPIC-002-core-features.md
✅ bmad-backlog/epics/EPIC-003-ai-features.md

"Complete backlog created! Ready to implement?

Run: /titanium:plan bmad-backlog/epics/EPIC-001-foundation.md"
```

### The Interactive Process

**Phase 1: High-Level Idea (Product Brief)**

Questions:
1. "What's your project idea in one sentence?"
2. "What problem does it solve?"
3. "Who are the target users?"
4. "What makes it different from existing solutions?"
5. "What's the core value proposition?"
6. "What are the must-have features for MVP?"
7. "What's out of scope for MVP?"
8. "Any technical preferences? (Language, framework, hosting)"

**Output**: `bmad-backlog/product-brief.md`

**Phase 2: Product Requirements (PRD)**

Uses brief as input, asks:
1. "Let me review the brief... [shows brief]"
2. "What success metrics matter most?"
3. "What are the functional requirements?" (FR1, FR2, etc.)
4. "What are the non-functional requirements?" (NFR1, NFR2, etc.)
5. "Let me break this into epics... [proposes epic structure]"
6. "For each epic, what are the user stories?"
7. "What are the technical requirements (performance, security)?"
8. "What data sources do you need?"
9. "Any AI/ML requirements?"
10. "Design system preferences?"
11. "Go-to-market approach?"
12. "What risks should we document?"

**Output**: `bmad-backlog/prd/prd.md` (comprehensive PRD)

**Phase 3: Technical Architecture**

Uses PRD as input, asks:
1. "Let me design the architecture based on the PRD..."
2. "I'm proposing [tech stack]. Any objections?"
3. "For data architecture, I suggest [database schema]"
4. "For AI features, I recommend [AI architecture]"
5. "For infrastructure, I suggest [Railway for MVP, GKE for production]"
6. "Here's the security approach: [auth, rate limiting, encryption]"
7. "Deployment strategy: [CI/CD, migrations, blue-green]"
8. "Here's the monitoring plan: [metrics, logging, tracing]"

**Output**: `bmad-backlog/architecture/architecture.md` (1,000+ line architecture)

**Phase 4: Epic Breakdown**

Uses PRD + Architecture, creates each epic:
1. "Epic 1 should be Foundation. It includes: [lists stories]"
2. "Each story has acceptance criteria: [shows criteria]"
3. "Technical notes from architecture: [shows relevant details]"
4. "Dependencies: Epic 1 blocks all others"
5. [Repeats for each epic from PRD]

**Output**: Multiple `bmad-backlog/epics/EPIC-{num}-{name}.md` files

**Phase 5: Review & Finalize**

Shows summary:
```
📚 BMAD Backlog Complete!

Created Documents:
✅ Product Brief (foundation)
✅ PRD (11 sections, 148 user stories across 11 epics)
✅ Architecture (9 sections, complete technical design)
✅ 11 Epic files (148 total stories with acceptance criteria)

📁 Location: bmad-backlog/

Ready to implement?
Run: /titanium:plan bmad-backlog/epics/EPIC-001-foundation.md
```

---

## BMAD Slash Commands

### Command Overview

**6 BMAD Commands**:
1. `/bmad:start` - Complete guided workflow (generates ALL documents)
2. `/bmad:brief` - Product brief generation (standalone)
3. `/bmad:prd` - PRD generation (standalone)
4. `/bmad:architecture` - Architecture generation (standalone)
5. `/bmad:epic` - Single epic generation (add new OR regenerate existing)
6. `/bmad:index` - Regenerate story index summary

**When to Use Each**:

| Command | Use When | Output |
|---------|----------|--------|
| `/bmad:start` | Brand new project, empty folder | Complete backlog (all docs) |
| `/bmad:brief` | Just need high-level vision | product-brief.md |
| `/bmad:prd` | Have brief, need requirements | prd/prd.md |
| `/bmad:architecture` | Have PRD, need technical design | architecture/architecture.md |
| `/bmad:epic` | Add new feature OR regenerate epic | Single EPIC-*.md file |
| `/bmad:index` | Update story summary | STORY-INDEX.md |

---

### 1. `/bmad:start` - Guided Complete Workflow

**File**: `commands/bmad-start.md`

**Purpose**: Complete guided workflow from idea to full backlog

**Process**:
1. Check if project is empty or has existing docs
2. Ask: "Interactive mode or YOLO mode?"
   - Interactive: Ask questions section by section
   - YOLO: Generate drafts for user to refine
3. Create Product Brief (high-level idea capture)
4. Generate PRD from brief (comprehensive requirements)
5. Generate Architecture from PRD (technical design)
6. Generate all Epics from PRD epic list
7. Review and refine as needed
8. Store all documents in Pieces
9. Present summary and next steps

**Key Features**:
- Uses GPT-4 for document generation
- Follows BMAD templates strictly
- Interactive refinement
- Cross-document consistency
- vibe-check validation of structure
- Stores in Pieces for context

---

### 2. `/bmad:brief` - Generate Product Brief

**File**: `commands/bmad-brief.md`

**Purpose**: Create high-level product brief from idea

**Input**: User's project idea (one sentence to paragraph)

**Output**: `bmad-backlog/product-brief.md`

**Sections**:
- Executive Summary (concept, problem, market, value prop)
- Problem Statement (pain points, impact, why now)
- Proposed Solution (approach, differentiators, vision)
- Target Users (primary, secondary segments)
- Goals & Success Metrics (business, user, KPIs)
- MVP Scope (core features, out of scope, success criteria)
- Post-MVP Vision (phase 2, long-term, expansion)
- Technical Considerations (platforms, tech preferences, architecture)
- Constraints & Assumptions (budget, timeline, resources, technical)
- Risks & Open Questions
- Appendices (research, stakeholder input, references)
- Next Steps (handoff to PRD generation)

**Process**:
1. Ask high-level questions
2. Generate brief with GPT-4
3. Show to user for refinement
4. Save to bmad-backlog/product-brief.md
5. Store in Pieces
6. Suggest next command: `/bmad:prd`

---

### 3. `/bmad:prd` - Generate PRD

**File**: `commands/bmad-prd.md`

**Purpose**: Create comprehensive Product Requirements Document

**Input**:
- Reads `bmad-backlog/product-brief.md` (if exists)
- Or user provides requirements inline

**Output**: `bmad-backlog/prd/prd.md`

**Sections** (matching AuricBeat structure):
1. Header (Version, Date, Owner, Status)
2. Executive Summary (Vision, Mission)
3. Product Overview (Users, Value Props, Competitive Position)
4. Success Metrics (North Star, KPIs)
5. Feature Requirements (V1 MVP, V2 Features with Acceptance Criteria)
6. User Stories (organized by Epic)
7. Technical Requirements (Performance, Scalability, Security, Availability, Browser)
8. Data Requirements (Sources, Quality)
9. AI/ML Requirements (if applicable - Use Cases, Guardrails, Evaluation)
10. Design Requirements (Design System, Key Screens)
11. Go-to-Market Strategy (Phases, Pricing, Acquisition)
12. Risks & Mitigation (Technical, Business, Legal tables)
13. Open Questions (numbered)
14. Appendix (Glossary, References)
15. Footer (Status, Next Steps)

**Process**:
1. Check for product-brief.md, read if exists
2. Ask for requirements (or use brief)
3. Interactive section-by-section generation
4. User reviews and refines each section
5. Use GPT-4 to generate comprehensive content
6. Ensure Epic List section is well-structured (for epic generation)
7. Save to bmad-backlog/prd/prd.md
8. Validate with vibe-check
9. Store in Pieces
10. Suggest: `/bmad:architecture`

---

### 4. `/bmad:architecture` - Generate Architecture

**File**: `commands/bmad-architecture.md`

**Purpose**: Create comprehensive technical architecture document

**Input**:
- Reads `bmad-backlog/prd/prd.md` (required)
- Uses technical requirements from PRD

**Output**: `bmad-backlog/architecture/architecture.md`

**Sections** (matching AuricBeat structure):
1. Header (Version, Date, Owner, Status)
2. Table of Contents (auto-generated)
3. System Overview (Context from PRD, Key Requirements)
4. Architecture Principles (6-10 guiding principles)
5. High-Level Architecture (ASCII diagram of all layers)
6. Component Details
   - Frontend (Framework, Stack, Features, File Structure)
   - Backend (Framework, Stack, Service Architecture, Code Examples)
   - Data Ingestion (if needed - Workflows, Prefect/Airflow DAGs)
   - Real-time (if needed - WebSocket, Kafka, Stream Processing)
7. Data Architecture
   - Database Schema (SQL CREATE TABLE statements for all tables)
   - Time-Series Tables (if applicable - TimescaleDB)
   - Vector Store (if AI - pgvector, indexes)
8. AI/ML Architecture (if PRD has AI requirements)
   - LLM Infrastructure (vLLM, Model Gateway)
   - RAG Pipeline (LlamaIndex, retrieval)
   - NER/Event Extraction
   - Sentiment Analysis
9. Infrastructure
   - MVP Deployment (Railway/Vercel/etc. with config)
   - Production Deployment (GKE/ECS/etc. with config)
   - Storage (databases, object storage, caching)
   - Networking (CDN, load balancer, service mesh)
10. Security Architecture
    - Authentication & Authorization (flows, JWT, middleware code)
    - Rate Limiting (tier-based, Redis implementation)
    - Data Encryption (at rest, in transit)
    - PII Handling (retention, compliance)
11. Deployment Strategy
    - CI/CD Pipeline (GitHub Actions YAML)
    - Database Migrations (Alembic/Flyway examples)
    - Blue-Green Deployment (diagram, steps)
12. Monitoring & Observability
    - Metrics (Prometheus metrics, code examples)
    - Logging (Structured logging, examples)
    - Tracing (OpenTelemetry spans, examples)
    - Alerting (Critical alerts, warning thresholds)
13. Appendix
    - Technology Decisions Table (with alternatives and rationale)
    - Performance Benchmarks (targets and how to measure)
    - Cost Estimates (MVP and Production monthly costs)
14. Footer (Status, Next Steps: Epic breakdown)

**Process**:
1. Read PRD thoroughly
2. Extract technical requirements
3. Generate architecture section by section with GPT-4
4. Include detailed code examples (SQL, Python, TypeScript)
5. Create ASCII diagrams for system architecture
6. Ensure architecture references PRD requirements
7. Save to bmad-backlog/architecture/architecture.md
8. Validate structure with vibe-check
9. Store in Pieces
10. Suggest: `/bmad:epic` for each epic

---

### 5. `/bmad:epic` - Generate Single Epic

**File**: `commands/bmad-epic.md`

**Purpose**: Create or regenerate a single epic with user stories

**When to Use**:
- **Add NEW epic** to existing backlog (change request, new feature 6 months later)
- **Regenerate epic** for refinement
- **Incremental backlog building** (advanced users, not using `/bmad:start`)

**NOT used during `/bmad:start`** - guided workflow generates all epics automatically

**Input**:
- Reads `bmad-backlog/prd/prd.md` (required)
- Reads `bmad-backlog/architecture/architecture.md` (recommended)
- Epic name or number

**Output**: `bmad-backlog/epics/EPIC-{num}-{slug}.md`

**Example Usage**:
```bash
# 6 months after launch, need mobile app
/bmad:epic "Mobile App"
# → Creates EPIC-012-mobile-app.md
# → Integrates with existing backlog

# Or regenerate existing epic
/bmad:epic 3
# → Regenerates EPIC-003 with refinements
```

**Process**:
1. Read PRD to find epic definition
2. Read Architecture for technical context
3. Ask: "Which epic do you want to detail? (or I can do all sequentially)"
4. For the epic:
   - Extract epic description from PRD
   - Break into user stories (STORY-{epic}-{num})
   - For each story:
     - Write "As a X I want Y so that Z"
     - Generate acceptance criteria (checkboxes)
     - Add technical notes from Architecture
   - Add dependencies (what blocks, what's blocked by)
   - Add risks & mitigation
   - Add related epics
5. Save to bmad-backlog/epics/EPIC-{num}-{name}.md
6. Store in Pieces
7. If more epics: "Epic {N} complete. Generate next epic?"

**Generates All Stories**:
- STORY-{epic}-01, STORY-{epic}-02, etc.
- Each with acceptance criteria
- Technical notes pulled from architecture
- Sequential dependencies noted

---

### 6. `/bmad:index` - Generate Story Index

**File**: `commands/bmad-index.md`

**Purpose**: Generate or regenerate story index summary table

**When to Use**:
- After `/bmad:start` completes (auto-generated)
- After adding new epics with `/bmad:epic`
- After manually editing epic files
- Want refreshed story count and totals

**Input**:
- Scans all files in `bmad-backlog/epics/`
- Reads each epic file to extract stories

**Output**: `bmad-backlog/STORY-INDEX.md`

**Process**:
1. Scan `bmad-backlog/epics/` for all EPIC-*.md files
2. For each epic:
   - Extract epic number, name, priority
   - Parse all STORY sections
   - Extract: Story ID, Title, Priority, Story Points (if present)
   - Count total stories in epic
3. Calculate totals:
   - Total epics
   - Total stories across all epics
   - Total story points
   - Priority distribution
4. Generate summary tables:
   - Epic overview table
   - Per-epic story tables
5. Save to `bmad-backlog/STORY-INDEX.md`
6. Display summary to user

**Example Output**:
```
📊 Story Index Generated

Total: 5 epics, 45 stories, 180 story points

Epic Distribution:
- Epic 1: 10 stories (45 points)
- Epic 2: 12 stories (52 points)
- Epic 3: 8 stories (35 points)
- Epic 4: 9 stories (28 points)
- Epic 5: 6 stories (20 points)

Priority Breakdown:
- P0 (Must Have): 32 stories (70%)
- P1 (Should Have): 10 stories (22%)
- P2 (Nice to Have): 3 stories (7%)

Saved to: bmad-backlog/STORY-INDEX.md
```

**Commands**:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py index "bmad-backlog/epics/" "$(pwd)"
```

---

## Utility Scripts

### 1. `bmad_generator.py` - Document Generator

**Location**: `hooks/utils/bmad/bmad_generator.py`

**Purpose**: Use GPT-4 to generate BMAD documents following strict templates

**Functions**:

```python
def generate_brief(idea: str, project_path: str) -> str:
    """Generate product brief from idea"""
    prompt = f"""Generate a Product Brief following BMAD format.

User's idea: {idea}

Create a comprehensive brief with:
1. Executive Summary (vision, mission)
2. Problem Statement (pain points, impact)
3. Proposed Solution (approach, differentiators)
4. Target Users (primary, secondary)
5. Goals & Success Metrics
6. MVP Scope (core features, out of scope)
7. Post-MVP Vision
8. Technical Considerations
9. Constraints & Assumptions
10. Risks & Open Questions

Format as markdown with proper headers and sections.
Use BMAD template structure strictly."""

    # Call GPT-4
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.4
    )

    return response.choices[0].message.content

def generate_prd(brief_path: str, project_path: str) -> str:
    """Generate PRD from product brief"""
    # Read brief
    with open(brief_path) as f:
        brief = f.read()

    prompt = f"""Generate a comprehensive PRD following BMAD format.

Product Brief:
{brief}

Create PRD with these sections (matching BMAD template exactly):
[... list all 15 sections ...]

Include:
- Detailed feature requirements with acceptance criteria
- User stories organized by epic
- Complete technical requirements
- Data and AI/ML requirements if applicable
- Design requirements
- Go-to-market strategy
- Risk tables
- Open questions
- Glossary

Format strictly as BMAD PRD template."""

    # Call GPT-4 with larger context
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.3
    )

    return response.choices[0].message.content

def generate_architecture(prd_path: str, project_path: str) -> str:
    """Generate architecture from PRD"""
    # Similar to generate_prd but for architecture
    pass

def generate_epic(prd_path: str, arch_path: str, epic_number: int, project_path: str) -> str:
    """Generate single epic with stories"""
    # Read PRD and Architecture
    # Extract epic definition from PRD
    # Pull technical context from Architecture
    # Generate stories with acceptance criteria
    # Add technical notes
    pass

def generate_story_index(epics_dir: str, project_path: str) -> str:
    """Generate STORY-INDEX.md from all epic files"""
    # Scan epics/ directory
    # Parse each EPIC-*.md file
    # Extract: Epic number, name, all stories
    # Count story points
    # Create summary tables
    # Calculate distributions
    pass
```

**Dependencies**:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "openai",
# ]
# ///
```

---

### 2. `bmad_validator.py` - Document Validator

**Location**: `hooks/utils/bmad/bmad_validator.py`

**Purpose**: Validate generated documents match BMAD structure

**Functions**:

```python
def validate_prd(prd_content: str) -> dict:
    """Validate PRD has all required sections"""
    required_sections = [
        "Executive Summary",
        "Product Overview",
        "Success Metrics",
        "Feature Requirements",
        "User Stories",
        "Technical Requirements",
        "Data Requirements",
        "Design Requirements",
        "Go-to-Market Strategy",
        "Risks & Mitigation",
        "Open Questions",
        "Appendix"
    ]

    results = {
        "valid": True,
        "missing_sections": [],
        "warnings": []
    }

    for section in required_sections:
        if section not in prd_content:
            results["valid"] = False
            results["missing_sections"].append(section)

    return results

def validate_epic(epic_content: str, epic_number: int) -> dict:
    """Validate epic structure"""
    # Check for required fields
    # Verify story format
    # Check acceptance criteria
    pass

def validate_architecture(arch_content: str) -> dict:
    """Validate architecture completeness"""
    # Check for all required sections
    # Verify code examples present
    # Check for cost estimates
    pass
```

---

## Cost Analysis (Corrected)

### Token Usage Estimates

**Product Brief**:
- Input: ~1,500 tokens (prompt + idea)
- Output: ~700 tokens
- Total: 2,200 tokens
- **Cost**: ~$0.02

**PRD**:
- Input: ~3,000 tokens (prompt + brief)
- Output: ~2,500 tokens
- Total: 5,500 tokens
- **Cost**: ~$0.06

**Architecture**:
- Input: ~4,000 tokens (prompt + PRD)
- Output: ~3,500 tokens
- Total: 7,500 tokens
- **Cost**: ~$0.08

**Epic** (per epic):
- Input: ~2,500 tokens (prompt + PRD + Architecture)
- Output: ~1,500 tokens
- Total: 4,000 tokens
- **Cost per epic**: ~$0.01

**All Epics** (5 epics typical):
- Total: 20,000 tokens
- **Cost**: ~$0.05

**Story Index**:
- Input: ~1,000 tokens (all epic files)
- Output: ~500 tokens
- Total: 1,500 tokens
- **Cost**: ~$0.01

### GPT-4o Pricing

- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens

### Complete Backlog Cost

**`/bmad:start` (all documents)**:
- Total tokens: ~36,700 tokens
- Total cost: **~$0.22**
- **Range: $0.20-0.25** depending on complexity

### Individual Command Costs

| Command | Cost |
|---------|------|
| `/bmad:brief` | ~$0.02 |
| `/bmad:prd` | ~$0.06 |
| `/bmad:architecture` | ~$0.08 |
| `/bmad:epic` (single) | ~$0.01 |
| `/bmad:index` | ~$0.01 |
| **Complete backlog** | **~$0.22** |

**Very affordable!** Less than a cup of coffee for complete project documentation.

---

## Implementation Timeline

### Phase 7 (After Week 4): BMAD Document Generation

**Duration**: 3-4 weeks

#### Week 1: Core Generation System

**Day 1-2**: Utility Scripts
- [ ] Create `hooks/utils/bmad/` directory
- [ ] Write `bmad_generator.py` with GPT-4 integration
- [ ] Write `bmad_validator.py` for structure validation
- [ ] Test document generation standalone

**Day 3-4**: Product Brief Command
- [ ] Create `/bmad:brief` command
- [ ] Test brief generation
- [ ] Validate output matches BMAD format
- [ ] Add vibe-check validation

**Day 5**: PRD Foundation
- [ ] Create `/bmad:prd` command (basic)
- [ ] Test PRD generation from brief
- [ ] Validate section structure

#### Week 2: PRD & Architecture

**Day 1-3**: Complete PRD Command
- [ ] Add all 15 PRD sections
- [ ] Interactive section refinement
- [ ] Epic list generation
- [ ] User story generation
- [ ] Test with various project types

**Day 4-5**: Architecture Command
- [ ] Create `/bmad:architecture` command
- [ ] Generate from PRD
- [ ] Include code examples (SQL, Python, etc.)
- [ ] ASCII diagram generation
- [ ] Test architecture quality

#### Week 3: Epic Generation

**Day 1-2**: Epic Command
- [ ] Create `/bmad:epic` command
- [ ] Read PRD and Architecture
- [ ] Generate stories with acceptance criteria
- [ ] Add technical notes from architecture
- [ ] Test with multiple epics

**Day 3-4**: Guided Workflow
- [ ] Create `/bmad:start` command
- [ ] Implement complete guided flow
- [ ] Interactive question/answer system
- [ ] Sequential document generation
- [ ] Test end-to-end workflow

**Day 5**: Integration
- [ ] Link to titanium:plan
- [ ] Test complete cycle: /bmad:start → /titanium:plan → /titanium:work
- [ ] Validate document references work

#### Week 4: Polish & Release

**Day 1-2**: Testing
- [ ] Test with 5 different project types
- [ ] Validate all documents match BMAD format
- [ ] Check cross-references work
- [ ] Test titanium:plan can read epics

**Day 3**: Documentation
- [ ] Write BMAD commands guide
- [ ] Update README with BMAD section
- [ ] Create examples

**Day 4-5**: Release
- [ ] Update plugin version to 2.1.0
- [ ] Create PR
- [ ] Release BMAD generation system

---

## BMAD Command Specifications

### Command: `/bmad:start`

**Full Interactive Workflow**:

```markdown
---
description: Guided workflow to create complete BMAD backlog from idea
---

# BMAD Start - Complete Guided Workflow

You are guiding the user through complete BMAD backlog creation.

## Step 1: Introduction

Present:
```
🚀 BMAD Document Generation

I'll help you create complete project documentation following the BMAD methodology.

This process will create:
- Product Brief (high-level vision)
- PRD (comprehensive requirements)
- Architecture (technical design)
- Epic breakdowns (all features organized)

This takes about 30-45 minutes for a typical project.

Ready to start?
```

## Step 2: Check for Existing Documentation

```bash
ls -la bmad-backlog/ 2>/dev/null || echo "No backlog found"
```

**If documentation exists**:
Ask: "I found existing BMAD documentation. Would you like to:
1. Start fresh (overwrites existing)
2. Add to existing (create new epics)
3. Refine existing (regenerate specific documents)
4. Cancel"

**If no documentation**:
Continue to Step 3

## Step 3: Choose Mode

Ask user:
```
Choose your mode:

1. **Interactive** - I'll ask questions section by section (recommended)
2. **YOLO** - I'll generate complete drafts based on your idea (faster, requires refinement)

Which mode?
```

Store user's choice.

## Step 4: Capture High-Level Idea

Ask:
```
What's your project idea?

Describe it at a high level:
- What is it?
- Who is it for?
- What problem does it solve?

Be as detailed or brief as you like - I'll ask follow-up questions.
```

Store user's response.

## Step 5: Generate Product Brief

Call utility script:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py brief "{{user_idea}}" "$(pwd)"
```

This creates `bmad-backlog/product-brief.md`

Show user:
```
✅ Product Brief Created

Let me show you what I generated:
[Display key sections]

Would you like to:
1. Approve and continue
2. Refine specific sections
3. Start over
```

**If refinements needed**:
- Make changes interactively
- Regenerate sections

**When approved**:
- Save final brief
- Store in Pieces
- Continue to Step 6

## Step 6: Generate PRD

Call utility script:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py prd "bmad-backlog/product-brief.md" "$(pwd)"
```

For Interactive Mode:
- Generate section by section
- Show each section to user
- Ask for refinements
- Build complete PRD

For YOLO Mode:
- Generate complete PRD
- Show to user
- Refine as needed

**Key Sections to Focus On**:
1. Feature Requirements (with acceptance criteria)
2. Epic List (foundation for epic generation)
3. User Stories (organized by epic)
4. Technical Requirements (guides architecture)

Save to `bmad-backlog/prd/prd.md`

Validate with vibe-check:
```
mcp__vibe-check__vibe_check(
  goal: "Create comprehensive PRD",
  plan: "Generated PRD with [X] epics, [Y] features",
  uncertainties: ["Is epic structure logical?", "Are requirements complete?"]
)
```

## Step 7: Generate Architecture

Call utility script:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py architecture "bmad-backlog/prd/prd.md" "$(pwd)"
```

Generate:
- System overview from PRD requirements
- Tech stack recommendations (based on PRD technical preferences)
- Component architecture
- Data architecture (SQL schemas for all entities)
- AI/ML architecture (if PRD has AI requirements)
- Infrastructure design
- Security architecture
- Deployment strategy
- Monitoring plan

Show user tech stack recommendations:
```
Based on your PRD, I recommend:

Frontend: Next.js 14 + TypeScript + Tailwind + shadcn/ui
Backend: FastAPI + Python 3.11 + SQLAlchemy
Database: PostgreSQL 17 + TimescaleDB + pgvector
Cache: Redis
Hosting: Railway (MVP) → GKE (Production)

Approve this stack, or specify alternatives?
```

After user approval, generate complete architecture.

Save to `bmad-backlog/architecture/architecture.md`

## Step 8: Generate All Epics

Read epic list from PRD.

For each epic:
```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py epic "bmad-backlog/prd/prd.md" "bmad-backlog/architecture/architecture.md" {epic_number} "$(pwd)"
```

Generate:
- Epic description
- Business value
- Success criteria
- User stories (STORY-{epic}-{num} format)
  - Each with acceptance criteria
  - Each with technical notes from architecture
- Dependencies
- Risks
- Definition of done

Save each to `bmad-backlog/epics/EPIC-{num}-{slug}.md`

Show progress:
```
Generating epics...
✅ Epic 1: Foundation - 8 stories
✅ Epic 2: Core Features - 12 stories
✅ Epic 3: Advanced Features - 10 stories
[... etc ...]
```

## Step 8.5: Generate Story Index

After all epics are created, generate summary index:

```bash
uv run {{PLUGIN_DIR}}/hooks/utils/bmad/bmad_generator.py index "bmad-backlog/epics/" "$(pwd)"
```

This creates `bmad-backlog/STORY-INDEX.md` with:
- Total epics, stories, story points
- Epic overview table
- Per-epic story tables with IDs, titles, priorities, points, status
- Priority distribution
- Development phase breakdown

**Why**: Provides quick overview of entire backlog, useful for sprint planning

## Step 9: Store in Pieces

Create comprehensive Pieces memory:
```
mcp__Pieces__create_pieces_memory(
  summary_description: "Complete BMAD backlog for {project_name}",
  summary: "Generated complete project backlog with Product Brief, PRD ({X} sections, {Y} features), Architecture ({Z} sections), and {N} Epics with {M} total user stories.

Key features:
[List main features from PRD]

Tech stack:
[Stack from architecture]

Epics:
[List all epics]

Ready for implementation with /titanium:plan",
  files: [
    "bmad-backlog/product-brief.md",
    "bmad-backlog/prd/prd.md",
    "bmad-backlog/architecture/architecture.md",
    "bmad-backlog/epics/*.md"
  ],
  project: "$(pwd)"
)
```

## Step 10: Present Summary

```
📚 BMAD Backlog Generation Complete!

🎯 Project: {project_name}

📄 Documents Created:
✅ Product Brief (vision and goals)
✅ PRD (comprehensive requirements)
   - {X} epics
   - {Y} features
   - {Z} user stories
✅ Architecture (technical design)
   - Complete tech stack
   - Database schemas
   - Infrastructure plan
   - Security architecture
✅ {N} Epic Files
   - {M} total user stories
   - All with acceptance criteria
   - Technical notes included

📁 Location: bmad-backlog/

💾 All documents stored in Pieces for future reference

---

Ready to implement?

Option 1: Review the backlog first
- Read bmad-backlog/prd/prd.md
- Review bmad-backlog/architecture/architecture.md
- Check bmad-backlog/epics/*.md

Option 2: Start implementing immediately
- Run: /titanium:plan bmad-backlog/epics/EPIC-001-*.md
- Then: /titanium:work

What would you like to do?
```

## Important Guidelines

ALWAYS:
- ✅ Follow BMAD templates strictly
- ✅ Generate comprehensive content (not minimal)
- ✅ Include code examples in Architecture
- ✅ Include SQL schemas in Architecture
- ✅ Use proper epic/story numbering (EPIC-001, STORY-001-01)
- ✅ Add acceptance criteria to all stories
- ✅ Reference PRD and Architecture in epics
- ✅ Validate structure with vibe-check
- ✅ Store all documents in Pieces

NEVER:
- ❌ Generate minimal/incomplete documents
- ❌ Skip sections from BMAD templates
- ❌ Forget acceptance criteria
- ❌ Miss technical notes in stories
- ❌ Skip cross-references between documents
```

---

## Integration with Orchestration System

### Complete Development Cycle

```
Empty Folder
    ↓
/bmad:start (30-45 min)
    ↓
bmad-backlog/ created (Brief, PRD, Architecture, Epics)
    ↓
/titanium:plan bmad-backlog/epics/EPIC-001-foundation.md (2 min)
    ↓
.titanium/plan.json created
    ↓
/titanium:work (2-6 hours per epic)
    ↓
Epic 1 implemented and tested
    ↓
/titanium:review
    ↓
Quality validated
    ↓
Repeat for Epic 2, 3, etc.
    ↓
Complete Project Done!
```

### Document Flow

```
Idea
  ↓
Product Brief (high-level)
  ↓
PRD (requirements + epic list)
  ↓ ←─────────┐
Architecture (technical design)
  ↓           │
Epic Files (stories + acceptance criteria + technical notes from architecture)
  ↓
titanium:plan (implementation plan)
  ↓
titanium:work (code implementation)
```

---

## File Structure After BMAD Generation

```
your-project/
├── bmad-backlog/                               # BMAD documentation
│   ├── product-brief.md                       # Optional, high-level vision
│   ├── prd/
│   │   └── prd.md                             # Complete PRD (500-1000 lines)
│   ├── architecture/
│   │   └── architecture.md                    # Technical architecture (1000-1500 lines)
│   ├── epics/
│   │   ├── EPIC-001-foundation.md             # 300-500 lines each
│   │   ├── EPIC-002-core-features.md
│   │   ├── EPIC-003-advanced-features.md
│   │   └── ...
│   └── STORY-INDEX.md                         # Auto-generated summary table
│
├── .titanium/                                  # Created later by titanium:plan
│   └── plan.json
│
└── src/                                        # Created later by titanium:work
    └── ...
```

**STORY-INDEX.md Contents**:
```markdown
# {Project} - Story Index

**Total Epics:** 5
**Total User Stories:** 45
**Total Story Points:** 180

## Epic Overview

| Epic ID | Epic Name | Stories | Story Points | Status |
|---------|-----------|---------|--------------|--------|
| EPIC-001 | Foundation | 10 | 45 | Not Started |
| EPIC-002 | Core Features | 12 | 52 | Not Started |
...

## EPIC-001: Foundation
| Story ID | Title | Priority | Points | Status |
|----------|-------|----------|--------|--------|
| US-001-001 | Setup database | P0 | 5 | Not Started |
...
```

---

## Testing Strategy

### Document Quality Tests

**Test 1: Brief Generation**
```bash
/bmad:brief "Social network for developers with code-based profiles"
# Verify: bmad-backlog/product-brief.md created
# Check: All required sections present
# Validate: Clear problem statement and MVP scope
```

**Test 2: PRD Generation**
```bash
/bmad:prd
# Reads brief
# Generates comprehensive PRD
# Verify: Epic list logical and sequential
# Check: User stories organized by epic
# Validate: Technical requirements complete
```

**Test 3: Architecture Generation**
```bash
/bmad:architecture
# Reads PRD
# Generates architecture
# Verify: SQL schemas for all entities
# Check: Code examples in all relevant sections
# Validate: Cost estimates present
```

**Test 4: Epic Generation**
```bash
/bmad:epic 1
# Generates EPIC-001
# Verify: Stories have acceptance criteria
# Check: Technical notes reference architecture
# Validate: Dependencies documented
```

**Test 5: Complete Workflow**
```bash
/bmad:start
# Full guided workflow
# Verify: All documents created
# Check: Cross-references work
# Validate: Can run titanium:plan on epic files
```

### Integration Tests

**Test: BMAD → Titanium Integration**
```bash
# 1. Generate BMAD backlog
/bmad:start "AI todo app"

# 2. Create implementation plan
/titanium:plan bmad-backlog/epics/EPIC-001-foundation.md

# 3. Verify plan quality
# Check: Tasks make sense
# Check: Agents assigned correctly
# Check: References architecture correctly

# 4. Execute workflow
/titanium:work

# 5. Verify implementation
# Check: Code matches architecture
# Check: All acceptance criteria met
```

---

## Complete User Journey

### Scenario: Brand New Project

**User**: Developer with idea, empty folder

**Journey**:

```bash
# Day 1: Documentation
mkdir my-ai-app
cd my-ai-app
git init

/bmad:start

Claude: "Welcome! What's your project idea?"
User: "AI-powered todo app with voice input and smart scheduling"

Claude: "Great! Let me ask some questions..."
[15-20 interactive questions]

Claude: "Creating your backlog..."
# 30-45 minutes later

Claude: "Complete! Created:
- Product Brief
- PRD with 4 epics, 35 user stories
- Architecture with complete tech stack
- 4 Epic files with stories and acceptance criteria

Ready to implement?"

User: "Yes, start with Epic 1"

# Day 1-2: Implementation
/titanium:plan bmad-backlog/epics/EPIC-001-foundation.md

Claude: "Plan created: 8 stories, 3 hours estimated"

/titanium:work

Claude: "Implementing Epic 1..."
[3 hours of orchestrated work]
Claude: "Epic 1 complete! All tests passing."

/titanium:review
Claude: "Review complete: No critical issues"

# Day 3-4: Epic 2
/titanium:plan bmad-backlog/epics/EPIC-002-core-features.md
/titanium:work
# [4 hours]

# Day 5-6: Epic 3
/titanium:plan bmad-backlog/epics/EPIC-003-ai-features.md
/titanium:work
# [6 hours]

# Day 7: Epic 4
/titanium:plan bmad-backlog/epics/EPIC-004-polish.md
/titanium:work
# [2 hours]

# Done! Complete project in 1 week.
```

**Timeline**:
- Documentation: 45 minutes (BMAD generation)
- Implementation: 15 hours (4 epics × ~4 hours avg)
- Total: ~1 week for complete MVP

**Cost**:
- BMAD generation: ~$0.15 (GPT-4 for all documents)
- Implementation: ~$0.40 (4 workflows × $0.10)
- **Total: ~$0.55** for complete project

---

## What's NOT Included (Initially)

### Individual .story.md Files

**Found in**: AuricBeat has `stories/` folder
**Why not included**:
- Stories are already in epic files (STORY-001-01, STORY-001-02, etc.)
- Individual story files are BMAD-METHOD's dev workflow artifacts
- Used during implementation (SM agent creates them)
- Not needed for initial backlog generation
- **May add in future** if users want granular story management

### QA Folder

**Found in**: AuricBeat has `qa/` folder with assessments
**Why not included**:
- BMAD-METHOD QA agent specific
- We handle quality with `/titanium:review` instead
- Not part of core BMAD documentation
- **May add in future** if demand exists

### Custom Research Documents

**Found in**: AuricBeat has `data-sources-research.md`
**Why not included**:
- Project-specific, not template-driven
- User creates these manually if needed
- Can't be auto-generated from templates
- Not part of standard BMAD methodology

### README.md in stories/

**Found in**: Explains story format
**Why included**: Actually **YES** - we'll generate this in `/bmad:index`
- Explains story ID format
- Documents story point scale
- Useful reference for developers

---

## Key Design Decisions

### 1. Strict BMAD Format Adherence

**Why**: Documents are for AI consumption. Strict structure = better parsing.

**How**:
- Use exact section headers from BMAD templates
- Include all required fields
- Follow numbering conventions (EPIC-001, STORY-001-01)
- Maintain cross-references

### 2. Guided Interactive Workflow

**Why**: Better quality, user understands the backlog

**How**:
- `/bmad:start` asks questions step by step
- Shows generated content for approval
- Allows refinement before moving on
- Takes 30-45 minutes but produces quality docs

**Alternative**: YOLO mode for speed (generate drafts, refine later)

### 3. GPT-4 for Generation

**Why**: Needs understanding of BMAD structure and quality content

**Model**: `gpt-4o`
**Temperature**: 0.3-0.4 (balanced creativity and consistency)
**Max Tokens**: 3000-4000 per document section

### 4. Folder Structure: bmad-backlog/

**Why**: Matches BMAD methodology, organized, clear

**Structure**:
```
bmad-backlog/
├── product-brief.md (optional but recommended)
├── prd/
│   └── prd.md
├── architecture/
│   └── architecture.md
└── epics/
    └── EPIC-*.md
```

### 5. Cross-Document References

**PRD → Architecture**:
- PRD defines requirements
- Architecture implements requirements
- Architecture cites PRD sections

**Architecture → Epics**:
- Epics reference architecture tech stack
- Technical Notes quote architecture code examples
- Dependencies noted

---

## Example Prompts to GPT-4

### Generate Product Brief

```python
prompt = f"""Generate a Product Brief following BMAD methodology.

User's idea: {user_idea}

Create a comprehensive brief with these sections:

## Executive Summary
- Product concept (1-2 sentences)
- Problem being solved
- Target market
- Key value proposition

## Problem Statement
- Current pain points (detailed)
- Impact of problem (quantify if possible)
- Why existing solutions fail
- Urgency

## Proposed Solution
- Core approach
- Key differentiators
- Why this will succeed
- Product vision

## Target Users
- Primary segment (profile, needs, goals)
- Secondary segment (if applicable)

## Goals & Success Metrics
- Business objectives (SMART goals)
- User success metrics
- KPIs with targets

## MVP Scope
- Core features (must-have) with rationale
- Out of scope for MVP
- MVP success criteria

## Post-MVP Vision
- Phase 2 features
- Long-term vision (1-2 years)
- Expansion opportunities

## Technical Considerations
- Platform requirements
- Technology preferences (Frontend, Backend, Database, Hosting)
- Architecture considerations

## Constraints & Assumptions
- Budget, Timeline, Resources
- Technical constraints
- Key assumptions

## Risks & Open Questions
- Key risks (with impact)
- Open questions needing answers
- Areas for further research

## Next Steps
- Immediate actions
- Handoff to PRD generation

Format as markdown with proper headers. Be comprehensive but concise.
Use the BMAD template structure exactly."""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=3000,
    temperature=0.4
)

return response.choices[0].message.content
```

### Generate PRD

```python
prompt = f"""Generate a comprehensive Product Requirements Document (PRD) following BMAD methodology.

Product Brief:
{brief_content}

Create PRD with these exact sections (match BMAD template):

# Product Requirements Document (PRD)
## {project_name}

**Document Version:** 1.0
**Last Updated:** {current_date}
**Product Owner:** TBD
**Status:** Draft

---

## Executive Summary
- Vision (1-2 paragraphs)
- Mission (1 paragraph)

## Product Overview
- Target Users (Primary, Secondary, Tertiary with profiles)
- Core Value Propositions (numbered list, 3-5 items)
- Competitive Positioning (vs 2-3 competitors)

## Success Metrics
- North Star Metric (one primary metric)
- Key Performance Indicators
  - Product Metrics (Engagement, Feature Adoption)
  - Business Metrics (Growth, Revenue)
  - Domain-specific Metrics (if applicable)

## Feature Requirements

### V1 MVP (12-16 Weeks)
For each major feature:
#### {N}. {Feature Name}
**Priority:** P0 (Must Have) | P1 (Should Have) | P2 (Nice to Have)

**Requirements:**
- [Detailed requirements]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

### V2 Pro Features (8-12 Weeks Post-MVP)
- List post-MVP features with priorities

## User Stories
Organize by Epic:
### Epic 1: {Epic Name}
- As a {user}, I want {action} so that {benefit}
- [More stories...]

### Epic 2: {Epic Name}
- [Stories...]

[Continue for all epics - aim for 3-6 epics total]

## Technical Requirements
- Performance (specific targets with p95)
- Scalability (concurrent users, throughput)
- Security & Compliance (standards, encryption)
- Availability (uptime SLAs)
- Browser Support (specific versions)

## Data Requirements
- Data Sources (detailed list with providers)
- Data Quality (freshness, accuracy standards)

## AI/ML Requirements (if applicable)
For each AI use case:
- Model recommendation
- Input/output specification
- Latency requirements
- Quality metrics
- Guardrails (source attribution, confidence thresholds)
- Evaluation approach

## Design Requirements
- Design System (framework, theme, accessibility)
- Key Screens (list and brief descriptions)

## Go-to-Market Strategy
- Launch Phases (with timelines)
- Pricing Strategy (tiers and pricing)
- Customer Acquisition (channels)

## Risks & Mitigation
Create tables for:
- Technical Risks
- Business Risks
- Data/Legal Risks

Each with: Risk | Impact | Likelihood | Mitigation

## Open Questions
Numbered list of unresolved questions

## Appendix
- Glossary (domain-specific terms)
- References (links, sources)

---

**Document Status:** ✅ Ready for Technical Review
**Next Steps:** Architecture document, epic breakdown

Generate comprehensive, detailed content. This PRD should be 500-1000 lines.
Be specific with acceptance criteria. Make epics logical and sequential.
Epic 1 must be Foundation/Infrastructure."""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=4000,
    temperature=0.3
)

return response.choices[0].message.content
```

---

## Implementation Checklist

### Utility Scripts

- [ ] `hooks/utils/bmad/bmad_generator.py`
  - [ ] generate_brief()
  - [ ] generate_prd()
  - [ ] generate_architecture()
  - [ ] generate_epic()
  - [ ] helper functions for sections

- [ ] `hooks/utils/bmad/bmad_validator.py`
  - [ ] validate_prd()
  - [ ] validate_architecture()
  - [ ] validate_epic()
  - [ ] check_cross_references()

### Commands

- [ ] `commands/bmad-start.md` - Complete guided workflow
- [ ] `commands/bmad-brief.md` - Product brief generation
- [ ] `commands/bmad-prd.md` - PRD generation
- [ ] `commands/bmad-architecture.md` - Architecture generation
- [ ] `commands/bmad-epic.md` - Single epic generation (add new/regenerate)
- [ ] `commands/bmad-index.md` - Story index generation

### Documentation

- [ ] Update README with BMAD commands
- [ ] Create BMAD usage guide
- [ ] Add examples of generated documents
- [ ] Update getting-started command

### Testing

- [ ] Test brief generation
- [ ] Test PRD generation
- [ ] Test architecture generation
- [ ] Test epic generation
- [ ] Test complete /bmad:start workflow
- [ ] Test integration with titanium:plan
- [ ] Validate document quality

---

## Version Planning

**Current**: v2.0.0 (Orchestration System)
**Next**: v2.1.0 (BMAD Document Generation)

**Release Timeline**:
- Week 1-4: Orchestration (v2.0.0) ← We are here
- Week 5-8: BMAD Generation (v2.1.0)
- Week 9+: Refinement and advanced features

---

## Questions Answered

**Q**: PRD → Architecture → Epics → Stories order?
**A**: ✅ Yes, this is the flow. Stories are essential (they're within epic files).

**Q**: Why Brief and Stories optional?
**A**:
- **Brief**: Can go directly to PRD if user knows requirements. Brief helps capture initial idea.
- **Stories**: Actually NOT optional - they're in the epic files (STORY-001-01, etc.). Essential for implementation.

**Q**: Folder structure?
**A**: ✅ Option B - BMAD-style with subdirectories (bmad-backlog/prd/, architecture/, epics/)

**Q**: Template fidelity?
**A**: ✅ Strict - Follow BMAD templates exactly for AI consumption

**Q**: Workflow preference?
**A**: ✅ Guided (/bmad:start) for empty folders, incremental commands available too

**Q**: Access BMAD repo?
**A**: ✅ Reference documents from /Users/sem/code/auritrac.com/bmad/output/ and tmp/BMAD-METHOD/

---

**Ready to implement BMAD document generation system after orchestration (v2.0.0) releases!**
