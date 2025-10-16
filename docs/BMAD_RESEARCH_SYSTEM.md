# BMAD Research System

**Purpose**: Enable structured research for technical decisions before architecture generation

**Problem**: Complex projects need API research, vendor evaluation, data source analysis, etc. Claude Code doesn't have robust web search, but web-based Claude/ChatGPT does.

**Solution**: Generate research prompts that users take to web AI, then import findings back.

---

## Workflow

### When Research is Needed

**During PRD generation**, if user mentions:
- "Need to integrate with APIs" → Research APIs
- "Need real-time data" → Research data vendors
- "Need payment processing" → Research Stripe vs alternatives
- "Need AI models" → Research LLM options
- "Need hosting" → Research Railway vs Vercel vs GCP

**Claude Code detects and suggests**:
```
⚠️  I detected you need [API/vendor/data source] research.

Would you like me to generate a research prompt?

This will:
1. Create a research prompt you can copy/paste to ChatGPT/Claude web
2. Generate a template for documenting findings
3. Save results to bmad-backlog/research/ folder
4. Use findings in architecture generation

Generate research prompt? (yes/no)
```

---

## The `/bmad:research` Command

### Command Specification

**File**: `commands/bmad-research.md`

**Purpose**: Generate structured research prompts and templates

**Usage**:
```bash
# Generate research prompt for topic
/bmad:research "data vendors for precious metals pricing"

# Or let Claude detect needs from PRD
/bmad:research
# → Claude: "I see your PRD mentions real-time pricing. Research that?"
```

### What It Generates

#### 1. Research Prompt (for web AI)

Creates: `bmad-backlog/research/RESEARCH-{topic}-prompt.md`

**Content**:
```markdown
# Research Prompt: {Topic}

Copy this entire prompt and paste into ChatGPT (GPT-4) or Claude (web) which have web search.

---

## Research Request

I'm building: {project name from PRD}

I need to research: {topic}

Please research and provide:

### 1. Overview
- What options exist in this space?
- What are the top 3-5 solutions/vendors/APIs?

### 2. Comparison Table

| Option | Pricing | Features | Pros | Cons | Best For |
|--------|---------|----------|------|------|----------|
| Option 1 | ... | ... | ... | ... | ... |
| Option 2 | ... | ... | ... | ... | ... |

### 3. Technical Details

For each option:
- API documentation links
- Authentication method
- Rate limits
- Data formats (JSON, XML, etc.)
- SDK availability (Python, Node.js, etc.)
- Code examples (if available)

### 4. Integration Complexity

- Estimated implementation time
- Dependencies required
- Learning curve
- Community support

### 5. Recommendations

Based on my project needs:
[List key requirements from PRD]

Which option would you recommend and why?

### 6. Cost Analysis

- Free tier availability
- Pricing tiers
- Estimated monthly cost for:
  - MVP (low volume)
  - Production (medium volume)
  - Scale (high volume)

### 7. Risks & Considerations

- Vendor lock-in risk
- Data freshness/accuracy
- Compliance requirements
- Regional availability
- Uptime SLAs

### 8. Source Links

Provide links to:
- Official documentation
- Pricing pages
- API references
- Community discussions
- Comparison articles

---

**After research**: Copy findings into the template I provided in:
bmad-backlog/research/RESEARCH-{topic}-findings.md
```

#### 2. Research Findings Template

Creates: `bmad-backlog/research/RESEARCH-{topic}-findings.md`

