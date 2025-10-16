---
description: Generate research prompts for technical decisions
---

# BMAD Research - Generate Research Prompts

You are helping the user research technical decisions by generating comprehensive research prompts for web-based AI (ChatGPT, Claude web) which have web search capabilities.

## Purpose

Generate structured research prompts that users can copy to ChatGPT/Claude web to research:
- API vendors and data sources
- Authentication providers
- Hosting platforms
- Payment processors
- Third-party integrations
- Technology stack options

Results are documented in structured templates and referenced during architecture generation.

## When to Use

**During BMAD workflow**:
- After PRD mentions external APIs/vendors
- Before architecture generation
- When technical decisions need research

**Standalone**:
- Evaluating vendor options
- Comparing technologies
- Cost analysis
- Technical due diligence

## Process

### Step 1: Identify Research Topic

**If user provided topic**:
```bash
# User ran: /bmad:research "data vendors for precious metals"
```
- Topic = "data vendors for precious metals"

**If no topic**:
- Ask: "What do you need to research?"
- Show common topics:
  ```
  Common research topics:
  1. Data vendors/APIs
  2. Hosting platforms (Railway, Vercel, GCP, etc.)
  3. Authentication providers (Clerk, Auth0, custom, etc.)
  4. Payment processors (Stripe, PayPal, etc.)
  5. AI/ML options (OpenAI, Anthropic, self-hosted)
  6. Database options
  7. Other (specify)

  Topic:
  ```

### Step 2: Gather Context from PRD

**If PRD exists**:
```bash
Read bmad-backlog/prd/prd.md
```

Extract relevant context:
- What features need this research?
- What are the constraints? (budget, performance)
- Any technical preferences mentioned?

**If no PRD**:
- Use topic only
- Generate generic research prompt
- Note: "Research will be more focused with a PRD"

### Step 3: Generate Research Prompt

Create comprehensive prompt for web AI.

**Topic slug**: Convert topic to filename-safe string
```python
topic_slug = topic.lower().replace(' ', '-').replace('/', '-')
# "data vendors for precious metals" → "data-vendors-for-precious-metals"
```

**Save to**: `bmad-backlog/research/RESEARCH-{topic_slug}-prompt.md`

**Prompt content**:
```markdown
# Research Prompt: {Topic}

**COPY THIS ENTIRE PROMPT** and paste into ChatGPT (GPT-4) or Claude (web).
They have web search and can provide current, comprehensive research.

---

## Research Request

**Project**: {{project name from PRD or "New Project"}}

**Research Topic**: {{topic}}

**Context**:
{{Extract from PRD:
- What features need this
- Performance requirements
- Budget constraints
- Technical preferences}}

---

## What I Need

Please research and provide:

### 1. Overview
- What options exist for {{topic}}?
- What are the top 5-7 solutions/vendors/APIs?
- Current market leaders?

### 2. Comparison Table

Create a detailed comparison table:

| Option | Pricing | Key Features | Pros | Cons | Best For |
|--------|---------|--------------|------|------|----------|
| Option 1 | | | | | |
| Option 2 | | | | | |
| Option 3 | | | | | |

### 3. Technical Details

For each option, provide:
- **API Documentation**: Official docs link
- **Authentication**: API key, OAuth, etc.
- **Rate Limits**: Requests per minute/hour
- **Data Format**: JSON, XML, GraphQL, etc.
- **SDKs**: Python, Node.js, etc. with links
- **Code Examples**: If available
- **Community**: GitHub stars, Stack Overflow activity

### 4. Integration Complexity

For each option:
- **Estimated Setup Time**: Hours/days
- **Dependencies**: What else is needed
- **Learning Curve**: Easy/Medium/Hard
- **Documentation Quality**: Excellent/Good/Poor
- **Community Support**: Active/Moderate/Limited

### 5. Recommendations

Based on my project requirements:
{{List key requirements}}

Which option would you recommend and why?

Provide recommendation for:
- **MVP**: Best for getting started quickly
- **Production**: Best for long-term reliability
- **Budget**: Most cost-effective option

### 6. Cost Analysis

For each option, provide:

**Free Tier**:
- What's included
- Limitations
- Good for MVP? (yes/no)

**Paid Tiers**:
- Tier names and pricing
- What each tier includes
- Rate limit increases

**Estimated Monthly Cost**:
- MVP (low volume): $X-Y
- Production (medium volume): $X-Y
- Scale (high volume): $X-Y

### 7. Risks & Considerations

For each option:
- **Vendor Lock-in**: How easy to migrate away?
- **Data Quality**: Accuracy, freshness, reliability
- **Compliance**: Regional restrictions, data governance
- **Uptime/SLA**: Published SLAs, historical uptime
- **Support**: Response times, support channels

### 8. Source Links

Provide links to:
- Official website
- Pricing page
- API documentation
- Getting started guide
- Community forums/Discord
- Comparison articles/reviews
- GitHub repositories (if applicable)

---

## Deliverable Format

Please structure your response to match the sections above for easy copy/paste into my findings template.

Thank you!
```

