---
name: bmad-prd
description: Create Product Requirements Documents (PRDs), Architecture Documents, Epics, and User Stories using the BMAD (Breakthrough Method for Agile AI Driven Development) methodology. Use when user requests PRDs, architecture docs, epics, stories, or product planning documentation that follows structured agile practices with deep context and detail.
---

# BMAD Method: PRD, Architecture, Epic, and Story Creation

This skill implements the BMAD (Breakthrough Method for Agile AI Driven Development) approach to creating high-quality, context-rich product requirements documents, architecture documents, epics, and user stories.

## Core Principles

1. **Human-in-the-Loop Refinement**: Work collaboratively with the user, asking clarifying questions
2. **Context-Rich Documentation**: Provide deep context, not generic AI-generated content
3. **Hyper-Detailed Stories**: Each story should contain everything needed for implementation
4. **No Generic Output**: Avoid bland, average responses - dig deep and be specific

## Document Hierarchy

```
Project Brief (optional)
    ↓
PRD (Product Requirements Document)
    ↓
Architecture Document
    ↓
Epics (High-level feature groups: #1.0, #2.0, etc.)
    ↓
User Stories (Detailed stories: 1.1, 1.2, 2.1, 2.2, etc.)
```

## Creating a Project Brief (Optional but Recommended)

### Purpose
A project brief provides strategic context before diving into detailed requirements.

### Structure
```markdown
# Project Brief: [Project Name]

## Executive Summary
[2-3 paragraphs: What is this? Why are we building it?]

## Market Context
- Target Audience
- Market Opportunity
- Competitive Landscape

## Business Objectives
- Primary Goals
- Success Criteria
- Key Metrics

## Constraints & Assumptions
- Budget/Timeline
- Technical Constraints
- Known Limitations

## Stakeholders
- Key Decision Makers
- Primary Users
- Technical Team
```