**Content**:
```markdown
# Research Findings: {Topic}

**Date**: {current date}
**Researcher**: {user name}
**Status**: Draft | Reviewed | Approved

---

## Research Summary

**Question**: {what was researched}

**Recommendation**: {chosen option and why}

**Confidence**: High | Medium | Low

---

## Options Evaluated

### Option 1: {Name}

**Overview**: {1-2 sentence description}

**Pricing**:
- Free tier: {details}
- Paid tiers: {details}
- Estimated cost for our use case: ${X}/month

**Features**:
- Feature 1
- Feature 2
- Feature 3

**Pros**:
- Pro 1
- Pro 2

**Cons**:
- Con 1
- Con 2

**Technical Details**:
- API: {REST/GraphQL/etc}
- Authentication: {API key/OAuth/etc}
- Rate limits: {X requests/minute}
- Data format: {JSON/XML/etc}
- SDKs: {Python, Node.js, etc}

**Documentation**: {link}

---

### Option 2: {Name}

[... same structure ...]

---

## Comparison Matrix

| Criteria | Option 1 | Option 2 | Option 3 | Winner |
|----------|----------|----------|----------|--------|
| Cost (MVP) | ${X}/mo | ${Y}/mo | ${Z}/mo | {Option} |
| Features | {count} | {count} | {count} | {Option} |
| API Quality | {rating} | {rating} | {rating} | {Option} |
| Documentation | {rating} | {rating} | {rating} | {Option} |
| Community | {rating} | {rating} | {rating} | {Option} |
| Ease of Use | {rating} | {rating} | {rating} | {Option} |

---

## Recommendation

**Chosen**: {Option X}

**Rationale**:
1. {Reason 1}
2. {Reason 2}
3. {Reason 3}

**Implementation Notes**:
- {Technical consideration 1}
- {Technical consideration 2}

**Cost Projection**:
- MVP: ${X}/month
- Production: ${Y}/month
- Scale: ${Z}/month

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| {Risk 1} | {High/Med/Low} | {High/Med/Low} | {How to mitigate} |
| {Risk 2} | {High/Med/Low} | {High/Med/Low} | {How to mitigate} |

---

## Implementation Checklist

- [ ] Create account with {vendor}
- [ ] Obtain API key
- [ ] Test API in development
- [ ] Review pricing and set alerts
- [ ] Document in architecture
- [ ] Add to .env.example

---

## References

- {Link 1}: {Description}
- {Link 2}: {Description}
- {Link 3}: {Description}

---

## Next Steps

1. Review this research with team
2. Make final decision on {chosen option}
3. Update PRD with data source details
4. Update Architecture with integration approach
5. Add to technical assumptions

---

**Status**: ✅ Research Complete | ⏳ Awaiting Approval
```

---

## Integration with BMAD Workflow

### Updated BMAD Workflow

```
/bmad:start
  ↓
Product Brief created
  ↓
PRD Generation starts
  ↓
Claude detects: "You need data vendors, APIs, etc."
  ↓
/bmad:research "data vendors" (automatic or user-triggered)
  ↓
Research prompt generated → User copies to ChatGPT/Claude web
  ↓
User pastes findings into template
  ↓
Research saved to bmad-backlog/research/
  ↓
PRD updated with research findings
  ↓
Architecture generation
  ↓
Architecture references research docs
  ↓
Complete backlog ready
```

### Folder Structure with Research

```
bmad-backlog/
├── product-brief.md
├── prd/
│   └── prd.md
├── architecture/
│   └── architecture.md
├── research/                           # NEW
│   ├── RESEARCH-data-vendors-prompt.md
│   ├── RESEARCH-data-vendors-findings.md
│   ├── RESEARCH-auth-providers-prompt.md
│   ├── RESEARCH-auth-providers-findings.md
│   └── RESEARCH-hosting-platforms-prompt.md
│       RESEARCH-hosting-platforms-findings.md
├── epics/
│   └── EPIC-*.md
└── STORY-INDEX.md
```

---

## Command Specification: `/bmad:research`

**File**: `commands/bmad-research.md`

```markdown
---
description: Generate research prompts for technical decisions
---

# BMAD Research Command

You are helping the user research technical decisions for their project.

## Purpose

Generate structured research prompts that users can take to web-based AI (ChatGPT, Claude web) which have web search capabilities. Results are documented in bmad-backlog/research/ for reference during architecture generation.

## When to Use

Research is needed when:
- Evaluating API vendors or data sources
- Comparing hosting platforms
- Choosing between frameworks/libraries
- Evaluating payment processors
- Selecting authentication providers
- Analyzing third-party integrations
- Cost/vendor comparisons

## Process

### Step 1: Identify Research Topic

Ask user (if not provided):
```
What do you need to research?