**Write this to file**: bmad-backlog/research/RESEARCH-{topic_slug}-prompt.md

### Step 4: Generate Findings Template

Create structured template for documenting research.

**Save to**: `bmad-backlog/research/RESEARCH-{topic_slug}-findings.md`

**Template content**:
```markdown
# Research Findings: {Topic}

**Date**: {current date}
**Researcher**: {user name or TBD}
**Status**: Draft

---

## Research Summary

**Question**: {what was researched}

**Recommendation**: {chosen option and why}

**Confidence**: High | Medium | Low

---

## Options Evaluated

### Option 1: {Name}

**Overview**:

**Pricing**:
- Free tier:
- Paid tiers:
- Estimated cost for MVP: $X/month
- Estimated cost for Production: $Y/month

**Features**:
-
-

**Pros**:
-
-

**Cons**:
-
-

**Technical Details**:
- API: REST | GraphQL | WebSocket
- Authentication:
- Rate limits:
- Data format:
- SDKs:

**Documentation**: {link}

**Community**: {GitHub stars, activity}

---

### Option 2: {Name}

[Same structure]

---

### Option 3: {Name}

[Same structure]

---

## Comparison Matrix

| Criteria | Option 1 | Option 2 | Option 3 | Winner |
|----------|----------|----------|----------|--------|
| Cost (MVP) | $X/mo | $Y/mo | $Z/mo | |
| Features | X | Y | Z | |
| API Quality | {rating} | {rating} | {rating} | |
| Documentation | {rating} | {rating} | {rating} | |
| Community | {rating} | {rating} | {rating} | |
| Ease of Use | {rating} | {rating} | {rating} | |
| **Overall** | | | | **{Winner}** |

---

## Recommendation

**Chosen**: {Option X}

**Rationale**:
1. {Reason 1}
2. {Reason 2}
3. {Reason 3}

**For MVP**: {Why this is good for MVP}

**For Production**: {Scalability considerations}

**Implementation Priority**: {When to implement - MVP/Phase 2/etc}

---

## Implementation Notes

**Setup Steps**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Configuration**:
```
{Config example or .env variables needed}
```

**Code Example**:
```{language}
{Basic usage example if available}
```

---

## Cost Projection

**MVP** (low volume):
- Monthly cost: $X
- Included: {what's covered}

**Production** (medium volume):
- Monthly cost: $Y
- Growth: {how costs scale}

**At Scale** (high volume):
- Monthly cost: $Z
- Optimization: {cost reduction strategies}

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| {Risk 1} | High/Med/Low | High/Med/Low | {How to mitigate} |
| {Risk 2} | High/Med/Low | High/Med/Low | {How to mitigate} |

---

## Implementation Checklist

- [ ] Create account/sign up
- [ ] Obtain API key/credentials
- [ ] Test in development environment
- [ ] Review pricing and set cost alerts
- [ ] Document integration in architecture
- [ ] Add credentials to .env.example
- [ ] Test error handling and rate limits

---

## References

- Official Website: {link}
- Pricing Page: {link}
- API Docs: {link}
- Getting Started: {link}
- Community: {link}
- Comparison Articles: {links}

---

## Next Steps

1. ✅ Research complete
2. Review findings with team (if applicable)
3. Make final decision on {chosen option}
4. Update PRD Technical Assumptions with this research
5. Reference in Architecture document generation

---

**Status**: ✅ Research Complete | ⏳ Awaiting Decision | ❌ Needs More Research

---

*Fill in this template with findings from ChatGPT/Claude web research.*
*Save this file when complete.*
*Architecture generation will reference this research.*
```