### Best Practices for Project Briefs
- Keep it concise (2-5 pages max)
- Focus on WHY before WHAT
- Include competitive analysis if relevant
- Reference supporting documents (don't inline massive content)
- Update as understanding evolves

## Creating a PRD (Product Requirements Document)

### Purpose
The PRD is the single source of truth for what will be built. It bridges business needs and technical implementation.

### PRD Structure

```markdown
# Product Requirements Document: [Product Name]

## 1. Goals and Background Context

### Problem Statement
[Describe the core problem being solved]

### Vision
[High-level vision for the product]

### Success Criteria
[How will we measure success?]

### Target Users
[Who are we building this for?]

### Out of Scope
[What are we explicitly NOT building in this version?]

## 2. Functional Requirements (FRs)

### FR-1: [Requirement Name]
**Description**: [Detailed description]
**Priority**: [Must Have / Should Have / Nice to Have]
**User Story Reference**: [Links to relevant epics/stories]

[Repeat for each functional requirement]

## 3. Non-Functional Requirements (NFRs)

### Performance
- Response time targets
- Throughput requirements
- Scalability goals

### Security
- Authentication/authorization requirements
- Data protection needs
- Compliance requirements

### Reliability
- Uptime targets
- Error handling
- Backup/recovery

### Usability
- Accessibility standards
- Browser/device support
- User experience goals

### Technical Constraints
- Technology stack requirements
- Integration requirements
- Infrastructure needs

## 4. Epics and User Stories (High-Level)

### Epic #1.0: [Epic Name]
**Description**: [High-level description of this feature area]
**Business Value**: [Why is this important?]
**Stories**:
- 1.1: [Brief story description]
- 1.2: [Brief story description]
- 1.3: [Brief story description]

### Epic #2.0: [Epic Name]
[Repeat structure]

## 5. User Interface Design Goals (if applicable)

### Design Principles
[Key UI/UX principles]

### Key Flows
[Critical user journeys]

### Design References
[Mockups, wireframes, design system references]

## 6. Success Metrics and KPIs

### Primary Metrics
[How will we measure success?]

### Secondary Metrics
[Additional success indicators]

### Instrumentation Needs
[What analytics/logging do we need?]

## 7. Dependencies and Risks

### External Dependencies
[Third-party services, APIs, etc.]

### Technical Risks
[Known technical challenges]

### Mitigation Strategies
[How we'll address risks]

## 8. Release Strategy

### MVP (Minimum Viable Product)
[What's included in first release?]

### Future Phases
[What comes next?]

### Rollout Plan
[How will we deploy?]
```

### PRD Best Practices

1. **Start with Discovery Questions**
   - What problem are we solving?
   - Who are the users?
   - What are the business goals?
   - What are the constraints?
   - What does success look like?

2. **Be Specific, Not Generic**
   - Avoid vague language
   - Include concrete examples
   - Reference specific use cases
   - Provide context and rationale

3. **Collaborate and Iterate**
   - Ask clarifying questions
   - Challenge assumptions
   - Validate understanding
   - Refine based on feedback

4. **Make It Actionable**
   - Clear, testable requirements
   - Prioritized features
   - Defined success criteria
   - Traceable to business goals

5. **Include Context for Decision-Making**
   - Why decisions were made
   - Alternatives considered
   - Tradeoffs accepted
   - Assumptions documented

## Creating Architecture Documents

### Purpose
The Architecture Document translates the PRD into a technical blueprint. It defines HOW the system will be built, what technologies will be used, and how components will interact.

### Architecture Document Structure

```markdown
# Architecture Document: [Product Name]

## 1. Executive Summary

### Overview
[High-level architectural approach and key decisions]

### Architecture Principles
[Core principles guiding this architecture]
- Scalability
- Maintainability
- Security-first
- Cost-effectiveness
[etc.]

### Key Technologies
[Major technology choices and why]

## 2. System Context

### System Boundaries
[What's inside vs outside the system]

### External Dependencies
[Third-party services, APIs, external systems]

### Integration Points
[How this system connects with other systems]

### Users and Actors
[Who/what interacts with the system]

## 3. High-Level Architecture

### Architecture Diagram
[ASCII diagram or reference to diagram file]
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│      Load Balancer              │
└──────┬──────────────────────┘
       │
┌──────▼──────────┐  ┌─────────────┐
│  App Server     │──│   Cache     │
└──────┬──────────┘  └─────────────┘
       │
┌──────▼──────────┐
│   Database      │
└─────────────────┘
```

### Architecture Pattern
[MVC, Microservices, Event-Driven, Layered, etc.]

### Component Overview
[Major system components and their responsibilities]

## 4. Technology Stack

### Frontend
- **Framework**: [React, Vue, Angular, etc.]
- **State Management**: [Redux, Zustand, Context API, etc.]
- **Styling**: [Tailwind, CSS Modules, styled-components, etc.]
- **Build Tools**: [Vite, Webpack, etc.]
- **Testing**: [Jest, Vitest, Cypress, etc.]

**Rationale**: [Why these choices?]

### Backend
- **Language**: [Node.js, Python, Go, etc.]
- **Framework**: [Express, FastAPI, Django, etc.]
- **API Style**: [REST, GraphQL, gRPC, etc.]
- **Authentication**: [JWT, OAuth2, Session-based, etc.]
- **Testing**: [Jest, pytest, etc.]

**Rationale**: [Why these choices?]

### Database
- **Primary Database**: [PostgreSQL, MongoDB, MySQL, etc.]
- **Caching Layer**: [Redis, Memcached, etc.]
- **Search Engine**: [Elasticsearch, Algolia, etc.] (if applicable)
- **Message Queue**: [RabbitMQ, Kafka, SQS, etc.] (if applicable)

**Rationale**: [Why these choices?]

### Infrastructure
- **Hosting**: [AWS, GCP, Azure, Vercel, etc.]
- **Container Orchestration**: [Docker, Kubernetes, ECS, etc.]
- **CI/CD**: [GitHub Actions, GitLab CI, Jenkins, etc.]
- **Monitoring**: [DataDog, New Relic, Prometheus, etc.]
- **Logging**: [CloudWatch, ELK Stack, etc.]

**Rationale**: [Why these choices?]

### Third-Party Services
- **Payment**: [Stripe, PayPal, etc.]
- **Email**: [SendGrid, AWS SES, etc.]
- **File Storage**: [S3, Cloudinary, etc.]
- **Analytics**: [Google Analytics, Mixpanel, etc.]
[etc.]

## 5. Data Architecture

### Data Model Overview
[High-level description of key entities and relationships]

### Entity Relationship Diagram
```
User ──< UserProfile
  │
  │
  └──< Order ──< OrderItem >── Product
         │
         └──< Payment
```

### Key Entities

#### User
```typescript
interface User {
  id: string;
  email: string;
  passwordHash: string;
  createdAt: Date;
  updatedAt: Date;
  role: 'admin' | 'user';
}
```

[Repeat for each key entity]

### Data Flow
[How data moves through the system]

1. User submits form
2. API validates data
3. Data stored in primary database
4. Cache updated
5. Event published to message queue
6. Background job processes event

### Data Storage Strategy
- **Hot Data**: [Redis cache, short TTL]
- **Warm Data**: [Primary database]
- **Cold Data**: [S3 archival storage]

### Backup and Recovery
- **Backup Frequency**: [Daily automated backups]
- **Retention**: [30 days]
- **Recovery Time Objective (RTO)**: [4 hours]
- **Recovery Point Objective (RPO)**: [1 hour]

## 6. API Design

### API Architecture
[REST, GraphQL, gRPC, etc.]

### Authentication & Authorization
- **Method**: [JWT tokens, OAuth2, API keys]
- **Token Expiry**: [15 minutes access, 7 days refresh]
- **Permission Model**: [RBAC, ABAC, etc.]

### API Endpoints

#### User Management
```http
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
GET    /api/v1/users/:id
PUT    /api/v1/users/:id
DELETE /api/v1/users/:id
```

[Document key endpoints with request/response examples]

#### Example: User Registration
```http
POST /api/v1/auth/register

Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

Response (201):
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-10-16T10:30:00Z"
}

Error Response (400):
{
  "error": "INVALID_EMAIL",
  "message": "Email address is invalid"
}
```

### API Versioning Strategy
[How APIs will be versioned: URL, header, etc.]

### Rate Limiting
- **Anonymous**: 100 requests/hour
- **Authenticated**: 1000 requests/hour
- **Premium**: 10000 requests/hour

## 7. Security Architecture

### Security Principles
[Security-first mindset, defense in depth, etc.]

### Authentication
[How users authenticate]

### Authorization
[How permissions are enforced]

### Data Encryption
- **In Transit**: TLS 1.3
- **At Rest**: AES-256 encryption
- **Sensitive Data**: Additional field-level encryption

### Security Measures
- **SQL Injection**: Parameterized queries, ORM
- **XSS**: Content Security Policy, input sanitization
- **CSRF**: CSRF tokens, SameSite cookies
- **Secrets Management**: AWS Secrets Manager / Vault
- **DDoS Protection**: CloudFlare, rate limiting

### Compliance
[GDPR, HIPAA, SOC2, etc. requirements]

## 8. Performance & Scalability

### Performance Requirements
- **API Response Time**: < 200ms (p95)
- **Page Load Time**: < 2s (p95)
- **Database Query Time**: < 50ms (p95)
- **Time to First Byte**: < 100ms

### Scaling Strategy

#### Horizontal Scaling
[How system scales out]
- Load balancer distributes traffic
- Stateless application servers
- Database read replicas

#### Vertical Scaling
[When/how to scale up]

#### Auto-scaling Rules
- **Scale Out**: CPU > 70% for 5 minutes
- **Scale In**: CPU < 30% for 10 minutes
- **Min Instances**: 2
- **Max Instances**: 10

### Caching Strategy
- **Browser Cache**: Static assets (1 year)
- **CDN Cache**: Images, CSS, JS (1 week)
- **API Cache**: Redis (5 minutes)
- **Database Cache**: Query results (varies)

### Performance Optimization
- **Database**: Indexing strategy, query optimization
- **Frontend**: Code splitting, lazy loading, image optimization
- **Backend**: Connection pooling, async processing
- **Network**: CDN, compression, HTTP/2

## 9. Reliability & Monitoring

### Availability Target
- **SLA**: 99.9% uptime (8.7 hours downtime/year)
- **Monitoring**: 24/7 automated monitoring
- **Alerting**: PagerDuty for critical issues

### Error Handling
- **User-Facing Errors**: Friendly messages, no stack traces
- **API Errors**: Consistent error format
- **Logging**: Structured logs to centralized system
- **Error Tracking**: Sentry for exception tracking

### Health Checks
```http
GET /health
Response: { "status": "healthy", "version": "1.2.3" }

GET /health/ready
Response: { "database": "ok", "cache": "ok", "queue": "ok" }
```

### Monitoring Metrics
- **Application**: Error rate, response time, throughput
- **Infrastructure**: CPU, memory, disk, network
- **Business**: User signups, conversion rate, revenue
- **Custom**: Feature usage, queue depth, etc.

### Alerting Thresholds
- **Critical**: Error rate > 1%, response time > 2s
- **Warning**: Error rate > 0.1%, response time > 1s
- **Info**: Deployments, configuration changes

## 10. Deployment Architecture

### Environments
1. **Development**: Local developer machines
2. **Staging**: Mirrors production, for testing
3. **Production**: Live environment

### CI/CD Pipeline
```
Code Push → Tests → Build → Deploy to Staging → Manual Approval → Deploy to Production
```

### Deployment Strategy
- **Method**: Blue-green deployment / Rolling deployment
- **Rollback Plan**: Automated rollback on health check failure
- **Database Migrations**: Run before deployment, backwards compatible

### Infrastructure as Code
- **Tool**: Terraform / CloudFormation
- **Version Control**: All infrastructure in Git
- **Environment Parity**: Staging mirrors production

## 11. Technical Constraints & Decisions

### Technology Constraints
[Existing systems, team expertise, licensing, etc.]

### Key Technical Decisions

#### Decision: Use PostgreSQL over MongoDB
**Context**: Need for complex queries and data relationships
**Options Considered**: PostgreSQL, MongoDB, MySQL
**Decision**: PostgreSQL
**Rationale**: ACID compliance, robust querying, team expertise
**Tradeoffs**: Slightly more complex schema changes

[Repeat for each major decision]

### Assumptions
[Technical assumptions being made]

### Risks & Mitigation
[Technical risks and how to address them]

## 12. Development Guidelines

### Code Organization
[Folder structure, naming conventions]

### Coding Standards
- **Style Guide**: [ESLint config, Prettier, etc.]
- **Testing Requirements**: [80% coverage minimum]
- **Code Review**: [Required before merge]
- **Documentation**: [JSDoc for public APIs]

### Git Workflow
- **Branching**: Git Flow / Trunk-based
- **Commit Messages**: Conventional Commits
- **PR Requirements**: Tests passing, reviewed, no conflicts

### Development Environment Setup
[How developers get started]

## 13. Testing Strategy

### Testing Pyramid
- **Unit Tests**: 70% coverage
- **Integration Tests**: 20% coverage
- **E2E Tests**: 10% coverage

### Test Types
- **Unit**: Individual functions/components
- **Integration**: API endpoints, database interactions
- **E2E**: Critical user journeys
- **Performance**: Load testing with k6/JMeter
- **Security**: OWASP Top 10, penetration testing

### Test Environments
- **Local**: Developer machines
- **CI**: Automated on every commit
- **Staging**: Full test suite before production

## 14. Future Considerations

### Technical Debt
[Known technical debt and plans to address]

### Scalability Roadmap
[How architecture will evolve as system grows]

### Feature Roadmap Impact
[How planned features will affect architecture]

### Technology Evolution
[Planned technology updates/migrations]

## 15. Appendices

### Glossary
[Technical terms and definitions]

### References
- [Link to PRD]
- [Link to API documentation]
- [Link to design system]
- [External documentation]

### Decision Log
[Record of all significant architectural decisions]

### Open Questions
[Architectural questions that need resolution]
```

### Architecture Document Best Practices

1. **Keep It Updated**
   - Architecture evolves with the system
   - Update as decisions are made
   - Version control all changes

2. **Be Pragmatic**
   - Choose "boring" technology when possible
   - Over-engineering is a risk
   - Start simple, add complexity as needed

3. **Document Decisions**
   - Record why decisions were made
   - Document alternatives considered
   - Note tradeoffs accepted

4. **Think About Operations**
   - How will it be deployed?
   - How will it be monitored?
   - How will it be debugged?

5. **Consider the Team**
   - Use technologies team knows
   - Document unfamiliar patterns
   - Plan for knowledge transfer

6. **Security First**
   - Security is not an afterthought
   - Design for security from day one
   - Document security measures

7. **Performance Matters**
   - Define performance requirements
   - Plan for scale from the start
   - Monitor and optimize continuously

### Common Architecture Pitfalls to Avoid

1. **Over-Engineering**: Building for problems you don't have yet
2. **Under-Engineering**: Ignoring known scale/performance requirements
3. **Technology Resume Building**: Choosing tech for learning, not fit
4. **Ignoring Operations**: Not considering deployment, monitoring, debugging
5. **No Clear Ownership**: Unclear who owns what component
6. **Tight Coupling**: Components too dependent on each other
7. **No Testing Strategy**: Testing as an afterthought

## Creating Epics

### Purpose
Epics group related user stories into logical feature areas. They represent high-level capabilities.

### Epic Structure

```markdown
# Epic #[X.0]: [Epic Name]

## Overview
[High-level description of this epic]

## Business Value
[Why is this epic important? What business goal does it support?]

## User Benefit
[How does this benefit end users?]

## Success Criteria
[How will we know this epic is complete and successful?]

## User Stories
- [X.1]: [Story title]
- [X.2]: [Story title]
- [X.3]: [Story title]

## Dependencies
- [Other epics or external dependencies]

## Estimated Effort
[T-shirt sizing: S/M/L/XL or story points]

## Priority
[Must Have / Should Have / Nice to Have]

## Target Release
[Which release/sprint?]
```

### Epic Numbering Convention
- **#1.0**: First major epic
- **#2.0**: Second major epic
- Stories within Epic #1.0: 1.1, 1.2, 1.3, etc.
- Stories within Epic #2.0: 2.1, 2.2, 2.3, etc.

### Epic Best Practices

1. **Keep Epics Cohesive**: Stories within an epic should be related
2. **Define Clear Boundaries**: Epic should represent a complete feature area
3. **Include Business Context**: Always explain the "why"
4. **Size Appropriately**: An epic should be deliverable in 1-3 sprints
5. **Make Them Testable**: Define clear success criteria

## Creating User Stories

### Purpose
User stories are detailed, implementable units of work. They should contain EVERYTHING a developer needs to build the feature.

### User Story Structure

```markdown
# Story [X.Y]: [Story Title]

## Story Metadata
- **Epic**: #[X.0] [Epic Name]
- **Priority**: [Must Have / Should Have / Nice to Have]
- **Estimated Effort**: [Story points or hours]
- **Status**: [Draft / Approved / In Progress / Done]
- **Assigned To**: [Developer name or TBD]

## User Story Statement
As a [type of user],
I want to [action/goal],
So that [benefit/value].

## Context and Background
[Detailed background information. Why are we building this? What problem does it solve? Include relevant context from the PRD and architecture.]

### Related Requirements
- **FR-[X]**: [Functional requirement this story addresses]
- **NFR-[X]**: [Non-functional requirements this story must satisfy]

### User Journey Context
[How does this story fit into the broader user experience?]

## Detailed Description
[Comprehensive description of what needs to be built. Be specific about:
- What UI elements are needed
- What data is processed
- What business logic is required
- How it integrates with other components
- What APIs or services are called]

## Acceptance Criteria

### Functional Criteria
1. **Given** [precondition]
   **When** [action]
   **Then** [expected result]

2. **Given** [precondition]
   **When** [action]
   **Then** [expected result]

[Continue for all scenarios]

### Non-Functional Criteria
- **Performance**: [Response time, load capacity]
- **Security**: [Authentication, authorization, data protection]
- **Accessibility**: [WCAG compliance, keyboard navigation]
- **Browser Support**: [Which browsers/versions]
- **Error Handling**: [Expected error scenarios and handling]

## Technical Implementation Guidance

### Architecture Context
[Relevant excerpts from architecture document: where this fits in the system, what patterns to use, what services to call]

### Data Model
[What data structures are involved? Database schema changes?]

### API Endpoints (if applicable)
```http
GET /api/[endpoint]
POST /api/[endpoint]
```
[Expected request/response formats]

### Key Technical Considerations
- [Integration points]
- [External dependencies]
- [Performance considerations]
- [Security requirements]
- [Error scenarios to handle]

## UI/UX Specifications (if applicable)

### Visual Design
[Mockups, wireframes, or detailed descriptions]

### Interaction Design
[User flows, state transitions, animations]

### Responsive Behavior
[How it adapts to different screen sizes]

### Accessibility Requirements
[ARIA labels, keyboard navigation, screen reader support]

## Testing Requirements

### Unit Tests
[What unit tests are needed?]

### Integration Tests
[What integration scenarios to test?]

### End-to-End Tests
[What user flows to test end-to-end?]

### Edge Cases
[Unusual scenarios to test]

## Dependencies

### Blocked By
[What must be completed before this story can start?]

### Blocks
[What other stories depend on this?]

### External Dependencies
[Third-party services, APIs, etc.]

## Definition of Done

- [ ] Code written and meets acceptance criteria
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Deployed to staging environment
- [ ] QA tested and approved
- [ ] Deployed to production
- [ ] Monitored for 24 hours with no issues

## Questions and Clarifications

### Open Questions
[Questions that need to be answered before implementation]

### Assumptions
[Assumptions being made]

### Risks
[Known risks or concerns]

## Notes

### Implementation Notes
[Additional notes for developers]

### Design Decisions
[Key decisions made and why]

### Future Enhancements
[Things to consider for future iterations]
```

### User Story Best Practices

1. **Include Full Context**: Developer should understand WHY and HOW, not just WHAT
2. **Be Hyper-Detailed**: More detail is better than less
3. **Make It Self-Contained**: Story should have everything needed to implement
4. **Use Clear Acceptance Criteria**: Given/When/Then format
5. **Include Technical Guidance**: Reference architecture, patterns, conventions
6. **Define Done Clearly**: Checklist of what "done" means
7. **Size Appropriately**: One story = one developer = 1-5 days of work
8. **Make It Testable**: Clear, verifiable acceptance criteria

## BMAD Workflow Guidelines

### When Creating Documentation

1. **Ask Probing Questions**
   - Don't assume - validate understanding
   - Challenge vague requirements
   - Dig deeper into motivations
   - Understand constraints

2. **Iterate and Refine**
   - Present draft for feedback
   - Incorporate changes
   - Validate alignment
   - Confirm understanding

3. **Provide Options**
   - Present alternatives when appropriate
   - Explain tradeoffs
   - Help user make informed decisions
   - Document decisions made

4. **Maintain Context**
   - Connect stories to epics
   - Link requirements to business goals
   - Show relationships between components
   - Reference relevant architecture

### Quality Standards

1. **Specificity Over Generality**
   - Concrete examples, not abstract concepts
   - Specific numbers, not ranges
   - Named entities, not "the system"

2. **Completeness**
   - All edge cases considered
   - All integration points identified
   - All NFRs addressed
   - All dependencies documented

3. **Clarity**
   - No ambiguous language
   - No jargon without explanation
   - Clear, scannable structure
   - Consistent terminology

4. **Actionability**
   - Testable acceptance criteria
   - Clear definition of done
   - Prioritized features
   - Assigned ownership

## Document Naming Conventions

### Files
- Project Brief: `docs/brief.md` or `docs/briefs/[feature-name].md`
- PRD: `docs/prd.md` or `docs/prd/[feature-name].md`
- Architecture: `docs/architecture.md`
- Epics: `docs/epics/[epic-number]-[epic-name].md`
- Stories: `docs/stories/[epic].[story]-[story-name].md`

### Examples
- `docs/brief.md`
- `docs/prd.md`
- `docs/epics/1.0-user-authentication.md`
- `docs/stories/1.1-login-form.md`
- `docs/stories/1.2-password-reset.md`

## Common Pitfalls to Avoid

1. **Being Too Generic**: Avoid bland, cookie-cutter language
2. **Insufficient Detail**: Stories should be comprehensive
3. **Missing Context**: Always explain the "why"
4. **Vague Acceptance Criteria**: Be specific and testable
5. **Ignoring NFRs**: Performance, security, etc. matter
6. **No Prioritization**: Everything can't be P0
7. **Missing Dependencies**: Identify what blocks what
8. **Unclear Definition of Done**: Be explicit

## Example Workflow

### User Request: "I need a PRD for a task management app"

**Claude's Approach:**

1. **Discovery Phase**
   ```
   Before I create the PRD, let me ask some key questions:

   - Who are the primary users? (individuals, teams, enterprises?)
   - What's the core problem you're solving? (too many tools, complexity, etc?)
   - What are the must-have features for MVP?
   - What are your key success metrics?
   - Any technical constraints? (platform, integrations, etc)
   - What's your target timeline?
   ```

2. **Draft PRD Creation**
   - Create comprehensive PRD following structure above
   - Include specific details based on answers
   - Flag areas needing more input

3. **Refinement**
   - Present draft for feedback
   - Ask follow-up questions on unclear areas
   - Iterate based on feedback

4. **Epic and Story Creation**
   - Break PRD into logical epics
   - Create detailed user stories
   - Ensure complete context in each story

## Integration with Development

### Handoff to Architecture
Once PRD is complete, architect should:
- Design system architecture
- Define technology stack
- Plan data models
- Identify integration points

### Handoff to Development
Stories should contain:
- Full PRD context relevant to the story
- Architecture excerpts relevant to implementation
- Clear technical guidance
- Complete acceptance criteria

### Quality Assurance
QA should use stories to:
- Write test cases from acceptance criteria
- Validate against NFRs
- Verify edge cases
- Check definition of done

## Tips for Success

1. **Start Simple, Add Depth**: Begin with structure, then add detail
2. **Use Templates Consistently**: Maintain structure across documents
3. **Link Everything**: Create traceability from brief → PRD → epic → story
4. **Version Control**: Track changes and decisions
5. **Review Regularly**: PRDs and stories should evolve
6. **Validate Often**: Check understanding with stakeholders
7. **Be Pragmatic**: Perfect is the enemy of good enough

## When to Use This Skill

Use this skill when:
- User requests a PRD, architecture document, epic, or user story
- User asks for product planning or technical architecture documentation
- User mentions "BMAD" or "agile planning"
- User needs help structuring requirements or technical design
- User wants detailed, context-rich documentation
- User is planning a software project or feature
- User needs system architecture, API design, or technology stack documentation

## When NOT to Use This Skill

Don't use for:
- Quick bug fixes (use simpler formats)
- Documentation that's not product/planning related
- When user explicitly asks for different format
- Non-software projects (unless requested)

---

**Remember**: The BMAD method is about creating high-quality, context-rich documentation through human-AI collaboration. Always ask questions, iterate, and ensure deep understanding before finalizing any document.