Common topics:
1. Data vendors/APIs
2. Hosting platforms
3. Authentication providers
4. Payment processors
5. AI/ML model options
6. Third-party integrations
7. Other (specify)

Topic:
```

### Step 2: Gather Context

Read PRD if it exists:
```bash
Read bmad-backlog/prd/prd.md
```

Extract relevant requirements:
- What features need this?
- What are the constraints? (budget, performance, etc.)
- Any technical preferences?

### Step 3: Generate Research Prompt

Create comprehensive research prompt file.

Save to: `bmad-backlog/research/RESEARCH-{topic-slug}-prompt.md`

**Prompt Template**:
[Include complete prompt with project context, comparison criteria, technical requirements, cost analysis, etc.]

### Step 4: Generate Findings Template

Create structured template for documenting research.

Save to: `bmad-backlog/research/RESEARCH-{topic-slug}-findings.md`

**Template includes**:
- Options evaluated
- Comparison matrix
- Recommendation
- Implementation notes
- Cost projections
- Risks
- References

### Step 5: Present to User

```
📋 Research Prompt Generated

Topic: {topic}

I've created two files:

1. **Prompt**: bmad-backlog/research/RESEARCH-{topic}-prompt.md
   → Copy this entire file
   → Paste into ChatGPT (GPT-4) or Claude (web)
   → They have web search and can research thoroughly

2. **Template**: bmad-backlog/research/RESEARCH-{topic}-findings.md
   → After research, copy findings into this template
   → Fill in the sections
   → Save the file

---

