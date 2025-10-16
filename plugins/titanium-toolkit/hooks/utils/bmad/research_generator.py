#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
BMAD Research Prompt Generator

Generates research prompts and findings templates for technical decisions.
No GPT-4 calls - just template generation (Cost: $0).

Commands:
    prompt <topic> <project_path> [prd_path]    Generate research prompt
    template <topic> <project_path>              Generate findings template

Examples:
    uv run research_generator.py prompt "data vendors" "$(pwd)" "bmad-backlog/prd/prd.md"
    uv run research_generator.py template "data vendors" "$(pwd)"
"""

import sys
import re
from pathlib import Path
from datetime import datetime


def generate_research_prompt(topic: str, project_path: str, prd_path: str = None) -> str:
    """
    Generate research prompt for web AI (ChatGPT/Claude).

    Args:
        topic: Research topic
        project_path: Project directory
        prd_path: Optional path to PRD for context

    Returns:
        Research prompt content
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    topic_slug = topic.lower().replace(' ', '-').replace('/', '-')

    # Read PRD for context if provided
    project_context = ""
    project_name = "New Project"
    requirements_context = ""

    if prd_path and Path(prd_path).exists():
        try:
            with open(prd_path, 'r') as f:
                prd_content = f.read()

            # Extract project name
            match = re.search(r'##\s+(.+?)(?:\s+-|$)', prd_content, re.MULTILINE)
            if match:
                project_name = match.group(1).strip()

            # Extract relevant requirements
            if "data" in topic.lower() or "api" in topic.lower():
                data_section = extract_section(prd_content, "Data Requirements")
                if data_section:
                    requirements_context = f"\n**Project Requirements**:\n{data_section[:500]}"

            if "auth" in topic.lower():
                security_section = extract_section(prd_content, "Security")
                if security_section:
                    requirements_context = f"\n**Security Requirements**:\n{security_section[:500]}"

            project_context = f"\n**Project**: {project_name}\n"

        except Exception:
            pass

    prompt_content = f"""# Research Prompt: {topic}

**Date**: {current_date}
**For**: {project_name}

---

## Instructions

**COPY THIS ENTIRE PROMPT** and paste into:
- ChatGPT (https://chat.openai.com) with GPT-4
- Claude (https://claude.ai) web version

They have web search capabilities for current, accurate information.

---

## Research Request
{project_context}
**Research Topic**: {topic}
{requirements_context}

Please research and provide comprehensive analysis:

---

### 1. Overview

- What options exist for {topic}?
- What are the top 5-7 solutions/vendors/APIs?
- Current market leaders?
- Recent changes in this space? (2024-2025)

---

### 2. Detailed Comparison Table

Create a comprehensive comparison:

| Option | Pricing | Key Features | Pros | Cons | Best For |
|--------|---------|--------------|------|------|----------|
| Option 1: [Name] | [Tiers] | [Top 3-5 features] | [2-3 pros] | [2-3 cons] | [Use case] |
| Option 2: [Name] | | | | | |
| Option 3: [Name] | | | | | |
| Option 4: [Name] | | | | | |
| Option 5: [Name] | | | | | |

---

### 3. Technical Details

For EACH option, provide:

#### [Option Name]

**API Documentation**: [Link to official docs]

**Authentication**:
- Method: API Key | OAuth | JWT | Other
- Security: HTTPS required? Token rotation?

**Rate Limits**:
- Free tier: X requests per minute/hour/day
- Paid tiers: Rate limit increases

**Data Format**:
- Response format: JSON | XML | GraphQL | CSV
- Webhook support: Yes/No
- Streaming: Yes/No

**SDK Availability**:
- Python: [pip package name] - [GitHub link]
- Node.js: [npm package name] - [GitHub link]
- Other languages: [List]

**Code Example**:
```python
# Basic usage example (if available from docs)
```

**Community**:
- GitHub stars: X
- Last updated: Date
- Issues: Open/closed ratio
- Stack Overflow: Questions count

---

### 4. Integration Complexity

For each option, estimate:

**Setup Time**:
- Account creation: X minutes
- API key generation: X minutes
- SDK integration: X hours
- Testing: X hours
**Total**: X hours/days

**Dependencies**:
- Libraries required
- Platform requirements
- Other services needed

**Learning Curve**:
- Documentation quality: Excellent | Good | Fair | Poor
- Tutorials available: Yes/No
- Community support: Active | Moderate | Limited

---

### 5. Recommendations

Based on the project requirements, provide specific recommendations:

**For MVP** (budget-conscious, speed):
- **Recommended**: [Option]
- **Why**: [Rationale]
- **Tradeoffs**: [What you give up]

**For Production** (quality-focused, scalable):
- **Recommended**: [Option]
- **Why**: [Rationale]
- **Cost**: $X/month at scale

**For Enterprise** (feature-complete):
- **Recommended**: [Option]
- **Why**: [Rationale]
- **Cost**: $Y/month

---

### 6. Detailed Cost Analysis

For each option:

#### [Option Name]

**Free Tier**:
- What's included: [Limits]
- Restrictions: [What's missing]
- Good for MVP? Yes/No - [Why]

**Starter/Basic Tier**:
- Price: $X/month
- Includes: [Features and limits]
- Rate limits: X requests/min

**Professional Tier**:
- Price: $Y/month
- Includes: [Features and limits]
- Rate limits: Y requests/min

**Enterprise Tier**:
- Price: $Z/month or Custom
- Includes: [Features]
- SLA: X% uptime

**Estimated Monthly Cost**:
- MVP (low volume): $X-Y
- Production (medium volume): $X-Y
- Scale (high volume): $X-Y

**Hidden Costs**:
- [Overage charges, add-ons, etc.]

---

### 7. Risks & Considerations

For each option, analyze:

**Vendor Lock-in**:
- How easy to migrate away? (Easy/Medium/Hard)
- Data export capabilities
- API compatibility with alternatives

**Data Quality/Reliability**:
- Uptime history (if available)
- Published SLAs
- Known outages or issues
- Data accuracy/freshness

**Compliance & Security**:
- Data residency (US/EU/Global)
- Compliance certifications (SOC 2, GDPR, etc.)
- Security features (encryption, access controls)
- Privacy policy concerns

**Support & Maintenance**:
- Support channels (email, chat, phone)
- Response time SLAs
- Documentation updates
- Release cadence
- Deprecation policy

**Scalability**:
- Auto-scaling capabilities
- Performance at high volume
- Regional availability
- CDN/edge locations

---

### 8. Source Links

Provide current, working links to:

**Official Resources**:
- Homepage: [URL]
- Pricing page: [URL]
- API documentation: [URL]
- Getting started guide: [URL]
- Status page: [URL]

**Developer Resources**:
- GitHub repository: [URL]
- SDK documentation: [URL]
- API reference: [URL]
- Code examples: [URL]

**Community**:
- Community forum: [URL]
- Discord/Slack: [URL]
- Stack Overflow tag: [URL]
- Twitter/X: [Handle]

**Reviews & Comparisons**:
- G2/Capterra reviews: [URL]
- Comparison articles: [URL]
- User testimonials: [URL]
- Case studies: [URL]

---

## Deliverable

Please structure your response with clear sections matching the template above.

This research will inform our architecture decisions and be documented for future reference.

Thank you!

---

**After completing research**:
1. Copy findings into template: bmad-backlog/research/RESEARCH-{topic_slug}-findings.md
2. Return to Claude Code
3. Continue with /bmad:architecture (will use your research)
"""

    # Save prompt
    prompt_path = Path(project_path) / "bmad-backlog" / "research" / f"RESEARCH-{topic_slug}-prompt.md"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)

    with open(prompt_path, 'w') as f:
        f.write(prompt_content)

    return prompt_content