### Step 5: Present to User

```
📋 Research Prompt and Template Generated!

I've created two files:

📄 1. Research Prompt
Location: bmad-backlog/research/RESEARCH-{{topic}}-prompt.md

This contains a comprehensive research prompt with your project context.

📄 2. Findings Template
Location: bmad-backlog/research/RESEARCH-{{topic}}-findings.md

This is a structured template for documenting research results.

---

🔍 Next Steps:

1. Open: bmad-backlog/research/RESEARCH-{{topic}}-prompt.md

2. **Copy the entire prompt**

3. Open ChatGPT (https://chat.openai.com) or Claude (https://claude.ai)
   → They have web search for current info!

4. Paste the prompt

5. Wait for comprehensive research (5-10 minutes)

6. Copy findings into template:
   bmad-backlog/research/RESEARCH-{{topic}}-findings.md

7. Save the template file

8. Come back and run:
   - /bmad:prd (if updating PRD)
   - /bmad:architecture (I'll use your research!)

---

Would you like me to show you the research prompt now?
```

**If user says yes**:
- Display the prompt file content
- User can copy directly

**If user says no**:
- "The files are ready when you need them!"

### Step 6: Store in Pieces

```
mcp__Pieces__create_pieces_memory(
  summary_description: "Research prompt for {{topic}}",
  summary: "Generated research prompt for {{topic}}. User will research: {{what to evaluate}}. Purpose: {{why needed for project}}. Findings will inform: {{PRD technical assumptions / Architecture tech stack decisions}}. Template provided for structured documentation.",
  files: [
    "bmad-backlog/research/RESEARCH-{{topic}}-prompt.md",
    "bmad-backlog/research/RESEARCH-{{topic}}-findings.md"
  ],
  project: "$(pwd)"
)
```

## Integration with Other Commands

### Called from `/bmad:prd`

When PRD generation detects research needs:
```
Claude: "I see you need data vendors. Generate research prompt?"
User: "yes"

[Runs /bmad:research "data vendors"]

Claude: "Research prompt generated. Please complete research and return when done."

[User researches, fills template]

User: "Research complete"

Claude: "Great! Continuing PRD with your findings..."
[Reads RESEARCH-data-vendors-findings.md]
[Incorporates into PRD Technical Assumptions]
```

### Used by `/bmad:architecture`

Architecture generation automatically checks for research:
```bash
ls bmad-backlog/research/RESEARCH-*-findings.md
```

If found:
- Read all findings
- Use recommendations in tech stack
- Reference research in Technology Decisions table
- Include costs from research in cost estimates

## Voice Feedback

Voice announces:
- "Research prompt generated" (when done)
- "Ready for external research" (reminder)

## Example Topics

**Data & APIs**:
- "data vendors for {domain}"
- "API marketplaces"
- "real-time data feeds"

**Infrastructure**:
- "hosting platforms for {tech stack}"
- "CI/CD providers"
- "monitoring solutions"
- "CDN providers"

**Third-Party Services**:
- "authentication providers"
- "payment processors"
- "email services"
- "SMS providers"

**AI/ML**:
- "LLM hosting options"
- "embedding models"
- "vector databases"

## Important Guidelines

**Always**:
- ✅ Include project context in prompt
- ✅ Generate findings template
- ✅ Guide user to web AI
- ✅ Store prompts in Pieces
- ✅ Explain next steps clearly

**Never**:
- ❌ Try to research in Claude Code (limited web search)
- ❌ Hallucinate vendor pricing (use web AI)
- ❌ Skip generating findings template
- ❌ Forget project context in prompt

## Why This Approach

**Claude Code limitations**:
- Limited web search
- Can't browse vendor pricing pages
- May hallucinate current details

**ChatGPT/Claude Web strengths**:
- Actual web search
- Can browse documentation
- Current pricing information
- Community discussions
- Up-to-date comparisons

**Best of both worlds**:
- Claude Code: Generate prompts, manage workflow
- Web AI: Thorough research with search
- Result: Informed decisions, documented rationale

**Cost**: $0 (no API calls, just template generation)

---

**This command enables informed technical decisions with documented research!**
