#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "openai",
# ]
# ///

"""
BMAD Document Generator Utility

Generates BMAD methodology documents using GPT-4:
- Product Brief
- PRD (Product Requirements Document)
- Architecture Document
- Epic files with user stories
- Story Index summary

Commands:
    brief <idea> <project_path>                      Generate product brief
    prd <brief_path> <project_path>                  Generate PRD from brief
    architecture <prd_path> <project_path>           Generate architecture from PRD
    epic <prd_path> <arch_path> <epic_num> <project_path>  Generate single epic
    index <epics_dir> <project_path>                Generate story index

Examples:
    uv run bmad_generator.py brief "AI todo app with voice input" "$(pwd)"
    uv run bmad_generator.py prd bmad-backlog/product-brief.md "$(pwd)"
    uv run bmad_generator.py architecture bmad-backlog/prd/prd.md "$(pwd)"
    uv run bmad_generator.py epic bmad-backlog/prd/prd.md bmad-backlog/architecture/architecture.md 1 "$(pwd)"
    uv run bmad_generator.py index bmad-backlog/epics/ "$(pwd)"
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


def generate_brief(idea: str, project_path: str) -> str:
    """
    Generate Product Brief from high-level idea.

    Args:
        idea: User's project idea
        project_path: Project directory path

    Returns:
        Generated brief content
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    current_date = datetime.now().strftime("%B %d, %Y")

    prompt = f"""Generate a comprehensive Product Brief following BMAD methodology.

User's Project Idea:
{idea}

Create a Product Brief with these sections (use exact headers):

# Product Brief: {{Project Name}}

**Version:** 1.0
**Date:** {current_date}
**Status:** Draft

---

## Executive Summary

{{Write 2-3 paragraphs covering:
- Product concept (what it is)
- Problem being solved
- Target market
- Key value proposition}}

---

## Problem Statement

{{Write 2-3 paragraphs covering:
- Current state and pain points (be specific)
- Impact of the problem (quantify if possible)
- Why existing solutions fall short
- Urgency and importance of solving this now}}

---

## Proposed Solution

{{Write 2-3 paragraphs covering:
- Core concept and approach
- Key differentiators from existing solutions
- Why this solution will succeed
- High-level product vision}}

---

## Target Users

### Primary User Segment

{{Define primary users with:
- Demographic/firmographic profile
- Current behaviors and workflows
- Specific needs and pain points
- Goals they're trying to achieve}}

### Secondary User Segment

{{Define secondary users (if applicable) with same details}}

---

## Goals & Success Metrics

### Business Objectives
- {{Objective 1 with metric}}
- {{Objective 2 with metric}}
- {{Objective 3 with metric}}

### User Success Metrics
- {{Metric 1: definition and target}}
- {{Metric 2: definition and target}}
- {{Metric 3: definition and target}}

### Key Performance Indicators (KPIs)
- {{KPI 1: definition and target}}
- {{KPI 2: definition and target}}
- {{KPI 3: definition and target}}

---

## MVP Scope

### Core Features (Must Have)
- **{{Feature 1}}:** {{Description and rationale}}
- **{{Feature 2}}:** {{Description and rationale}}
- **{{Feature 3}}:** {{Description and rationale}}
- **{{Feature 4}}:** {{Description and rationale}}

### Out of Scope for MVP
- {{Feature not included in MVP}}
- {{Feature not included in MVP}}
- {{Feature not included in MVP}}

### MVP Success Criteria
{{What defines MVP success - 2-3 sentences}}

---

## Post-MVP Vision

### Phase 2 Features
{{List 3-5 next-priority features after MVP}}

### Long-term Vision
{{1-2 year vision for the product}}

### Expansion Opportunities
{{Potential future expansions or adjacent markets}}

---

## Technical Considerations

### Platform Requirements
- **Target Platforms:** {{Web/Mobile/Desktop/etc}}
- **Browser/OS Support:** {{Specific requirements}}
- **Performance Requirements:** {{Load time, responsiveness, etc}}

### Technology Preferences
- **Frontend:** {{Framework preference or "TBD"}}
- **Backend:** {{Framework preference or "TBD"}}
- **Database:** {{Database preference or "TBD"}}
- **Hosting/Infrastructure:** {{Hosting preference or "TBD"}}

### Architecture Considerations
- **Repository Structure:** {{Monorepo/Polyrepo preference}}
- **Service Architecture:** {{Monolith/Microservices preference}}
- **Integration Requirements:** {{External integrations needed}}
- **Security/Compliance:** {{Security requirements}}

---

## Constraints & Assumptions

### Constraints
- **Budget:** {{Budget information}}
- **Timeline:** {{Timeline expectations}}
- **Resources:** {{Team size, availability}}
- **Technical:** {{Technical limitations}}

### Key Assumptions
- {{Assumption 1}}
- {{Assumption 2}}
- {{Assumption 3}}

---

## Risks & Open Questions

### Key Risks
- **{{Risk 1}}:** {{Description and potential impact}}
- **{{Risk 2}}:** {{Description and potential impact}}
- **{{Risk 3}}:** {{Description and potential impact}}

### Open Questions
- {{Question 1}}
- {{Question 2}}
- {{Question 3}}

### Areas Needing Further Research
- {{Research area 1}}
- {{Research area 2}}

---

## Next Steps

### Immediate Actions
1. {{Action item 1}}
2. {{Action item 2}}
3. {{Action item 3}}

### PM Handoff
This Product Brief provides the foundation for creating a comprehensive PRD. Next step: Generate PRD with `/bmad:prd` command.

---

Be comprehensive but concise. Infer reasonable defaults based on the idea. Format as clean markdown."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.4
        )

        brief_content = response.choices[0].message.content.strip()

        # Save to file
        brief_path = Path(project_path) / "bmad-backlog" / "product-brief.md"
        brief_path.parent.mkdir(parents=True, exist_ok=True)

        with open(brief_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(brief_content)

        return brief_content

    except Exception as e:
        print(f"Error generating brief: {e}", file=sys.stderr)
        sys.exit(1)


def generate_prd(brief_path: str, project_path: str) -> str:
    """
    Generate PRD from Product Brief.

    Args:
        brief_path: Path to product-brief.md
        project_path: Project directory path

    Returns:
        Generated PRD content
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    # Read brief
    try:
        with open(brief_path, 'r', encoding='utf-8') as f:
            brief_content = f.read()
    except Exception as e:
        print(f"Error reading brief: {e}", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    current_date = datetime.now().strftime("%B %d, %Y")

    # Extract project name from brief
    project_name = extract_project_name(brief_content)

    prompt = f"""Generate a comprehensive Product Requirements Document (PRD) following BMAD methodology.

Product Brief:
{brief_content}

Create a detailed PRD with these sections (use exact headers, follow BMAD template):

# Product Requirements Document (PRD)
## {project_name}

**Document Version:** 1.0
**Last Updated:** {current_date}
**Product Owner:** TBD
**Status:** Draft

---

## Executive Summary

### Vision
{{2-3 paragraphs describing the product vision}}

### Mission
{{1-2 paragraphs describing the mission}}

---

## Product Overview

### Target Users
1. **Primary:** {{User segment with detailed profile}}
2. **Secondary:** {{Secondary segment if applicable}}
3. **Tertiary:** {{Tertiary segment if applicable}}

### Core Value Propositions
1. {{Value prop 1 with details}}
2. {{Value prop 2 with details}}
3. {{Value prop 3 with details}}
4. {{Value prop 4 with details}}
5. {{Value prop 5 with details}}

### Competitive Positioning
- **vs {{Competitor 1}}:** {{How we differ}}
- **vs {{Competitor 2}}:** {{How we differ}}
- **vs {{Competitor 3}}:** {{How we differ}}

---

## Success Metrics

### North Star Metric
**{{Primary metric}}** {{Description and target}}

### Key Performance Indicators

#### Product Metrics
- **Engagement:**
  - {{Metric 1}}: {{Target}}
  - {{Metric 2}}: {{Target}}

- **Feature Adoption:**
  - {{Metric 1}}: {{Target}}
  - {{Metric 2}}: {{Target}}

#### Business Metrics
- **Growth:**
  - {{Metric 1}}: {{Target}}
  - {{Metric 2}}: {{Target}}

- **Revenue:**
  - {{Metric 1}}: {{Target}}
  - {{Metric 2}}: {{Target}}

---

## Feature Requirements

### V1 MVP (12-16 Weeks)

{{For each major feature (4-8 features):}}

#### {{N}}. {{Feature Name}}
**Priority:** P0 (Must Have) or P1 (Should Have)

**Requirements:**
- {{Requirement 1}}
- {{Requirement 2}}
- {{Requirement 3}}

**Acceptance Criteria:**
- [ ] {{Criterion 1}}
- [ ] {{Criterion 2}}
- [ ] {{Criterion 3}}

{{Repeat for all MVP features}}

### V2 Pro Features (8-12 Weeks Post-MVP)

{{List 4-6 post-MVP features with brief descriptions}}

---

## User Stories

{{Organize by Epic - aim for 3-6 epics total}}

### Epic 1: {{Epic Name}}
- As a **{{user}}**, I want **{{action}}** so that **{{benefit}}**
- As a **{{user}}**, I want **{{action}}** so that **{{benefit}}**
{{3-5 stories per epic}}

### Epic 2: {{Epic Name}}
{{Stories...}}

### Epic 3: {{Epic Name}}
{{Stories...}}

{{Continue for all epics}}

CRITICAL: Epic 1 MUST be "Foundation" or "Infrastructure" - establishing project setup, auth, basic structure.

---

## Technical Requirements

### Performance
- {{Metric 1}}: {{Target with p95}}
- {{Metric 2}}: {{Target}}
- {{Metric 3}}: {{Target}}

### Scalability
- Support {{N}} concurrent users (MVP)
- Support {{M}} concurrent users (Production)
- Handle {{X}} requests/operations per {{timeframe}}

### Security & Compliance
- {{Security requirement 1}}
- {{Security requirement 2}}
- {{Compliance standard if applicable}}

### Availability
- {{Uptime SLA}} uptime (free tier)
- {{Uptime SLA}} uptime (Pro tier if applicable)

### Browser Support
- {{Browser 1}} (versions)
- {{Browser 2}} (versions)
- {{Mobile support}}

---

## Data Requirements

### Data Sources
{{If project needs external data}}

#### {{Data Type 1}}
- **Source:** {{Vendor/API name or TBD}}
- **Freshness:** {{Real-time, hourly, daily}}
- **Format:** {{JSON, CSV, etc}}

{{Repeat for all data needs}}

### Data Quality
- {{Quality requirement 1}}
- {{Quality requirement 2}}

---

## AI/ML Requirements

{{Only include if project uses AI}}

### Use Cases

#### {{Use Case 1}}
- **Model:** {{GPT-4, Claude, local model, etc}}
- **Input:** {{What goes in}}
- **Output:** {{What comes out}}
- **Latency:** {{Response time requirement}}
- **Quality:** {{Accuracy/precision target}}

{{Repeat for all AI use cases}}

### Guardrails
- {{Guardrail 1 - e.g., source attribution}}
- {{Guardrail 2 - e.g., confidence thresholds}}
- {{Guardrail 3 - e.g., hallucination prevention}}

### Evaluation
- {{How to measure AI quality}}
- {{Evaluation frequency}}

---

## Design Requirements

### Design System
- **Framework:** {{Tailwind, Material UI, etc}}
- **Theme:** {{Dark/Light/Both}}
- **Accessibility:** {{WCAG level or None}}
- **Responsiveness:** {{Mobile-first, Desktop-first}}

### Key Screens
1. {{Screen 1 name and brief description}}
2. {{Screen 2 name and brief description}}
3. {{Screen 3 name and brief description}}
{{List 5-10 critical screens}}

---

## Go-to-Market Strategy

### Launch Phases

#### Phase 1: {{Phase name (e.g., Closed Alpha)}}
- {{Details, timeline, scope}}

#### Phase 2: {{Phase name}}
- {{Details}}

### Pricing Strategy
- **Free Tier:** {{Features and limitations}}
- **Pro Tier:** ${{price}}/month - {{Features}}
- **Team Tier:** {{If applicable}}

### Customer Acquisition
- **Organic:** {{SEO, content, etc}}
- **Community:** {{Platforms}}
- **Partnerships:** {{Ideas}}
- **Paid:** {{Advertising channels}}

---

## Risks & Mitigation

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| {{Risk 1}} | {{High/Med/Low}} | {{High/Med/Low}} | {{How to mitigate}} |
| {{Risk 2}} | {{High/Med/Low}} | {{High/Med/Low}} | {{How to mitigate}} |
| {{Risk 3}} | {{High/Med/Low}} | {{High/Med/Low}} | {{How to mitigate}} |

### Business Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| {{Risk 1}} | {{High/Med/Low}} | {{High/Med/Low}} | {{How to mitigate}} |
| {{Risk 2}} | {{High/Med/Low}} | {{High/Med/Low}} | {{How to mitigate}} |

---

## Open Questions

1. {{Question 1}}
2. {{Question 2}}
3. {{Question 3}}
{{List 5-10 unresolved questions}}

---

## Appendix

### Glossary
- **{{Term 1}}:** {{Definition}}
- **{{Term 2}}:** {{Definition}}

### References
- {{Link 1}}: {{Description}}
- {{Link 2}}: {{Description}}

---

**Document Status:** ✅ Ready for Technical Review
**Next Steps:** Architecture document, epic breakdown

---

IMPORTANT GUIDELINES:
1. Be comprehensive - aim for 500-1000 lines
2. Epic 1 MUST be "Foundation" or "Infrastructure"
3. Include specific acceptance criteria (not vague)
4. Use proper priority labels (P0, P1, P2)
5. Make user stories actionable ("As a X, I want Y, so that Z")
6. Include realistic metrics and targets
7. Be specific with technical requirements
8. Format as clean markdown with proper headers"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3
        )

        prd_content = response.choices[0].message.content.strip()

        # Save to file
        prd_path = Path(project_path) / "bmad-backlog" / "prd" / "prd.md"
        prd_path.parent.mkdir(parents=True, exist_ok=True)

        with open(prd_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(prd_content)

        return prd_content

    except Exception as e:
        print(f"Error generating PRD: {e}", file=sys.stderr)
        sys.exit(1)


def extract_project_name(content: str) -> str:
    """Extract project name from document header."""

    # Pattern 1: Look for "# Product Requirements Document (PRD)" followed by "## ProjectName"
    prd_h1_match = re.search(r'(?m)^#\s+Product Requirements Document(?:\s+\(PRD\))?', content)
    if prd_h1_match:
        # Found PRD header, now find the next H2 line
        after_prd = content[prd_h1_match.end():]
        h2_match = re.search(r'(?m)^##\s+(.+?)(?:\s+-\s+|\s*$)', after_prd)
        if h2_match:
            return h2_match.group(1).strip()

    # Pattern 2: Look for "# Product Brief: NAME" or "# Architecture Document"
    title_match = re.search(r'(?m)^#\s+(?:Product Brief|Architecture Document|PRD|Project):\s*(.+)', content)
    if title_match:
        return title_match.group(1).strip()

    # Pattern 3: Look for standalone H1 with project name
    h1_match = re.search(r'(?m)^#\s+([^#\n]+?)(?:\s+-\s+|\s*$)', content)
    if h1_match:
        title = h1_match.group(1).strip()
        # Skip generic headers
        if title not in ['Product Requirements Document', 'Architecture Document', 'Product Brief', 'PRD']:
            return title

    # Pattern 4: Look for H2 with project name (fallback)
    h2_match = re.search(r'(?m)^##\s+(.+?)(?:\s+-\s+|\s*$)', content)
    if h2_match:
        title = h2_match.group(1).strip()
        # Skip generic headers
        if title not in ['Executive Summary', 'Table of Contents', 'Overview']:
            return title

    return "Project"


def generate_architecture(prd_path: str, project_path: str) -> str:
    """
    Generate Architecture document from PRD.

    Args:
        prd_path: Path to prd.md
        project_path: Project directory path

    Returns:
        Generated architecture content
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    # Read PRD
    try:
        with open(prd_path, 'r', encoding='utf-8') as f:
            prd_content = f.read()
    except Exception as e:
        print(f"Error reading PRD: {e}", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    current_date = datetime.now().strftime("%B %d, %Y")
    project_name = extract_project_name(prd_content)

    prompt = f"""Generate a comprehensive Architecture Document following BMAD methodology.

Product Requirements Document:
{prd_content[:3000]}  # First part for context

Based on the PRD above, create a detailed Architecture Document.

This will be generated in TWO parts due to length. This is PART 1.

# Architecture Document
## {project_name}

**Document Version:** 1.0
**Last Updated:** {current_date}
**Architecture Owner:** TBD
**Status:** Draft

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [High-Level Architecture](#high-level-architecture)
4. [Component Details](#component-details)
5. [Data Architecture](#data-architecture)
6. [Infrastructure](#infrastructure)
7. [Security Architecture](#security-architecture)
8. [Deployment Strategy](#deployment-strategy)
9. [Monitoring & Observability](#monitoring--observability)
10. [Appendix](#appendix)

---

## System Overview

### Context
{{2-3 paragraphs explaining what the system does, referencing PRD features}}

### Key Requirements
{{Extract from PRD:
- Latency targets
- Throughput requirements
- Availability needs
- Security requirements}}

---

## Architecture Principles

{{List 6-10 guiding principles, e.g.:
1. **Mobile-First Design:** Responsive, progressive enhancement
2. **API-First Development:** RESTful/GraphQL, versioned
3. **Event-Driven Where Appropriate:** Async workflows
4. **AI Transparency:** Source attribution, confidence thresholds
5. **Observability-First:** Metrics, logging, tracing
6. **Cost Optimization:** Efficient scaling, caching}}

---

## High-Level Architecture

{{Create ASCII diagram showing all layers:
- Client Layer (Frontend)
- API Gateway Layer
- Application Layer (Backend services)
- Business Logic Layer
- Data Layer (Databases, cache)
- Data Ingestion Layer (if applicable)
- Streaming/Event Layer (if applicable)
- AI/ML Layer (if applicable)
- External Integrations

Use box-drawing characters for clarity}}

Example format:
```
┌─────────────────────────────────────────┐
│          CLIENT LAYER                    │
├─────────────────────────────────────────┤
│  Next.js / React                         │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       APPLICATION LAYER                  │
├─────────────────────────────────────────┤
│  FastAPI / Express                       │
└─────────────────────────────────────────┘
{{etc}}
```

---

## Component Details

### Frontend

#### Technology Stack
- **Framework:** {{Next.js/React/Vue/etc based on PRD}}
- **Language:** {{TypeScript/JavaScript}}
- **Styling:** {{Tailwind/CSS-in-JS/etc}}
- **State Management:** {{Zustand/Redux/Context}}
- **Data Fetching:** {{React Query/SWR/etc}}

#### Key Features
- {{Feature 1}}
- {{Feature 2}}
- {{Feature 3}}

#### File Structure
```
app/ or src/
├── (auth)/
│   ├── login/
│   └── register/
├── (dashboard)/
│   ├── page.tsx
│   └── {{routes based on PRD}}
├── components/
│   ├── ui/
│   └── {{feature components}}
└── lib/
    ├── api-client.ts
    └── utils.ts
```

### Backend

#### Technology Stack
- **Framework:** {{FastAPI/Express/Django based on PRD}}
- **Language:** {{Python/Node.js/etc}}
- **ORM:** {{SQLAlchemy/Prisma/TypeORM}}
- **Validation:** {{Pydantic/Zod/etc}}
- **Async:** {{asyncio/promises}}

#### Service Architecture
```
services/
├── api/
│   ├── routers/
│   │   ├── {{route1}}.py
│   │   ├── {{route2}}.py
│   │   └── {{route3}}.py
│   ├── dependencies.py
│   └── main.py
├── models/
├── schemas/
└── services/
```

---

Generate this first part comprehensively. Include specific tech stack based on PRD requirements. Be detailed. Next, I'll request part 2 with Data Architecture, Security, etc."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3
        )

        arch_part1 = response.choices[0].message.content.strip()

        # Generate Part 2
        prompt_part2 = f"""Continue the Architecture Document. This is PART 2.

Here's what you generated in Part 1:
{arch_part1[:1000]}

Now generate the remaining sections:

---

## Data Architecture

### Database Schema ({{PostgreSQL/MySQL/MongoDB based on tech stack}})

{{Generate CREATE TABLE statements for all main entities from PRD}}

Example:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

{{Add more tables for all PRD entities}}
```

{{If time-series data needed:}}
### Time-Series Tables (TimescaleDB)
```sql
CREATE TABLE {{timeseries_table}} (
    time TIMESTAMPTZ NOT NULL,
    {{fields}},
    PRIMARY KEY (time, {{partition_key}})
);

SELECT create_hypertable('{{table}}', 'time');
```

{{If AI features:}}
### Vector Store (pgvector)
```sql
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id UUID PRIMARY KEY,
    embedding vector(1536),
    {{fields}}
);
```

---

## Infrastructure

### MVP Deployment ({{Railway/Vercel/etc}})
{{Configuration, services, why chosen}}

### Production Deployment ({{GKE/ECS/etc}})
{{When to migrate, architecture, cost}}

---

## Security Architecture

### Authentication & Authorization
{{Flow diagram, JWT details, code examples}}

### Rate Limiting
{{Tier-based limits, implementation with code}}

### Data Encryption
{{At rest, in transit}}

---

## Deployment Strategy

### CI/CD Pipeline
```yaml
{{GitHub Actions or similar YAML}}
```

### Database Migrations
{{Alembic/Flyway examples}}

---

## Monitoring & Observability

### Metrics (Prometheus)
```python
{{Code examples of metrics}}
```

### Logging
```python
{{Structured logging examples}}
```

---

## Appendix

### Technology Decisions

| Component | Choice | Alternatives | Rationale |
|-----------|--------|-------------|-----------|
| Frontend | {{choice}} | {{alt1, alt2}} | {{why}} |
| Backend | {{choice}} | {{alt1, alt2}} | {{why}} |
| Database | {{choice}} | {{alt1, alt2}} | {{why}} |

### Performance Benchmarks

| Metric | Target | Measurement |
|--------|--------|-------------|
| {{metric}} | {{target}} | {{how measured}} |

### Cost Estimates

**MVP:**
- {{Service 1}}: ${{X}}/month
- {{Service 2}}: ${{Y}}/month
- **Total: ~${{Z}}/month**

**Production:**
- {{Scaled costs}}

---

**Document Status:** ✅ Ready for Implementation
**Next Steps:** Epic breakdown, story writing

---

Be comprehensive. Include real code examples. Be specific with costs."""

        response_part2 = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_part2}],
            max_tokens=4000,
            temperature=0.3
        )

        arch_part2 = response_part2.choices[0].message.content.strip()

        # Combine parts
        arch_content = arch_part1 + "\n\n" + arch_part2

        # Save to file
        arch_path = Path(project_path) / "bmad-backlog" / "architecture" / "architecture.md"
        arch_path.parent.mkdir(parents=True, exist_ok=True)

        with open(arch_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(arch_content)

        return arch_content

    except Exception as e:
        print(f"Error generating architecture: {e}", file=sys.stderr)
        sys.exit(1)


def generate_epic(prd_path: str, arch_path: str, epic_number: int, project_path: str) -> str:
    """
    Generate single epic file with user stories.

    Args:
        prd_path: Path to prd.md
        arch_path: Path to architecture.md
        epic_number: Epic number to generate
        project_path: Project directory path

    Returns:
        Generated epic content
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    # Read PRD and Architecture
    try:
        with open(prd_path, 'r', encoding='utf-8') as f:
            prd_content = f.read()
        with open(arch_path, 'r', encoding='utf-8') as f:
            arch_content = f.read()
    except Exception as e:
        print(f"Error reading documents: {e}", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    current_date = datetime.now().strftime("%B %d, %Y")

    # Extract epic info from PRD
    epic_pattern = f"### Epic {epic_number}:"
    epic_section = extract_section(prd_content, epic_pattern)

    if not epic_section:
        print(f"Error: Epic {epic_number} not found in PRD", file=sys.stderr)
        sys.exit(1)

    prompt = f"""Generate a detailed Epic file following BMAD methodology.

Epic from PRD:
{epic_section}

Relevant Architecture (for technical notes):
{arch_content[:2000]}

Create epic file with this structure:

# EPIC-{epic_number:03d}: {{Epic Title}}

**Epic Owner:** {{Team or role}}
**Priority:** P0 (Must Have) or P1 (Should Have) or P2 (Nice to Have)
**Target Sprint:** Sprint {{X-Y}}
**Status:** 📋 Not Started
**Estimated Effort:** {{X}} story points

---

## Epic Description

{{2-3 paragraphs explaining:
- What this epic delivers
- Why it's important
- How it fits in the overall product}}

---

## Business Value

- {{Value point 1}}
- {{Value point 2}}
- {{Value point 3}}

---

## Success Criteria

- [ ] {{Epic-level success criterion 1}}
- [ ] {{Epic-level success criterion 2}}
- [ ] {{Epic-level success criterion 3}}

---

## User Stories

{{Generate 8-15 user stories for this epic}}

### STORY-{epic_number:03d}-{{story_num:02d}}: {{Story Title}}
**As a** {{user type}}
**I want** {{action}}
**So that** {{benefit}}

**Acceptance Criteria:**
- [ ] {{Criterion 1}}
- [ ] {{Criterion 2}}
- [ ] {{Criterion 3}}

**Technical Notes:**
```{{language}}
{{Code examples, file structures, or implementation hints from architecture}}
```

{{Repeat for all stories in this epic}}

---

## Dependencies

**Blocks:**
- {{What this epic enables}}

**Blocked By:**
- {{What must be done first}}

---

## Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| {{Risk}} | {{High/Med/Low}} | {{High/Med/Low}} | {{Mitigation}} |

---

## Technical Debt

- [ ] {{Known shortcut or future improvement}}
- [ ] {{Another item}}

---

## Related Epics

- **EPIC-{{X}}:** {{Relationship}}
- **EPIC-{{Y}}:** {{Relationship}}

---

## Definition of Done

- [ ] All user stories accepted by Product Owner
- [ ] Code reviewed and merged
- [ ] Unit tests pass with >70% coverage
- [ ] Integration tests pass
- [ ] Deployed to staging
- [ ] Documentation updated

---

**Last Updated:** {current_date}
**Status History:**
- {current_date}: Epic created

---

IMPORTANT:
- Be comprehensive (300-500 lines)
- Stories should be sequentially logical
- Include technical notes with code examples
- Reference architecture document
- Story format: STORY-{epic_number:03d}-{{num:02d}}
- Make acceptance criteria specific and testable"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3
        )

        epic_content = response.choices[0].message.content.strip()

        # Extract epic title for filename
        title_match = re.search(r'EPIC-\d+:\s*(.+)', epic_content)
        epic_title = title_match.group(1).strip() if title_match else "epic"
        epic_slug = epic_title.lower().replace(' ', '-').replace('&', 'and')

        # Save to file
        epic_path = Path(project_path) / "bmad-backlog" / "epics" / f"EPIC-{epic_number:03d}-{epic_slug}.md"
        epic_path.parent.mkdir(parents=True, exist_ok=True)

        with open(epic_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(epic_content)

        return epic_content

    except Exception as e:
        print(f"Error generating epic: {e}", file=sys.stderr)
        sys.exit(1)


def extract_section(content: str, section_header: str) -> str:
    """Extract section from markdown document."""
    lines = content.split('\n')
    section_lines = []
    in_section = False

    for line in lines:
        if section_header.lower() in line.lower():
            in_section = True
        elif in_section and line.startswith('#') and section_header not in line:
            break
        elif in_section:
            section_lines.append(line)

    return '\n'.join(section_lines).strip()


def generate_index(epics_dir: str, project_path: str) -> str:
    """
    Generate STORY-INDEX.md from all epic files.

    Args:
        epics_dir: Path to epics directory
        project_path: Project directory path

    Returns:
        Generated index content
    """
    epics_path = Path(epics_dir)

    if not epics_path.exists():
        print(f"Error: Epics directory not found: {epics_dir}", file=sys.stderr)
        sys.exit(1)

    # Scan for epic files
    epic_files = sorted(epics_path.glob("EPIC-*.md"))

    if not epic_files:
        print("Error: No epic files found", file=sys.stderr)
        sys.exit(1)

    # Parse each epic
    epics_data = []
    total_stories = 0
    total_points = 0

    for epic_file in epic_files:
        with open(epic_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract epic number and name
        match = re.search(r'EPIC-(\d+):\s*(.+)', content)
        if match:
            epic_num = int(match.group(1))
            epic_name = match.group(2).strip()
        else:
            continue

        # Count stories
        story_count = len(re.findall(r'### STORY-\d+-\d+:', content))

        # Estimate story points (rough - could parse if documented)
        estimated_points = story_count * 4  # Average 4 points per story

        epics_data.append({
            'number': epic_num,
            'name': epic_name,
            'stories': story_count,
            'points': estimated_points,
            'file': epic_file.name
        })

        total_stories += story_count
        total_points += estimated_points

    # Generate index
    current_date = datetime.now().strftime("%B %d, %Y")

    # Extract project name (prioritize PRD > Brief > Epic, avoid file leaks)
    project_name = "Project"  # Default

    # Try PRD first
    prd_file = Path(project_path) / "bmad-backlog" / "prd" / "prd.md"
    if prd_file.exists():
        try:
            with open(prd_file, 'r', encoding='utf-8') as f:
                project_name = extract_project_name(f.read())
        except Exception:
            pass

    # If no name from PRD, try Brief
    if project_name == "Project":
        brief_file = Path(project_path) / "bmad-backlog" / "product-brief.md"
        if brief_file.exists():
            try:
                with open(brief_file, 'r', encoding='utf-8') as f:
                    project_name = extract_project_name(f.read())
            except Exception:
                pass

    # If still no name, fall back to first epic
    if project_name == "Project" and epic_files:
        try:
            with open(epic_files[0], 'r', encoding='utf-8') as f:
                project_name = extract_project_name(f.read())
        except Exception:
            pass

    index_content = f"""# {project_name} - Story Index

**Total Epics:** {len(epics_data)}
**Total User Stories:** {total_stories}
**Total Story Points:** {total_points} (estimated)
**Version:** 1.0
**Last Updated:** {current_date}

---

## Epic Overview

| Epic ID | Epic Name | Stories | Story Points | Status |
|---------|-----------|---------|--------------|--------|
"""

    for epic in epics_data:
        index_content += f"| EPIC-{epic['number']:03d} | {epic['name']} | {epic['stories']} | {epic['points']} | Not Started |\n"

    index_content += f"| **TOTAL** | | **{total_stories}** | **{total_points}** | |\n"
    index_content += "\n---\n\n"

    # Add per-epic story details (would need to parse story IDs from files)
    index_content += """## Story Details

For detailed story breakdown, see individual epic files in `epics/` directory.

---

## Priority Distribution

{{To be calculated from individual story priorities}}

---

## Development Phases

{{To be defined based on epic dependencies and sequencing}}

---

**Next Steps:**
1. Review and approve epic breakdown
2. Prioritize stories for Sprint 1
3. Begin implementation with `/titanium:plan bmad-backlog/epics/EPIC-001-*.md`

"""

    # Save to file
    index_path = Path(project_path) / "bmad-backlog" / "STORY-INDEX.md"

    with open(index_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(index_content)

    return index_content


def main():
    """CLI interface for BMAD document generation."""

    if len(sys.argv) < 3:
        print("Usage: bmad_generator.py <command> <args...>", file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        print("  brief <idea> <project_path>", file=sys.stderr)
        print("  prd <brief_path> <project_path>", file=sys.stderr)
        print("  architecture <prd_path> <project_path>", file=sys.stderr)
        print("  epic <prd_path> <arch_path> <epic_num> <project_path>", file=sys.stderr)
        print("  index <epics_dir> <project_path>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "brief":
            idea = sys.argv[2]
            project_path = sys.argv[3]
            content = generate_brief(idea, project_path)
            print(f"✅ Product brief generated: bmad-backlog/product-brief.md")

        elif command == "prd":
            brief_path = sys.argv[2]
            project_path = sys.argv[3]
            content = generate_prd(brief_path, project_path)
            print(f"✅ PRD generated: bmad-backlog/prd/prd.md")

        elif command == "architecture":
            prd_path = sys.argv[2]
            project_path = sys.argv[3]
            content = generate_architecture(prd_path, project_path)
            print(f"✅ Architecture generated: bmad-backlog/architecture/architecture.md")

        elif command == "epic":
            prd_path = sys.argv[2]
            arch_path = sys.argv[3]
            epic_num = int(sys.argv[4])
            project_path = sys.argv[5]
            content = generate_epic(prd_path, arch_path, epic_num, project_path)
            print(f"✅ Epic {epic_num} generated")

        elif command == "index":
            epics_dir = sys.argv[2]
            project_path = sys.argv[3]
            content = generate_index(epics_dir, project_path)
            print(f"✅ Story index generated: bmad-backlog/STORY-INDEX.md")

        else:
            print(f"Error: Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