Steps:
1. Open: bmad-backlog/research/RESEARCH-{topic}-prompt.md
2. Copy entire content
3. Go to: https://chat.openai.com (or https://claude.ai)
4. Paste prompt
5. Wait for comprehensive research
6. Copy findings into template: bmad-backlog/research/RESEARCH-{topic}-findings.md
7. Come back and run: /bmad:prd or /bmad:architecture
   (I'll reference your research automatically)

Ready to view the prompt?
```

Show the prompt content so user can copy.

### Step 6: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Research prompt for {topic}",
  summary: "Generated research prompt for {topic}. User will research: {what to research}. Template provided for documenting findings. Findings will inform: {PRD/Architecture section}",
  files: [
    "bmad-backlog/research/RESEARCH-{topic}-prompt.md",
    "bmad-backlog/research/RESEARCH-{topic}-findings.md"
  ],
  project: "$(pwd)"
)
```

## Integration with Other Commands

### In `/bmad:prd`

Before Technical Assumptions section:
```
Check for research needs:
"I see you need data vendors. Would you like me to generate a research prompt? (yes/no)"

If yes:
- Run /bmad:research "data vendors"
- Wait for user to complete research
- Continue PRD with findings

If research findings exist:
- Read bmad-backlog/research/*.md files
- Incorporate recommendations into PRD
- Reference research in Technical Assumptions
```

### In `/bmad:architecture`

Before generating:
```
Check bmad-backlog/research/ folder

If research findings exist:
- Read all RESEARCH-*-findings.md files
- Use recommended options in architecture
- Reference research docs in technology decisions table
- Include cost estimates from research

Example:
"Based on research findings (RESEARCH-data-vendors-findings.md),
we'll use Zylalabs API marketplace..."
```

---

## Research Prompt Example

**For Data Vendors**:

```markdown
# Research Prompt: Data Vendors for Precious Metals Pricing

Copy this prompt to ChatGPT (GPT-4) or Claude (web) which have web search.

---

I'm building AuricBeat, an AI-powered precious metals research platform.

I need real-time and historical data for:
- Spot prices (Gold, Silver, Platinum, Palladium)
- Futures prices (COMEX)
- Mining company equities (NYSE, TSX, ASX, AIM)
- USD Index (DXY)
- 10Y real yields

**Requirements**:
- Real-time pricing (<1 second lag for spots)
- Historical data (10+ years)
- API-based (REST or WebSocket)
- Reliable uptime (>99.5%)
- Cost-effective for MVP (<$300/month)

**Please research and compare**:

1. Zylalabs API Marketplace
2. IEX Cloud
3. Polygon.io
4. Alpha Vantage
5. Twelve Data
6. Nasdaq Data Link

For each, provide:
- Pricing (free tier, paid tiers)
- Data coverage (which metals, which exchanges)
- API quality (REST/WebSocket, documentation)
- Rate limits
- Data freshness (real-time vs delayed)
- Community/support
- Code examples (Python, Node.js)

**Create comparison table** and recommend best option for:
- MVP (budget-conscious)
- Production (quality-focused)
- Enterprise (complete coverage)

Include links to: pricing pages, API docs, community reviews.
```

**User takes this to web AI, gets comprehensive research with web results, brings findings back.**

---

## Utility Script: `research_generator.py`

**Location**: `hooks/utils/bmad/research_generator.py`

**Commands**:
```bash
# Generate research prompt
uv run research_generator.py prompt "data vendors" "bmad-backlog/prd/prd.md" "$(pwd)"

# Generate findings template
uv run research_generator.py template "data vendors" "$(pwd)"
```

**Functions**:
```python
def generate_research_prompt(topic: str, prd_path: str, project_path: str) -> str:
    """Generate research prompt with project context"""
    # Read PRD if exists
    # Extract relevant requirements
    # Generate comprehensive research prompt
    # Include: project context, requirements, comparison criteria
    # Save to bmad-backlog/research/RESEARCH-{topic}-prompt.md
    pass

def generate_findings_template(topic: str, project_path: str) -> str:
    """Generate template for documenting findings"""
    # Create structured template
    # Sections: Options, Comparison, Recommendation, Costs, Risks
    # Save to bmad-backlog/research/RESEARCH-{topic}-findings.md
    pass
```

---

## Integration Points

### 1. PRD Generation

**Before Technical Assumptions section**:
```
Claude: "I see you need:
- Real-time data vendor
- Payment processing
- Authentication provider

Would you like research prompts for these? (yes/all/no)"

User: "yes data vendor"

Claude:
- Generates research prompt
- Generates findings template
- "Please complete research and come back when done"
- Pauses PRD generation

User: [Does research in ChatGPT, fills template]

User: "Done with research"

Claude:
- Reads bmad-backlog/research/RESEARCH-data-vendor-findings.md
- Uses recommendation in PRD Technical Assumptions
- Continues PRD generation
```

### 2. Architecture Generation

**During tech stack selection**:
```
Claude: "Checking for research findings..."

[Reads all bmad-backlog/research/*-findings.md files]

Claude: "Based on your research:
- Data vendor: Zylalabs (from RESEARCH-data-vendors-findings.md)
- Auth: Custom JWT (from RESEARCH-auth-providers-findings.md)
- Hosting: Railway MVP (from RESEARCH-hosting-findings.md)

I'll use these in the architecture."

[Generates architecture with researched options]
[References research docs in Technology Decisions table]
```

---

## Research Topics (Common)

### Technical Infrastructure
- `/bmad:research "hosting platforms"`
- `/bmad:research "CI/CD providers"`
- `/bmad:research "monitoring solutions"`
- `/bmad:research "CDN providers"`

### Data & APIs
- `/bmad:research "data vendors"`
- `/bmad:research "API marketplaces"`
- `/bmad:research "real-time data feeds"`
- `/bmad:research "database options"`

### Third-Party Services
- `/bmad:research "authentication providers"`
- `/bmad:research "payment processors"`
- `/bmad:research "email services"`
- `/bmad:research "SMS providers"`

### AI/ML
- `/bmad:research "LLM options"`
- `/bmad:research "embedding models"`
- `/bmad:research "vector databases"`
- `/bmad:research "ML hosting"`

---

## Benefits

**Why This Approach**:
1. **Web Search**: ChatGPT/Claude web have actual web search
2. **Thorough**: Can browse docs, pricing pages, community discussions
3. **Documented**: Findings template ensures structured documentation
4. **Referenced**: Architecture cites research in decisions
5. **Repeatable**: Templates ensure consistency
6. **Preserved**: Research stored in backlog, not lost

**vs. Trying to Research in Claude Code**:
- ❌ Limited web search
- ❌ Can't browse thoroughly
- ❌ Might hallucinate vendor details
- ✅ Good for: Code, architecture design, document generation
- ❌ Bad for: Current vendor pricing, API availability, real-world comparisons

---

## Example: AuricBeat Data Vendors

**Your existing research**: `data-sources-research.md` (18KB)

**With BMAD research system**:

```bash
/bmad:research "data vendors for precious metals"

# Generated prompt includes:
# - AuricBeat context from PRD
# - Requirements (metals, exchanges, freshness)
# - Comparison criteria
# - Cost analysis

User → Copies prompt to ChatGPT
ChatGPT → Web search: Zylalabs, IEX, Polygon, Alpha Vantage, etc.
ChatGPT → Comprehensive comparison with current pricing
User → Copies findings into template
User → Saves to bmad-backlog/research/RESEARCH-data-vendors-findings.md

/bmad:architecture
# → Reads research findings
# → Uses Zylalabs recommendation
# → References research in tech decisions
# → "See RESEARCH-data-vendors-findings.md for vendor analysis"
```

**Result**: Informed architecture decisions with documented rationale.

---

## Update to BMAD Commands

### 7th Command: `/bmad:research`

**Additions**:
1. Add `/bmad:research` to command list
2. Integrate into `/bmad:prd` (detect research needs)
3. Integrate into `/bmad:architecture` (read research findings)
4. Add research folder to backlog structure
5. Update costs: +$0.00 (research done in external AI, free!)

### Updated Command List

**7 BMAD Commands** (was 6):
1. `/bmad:start` - Complete guided workflow
2. `/bmad:brief` - Product brief
3. `/bmad:research` - **NEW** - Research prompt generator
4. `/bmad:prd` - PRD
5. `/bmad:architecture` - Architecture
6. `/bmad:epic` - Single epic
7. `/bmad:index` - Story index

---

## Implementation

### Utility Script

**`research_generator.py`**:
- Generate research prompts with project context
- Generate findings templates
- No GPT-4 calls (just template generation)
- Cost: $0 (no API usage)

### Command

**`bmad-research.md`**:
- Detect research needs from PRD context
- Call research_generator.py
- Present prompt to user
- Guide user to external AI
- Provide template for findings
- Store in Pieces

### Integration

**Update `/bmad:prd`**:
- Before Technical Assumptions
- Detect research needs (APIs, vendors, etc.)
- Offer to generate research prompts
- Pause for research completion
- Resume with findings

**Update `/bmad:architecture`**:
- Check bmad-backlog/research/ folder
- Read all *-findings.md files
- Use recommendations in architecture
- Reference research in Technology Decisions table

---

## Cost Impact

**Research Generation**: $0 (just templates, no GPT-4)
**Research Execution**: $0 (user does it in ChatGPT/Claude web which are already paid/free)
**Total BMAD Cost**: Still ~$0.22 (no change)

**Time Impact**:
- Research prompt generation: ~30 seconds
- User research in web AI: ~10-15 minutes per topic
- Total: +10-45 minutes depending on complexity

**Worth it**: Informed architecture decisions, documented rationale, better vendor choices.

---

## Questions This Addresses

1. **"How do I know which API to use?"**
   → Generate research prompt, get comprehensive comparison

2. **"What's the current pricing for vendors?"**
   → Research in web AI with current web search

3. **"Should I use Stripe or PayPal?"**
   → Research prompt compares both with current pricing

4. **"How do I document vendor research?"**
   → Findings template provides structure

5. **"Where should research live?"**
   → bmad-backlog/research/ folder, referenced in architecture

---

**This completes the BMAD research system design!**