def generate_findings_template(topic: str, project_path: str) -> str:
    """
    Generate findings template for documenting research.

    Args:
        topic: Research topic
        project_path: Project directory

    Returns:
        Template content
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    topic_slug = topic.lower().replace(' ', '-').replace('/', '-')

    template_content = f"""# Research Findings: {topic}

**Date**: {current_date}
**Researcher**: [Your Name]
**Status**: Draft

---

## Research Summary

**Question**: What {topic} should we use?

**Recommendation**: [Chosen option and brief rationale]

**Confidence**: High | Medium | Low

**Decision Date**: [When decision was made]

---

## Options Evaluated

### Option 1: [Name]

**Overview**:
[1-2 sentence description of what this is]

**Pricing**:
- Free tier: [Details or N/A]
- Starter tier: $X/month - [What's included]
- Pro tier: $Y/month - [What's included]
- Enterprise: $Z/month or Custom
- **Estimated cost for our MVP**: $X/month

**Key Features**:
- [Feature 1]
- [Feature 2]
- [Feature 3]
- [Feature 4]

**Pros**:
- [Pro 1]
- [Pro 2]
- [Pro 3]

**Cons**:
- [Con 1]
- [Con 2]
- [Con 3]

**Technical Details**:
- API Type: REST | GraphQL | WebSocket | Other
- Authentication: API Key | OAuth | JWT | Other
- Rate Limits: X requests per minute/hour
- Data Format: JSON | XML | CSV | Other
- SDKs: Python ([package]), Node.js ([package]), Other
- Latency: Typical response time
- Uptime SLA: X%

**Documentation**: [Link]

**Community**:
- GitHub Stars: X
- Last Update: [Date]
- Active Development: Yes/No

---

### Option 2: [Name]

[Same structure as Option 1]

---

### Option 3: [Name]

[Same structure as Option 1]

---

### Option 4: [Name]

[Same structure as Option 1 - if evaluated]

---

## Comparison Matrix

| Criteria | Option 1 | Option 2 | Option 3 | Winner |
|----------|----------|----------|----------|--------|
| **Cost (MVP)** | $X/mo | $Y/mo | $Z/mo | [Option] |
| **Cost (Production)** | $X/mo | $Y/mo | $Z/mo | [Option] |
| **Features** | X/10 | Y/10 | Z/10 | [Option] |
| **API Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | [Option] |
| **Documentation** | Excellent | Good | Fair | [Option] |
| **Community** | Large | Medium | Small | [Option] |
| **Ease of Use** | Easy | Medium | Complex | [Option] |
| **Scalability** | High | Medium | High | [Option] |
| **Vendor Lock-in Risk** | Low | Medium | High | [Option] |
| **Overall Score** | X/10 | Y/10 | Z/10 | **[Winner]** |

---

## Final Recommendation

**Chosen**: [Option X]

**Rationale**:
1. [Primary reason - e.g., best balance of cost and features]
2. [Secondary reason - e.g., excellent documentation]
3. [Tertiary reason - e.g., active community]

**For MVP**:
- [Why this works for MVP]
- Cost: $X/month
- Timeline: [Can start immediately / Need 1 week setup]

**For Production**:
- [Scalability considerations]
- Cost at scale: $Y/month
- Migration path: [If we outgrow this]

**Implementation Priority**: MVP | Phase 2 | Future

---

## Implementation Plan

### Setup Steps

1. [Step 1 - e.g., Create account at vendor.com]
2. [Step 2 - e.g., Generate API key]
3. [Step 3 - e.g., Install SDK: pip install package]
4. [Step 4 - e.g., Test connection]
5. [Step 5 - e.g., Implement in production code]

**Estimated Setup Time**: X hours

### Configuration Required

**Environment Variables**:
```bash
# Add to .env.example
{{VENDOR}}_API_KEY=your_key_here
{{VENDOR}}_BASE_URL=https://api.vendor.com
```

**Code Configuration**:
```python
# Example configuration
from {{package}} import Client

client = Client(api_key=os.getenv('{{VENDOR}}_API_KEY'))
```

### Basic Usage Example

```python
# Example usage from documentation
{{code example if available}}
```

---

## Cost Projection

**Monthly Cost Breakdown**:

**MVP** (estimated volume):
- Base fee: $X
- Usage costs: $Y
- **Total**: $Z/month

**Production** (estimated volume):
- Base fee: $X
- Usage costs: $Y
- **Total**: $Z/month

**At Scale** (estimated volume):
- Base fee: $X
- Usage costs: $Y
- **Total**: $Z/month

**Cost Optimization**:
- [Strategy 1 to reduce costs]
- [Strategy 2]

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Vendor increases pricing | Medium | Medium | [Monitor pricing, have backup option] |
| Service downtime | High | Low | [Implement fallback, cache data] |
| Rate limit hit | Medium | Medium | [Implement rate limiting, queue requests] |
| Data quality issues | High | Low | [Validation layer, monitoring] |
| Vendor shutdown | High | Low | [Data export plan, alternative ready] |

---

## Testing Checklist

- [ ] Create account and obtain credentials
- [ ] Test API in development
- [ ] Verify rate limits and error handling
- [ ] Test with production-like volume
- [ ] Set up monitoring and alerts
- [ ] Document API integration in code
- [ ] Add to .env.example
- [ ] Create fallback/error handling
- [ ] Test cost with real usage
- [ ] Review security and compliance

---

## References

**Official Documentation**:
- Website: [URL]
- Pricing: [URL]
- API Docs: [URL]
- Getting Started: [URL]
- Status Page: [URL]

**Community Resources**:
- GitHub: [URL]
- Discord/Slack: [URL]
- Stack Overflow: [URL with tag]

**Comparison Articles**:
- [Article 1 title]: [URL]
- [Article 2 title]: [URL]

**User Reviews**:
- G2: [URL]
- Reddit discussions: [URLs]

---

## Next Steps

1. ✅ Research complete
2. Review findings with team (if applicable)
3. Make final decision on [chosen option]
4. Update bmad-backlog/prd/prd.md Technical Assumptions
5. Reference in bmad-backlog/architecture/architecture.md
6. Add to implementation backlog

---

**Status**: ✅ Research Complete | ⏳ Awaiting Decision | ❌ Needs More Research

**Recommendation**: [Final recommendation]

---

*This document was generated from research conducted using web-based AI.*
*Fill in all sections with findings from your research.*
*Save this file when complete - it will be referenced during architecture generation.*
"""

    # Save template
    template_path = Path(project_path) / "bmad-backlog" / "research" / f"RESEARCH-{topic_slug}-findings.md"
    template_path.parent.mkdir(parents=True, exist_ok=True)

    with open(template_path, 'w') as f:
        f.write(template_content)

    return template_content


def extract_section(content: str, section_header: str) -> str:
    """Extract section from markdown document."""
    lines = content.split('\n')
    section_lines = []
    in_section = False

    for line in lines:
        if section_header.lower() in line.lower() and line.startswith('#'):
            in_section = True
            continue
        elif in_section and line.startswith('#') and len(line.split()) > 1:
            # New section started
            break
        elif in_section:
            section_lines.append(line)

    return '\n'.join(section_lines).strip()


def main():
    """CLI interface for research prompt generation."""

    if len(sys.argv) < 4:
        print("Usage: research_generator.py <command> <topic> <project_path> [prd_path]", file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        print("  prompt <topic> <project_path> [prd_path]   Generate research prompt", file=sys.stderr)
        print("  template <topic> <project_path>            Generate findings template", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print('  uv run research_generator.py prompt "data vendors" "$(pwd)" "bmad-backlog/prd/prd.md"', file=sys.stderr)
        print('  uv run research_generator.py template "hosting platforms" "$(pwd)"', file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    topic = sys.argv[2]
    project_path = sys.argv[3]
    prd_path = sys.argv[4] if len(sys.argv) > 4 else None

    topic_slug = topic.lower().replace(' ', '-').replace('/', '-')

    try:
        if command == "prompt":
            content = generate_research_prompt(topic, project_path, prd_path)
            print(f"✅ Research prompt generated: bmad-backlog/research/RESEARCH-{topic_slug}-prompt.md")

        elif command == "template":
            content = generate_findings_template(topic, project_path)
            print(f"✅ Findings template generated: bmad-backlog/research/RESEARCH-{topic_slug}-findings.md")

        else:
            print(f"Error: Unknown command: {command}", file=sys.stderr)
            print("Valid commands: prompt, template", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
