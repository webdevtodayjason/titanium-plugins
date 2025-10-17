# Agent-to-Skills Mapping

This document defines which skills each agent should have access to, following Anthropic's Agent Skills guidelines.

## Skills Architecture

### Skill Categories

1. **Product/Planning**: BMAD methodology, requirements, roadmaps
2. **Development**: API design, frontend patterns, backend architecture
3. **Quality**: Code quality, testing, security
4. **Operations**: DevOps, infrastructure, deployment
5. **Documentation**: Technical writing, API docs

## Current Skills

### bmad-methodology (EXISTS ✅)
**File**: `skills/bmad-methodology/SKILL.md`
**Purpose**: Complete BMAD methodology for PRD, Architecture, Epic, and Story creation
**Size**: 1092 lines
**Used by**: product-manager, architect, project-planner

## Skills to Create

### 1. api-best-practices (NEW)
**File**: `skills/api-best-practices/SKILL.md`
**Purpose**: REST API design, OpenAPI specs, versioning, error handling, authentication patterns
**Content**:
- RESTful design principles
- HTTP status codes and when to use them
- API versioning strategies (URL vs header)
- Request/response patterns
- Error handling and error responses
- Rate limiting implementation
- Authentication (JWT, OAuth2, API keys)
- OpenAPI/Swagger documentation
- Pagination strategies
- HATEOAS principles
- API security best practices

**Used by**: api-developer, api-documenter

### 2. frontend-patterns (NEW)
**File**: `skills/frontend-patterns/SKILL.md`
**Purpose**: Modern frontend architecture, component patterns, state management, performance
**Content**:
- Component composition patterns
- State management (Redux, Zustand, Context)
- Performance optimization (memoization, lazy loading, code splitting)
- Accessibility (WCAG 2.1, ARIA)
- Responsive design patterns
- Form validation patterns
- Error boundary patterns
- Data fetching strategies (React Query, SWR)
- Testing patterns (unit, integration, E2E)
- Build optimization

**Used by**: frontend-developer, shadcn-ui-builder

### 3. testing-strategy (NEW)
**File**: `skills/testing-strategy/SKILL.md`
**Purpose**: TDD practices, test pyramid, coverage strategies, mocking
**Content**:
- Test pyramid (70% unit, 20% integration, 10% E2E)
- TDD red-green-refactor cycle
- Test structure (Arrange-Act-Assert)
- Mocking strategies and when to use them
- Test coverage goals and measuring
- Integration testing patterns
- E2E testing with Playwright/Cypress
- Performance testing
- Flaky test prevention
- Test data management
- CI/CD integration

**Used by**: tdd-specialist, test-runner

### 4. code-quality-standards (NEW)
**File**: `skills/code-quality-standards/SKILL.md`
**Purpose**: SOLID principles, design patterns, code smells, refactoring
**Content**:
- SOLID principles with examples
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Common design patterns (Factory, Strategy, Observer, etc.)
- Code smells and how to detect them
- Refactoring patterns
- Naming conventions
- Function/method size guidelines
- Cyclomatic complexity targets
- Technical debt management

**Used by**: code-reviewer, refactor

### 5. security-checklist (NEW)
**File**: `skills/security-checklist/SKILL.md`
**Purpose**: OWASP Top 10, common vulnerabilities, security patterns
**Content**:
- OWASP Top 10 detailed explanations
- SQL injection prevention
- XSS prevention
- CSRF protection
- Authentication best practices
- Authorization patterns (RBAC, ABAC)
- Secrets management
- Input validation
- Output encoding
- Security headers
- Rate limiting
- Logging sensitive data avoidance
- Dependency scanning

**Used by**: security-scanner

### 6. devops-patterns (NEW)
**File**: `skills/devops-patterns/SKILL.md`
**Purpose**: CI/CD, infrastructure as code, deployment strategies, monitoring
**Content**:
- CI/CD pipeline design
- GitHub Actions / GitLab CI patterns
- Infrastructure as Code (Terraform, CloudFormation)
- Container best practices (Docker)
- Kubernetes patterns
- Blue-green deployment
- Canary deployments
- Rolling updates
- Database migration strategies
- Environment management
- Monitoring and alerting (Prometheus, Grafana)
- Log aggregation
- Disaster recovery

**Used by**: devops-engineer

### 7. debugging-methodology (NEW)
**File**: `skills/debugging-methodology/SKILL.md`
**Purpose**: Systematic debugging, root cause analysis, diagnostic techniques
**Content**:
- Scientific debugging method
- Reproducing bugs consistently
- Binary search debugging
- Stack trace analysis
- Logging strategies
- Debugging tools (debuggers, profilers)
- Memory leak detection
- Performance profiling
- Network debugging
- Race condition detection
- Common bug patterns
- Root cause analysis (5 Whys)

**Used by**: debugger

### 8. technical-writing (NEW)
**File**: `skills/technical-writing/SKILL.md`
**Purpose**: Clear documentation, README structure, API docs, tutorials
**Content**:
- Documentation structure (README, guides, reference)
- Clear writing principles
- Code example best practices
- Tutorial structure
- API documentation patterns
- Changelog best practices
- Markdown formatting
- Diagrams and visuals
- Progressive disclosure
- User-focused language
- Avoiding jargon
- Version documentation

**Used by**: doc-writer, api-documenter

### 9. project-planning (NEW)
**File**: `skills/project-planning/SKILL.md`
**Purpose**: Breaking down complex projects, estimation, dependency management
**Content**:
- Work breakdown structure (WBS)
- Task estimation techniques (story points, t-shirt sizing)
- Dependency identification
- Critical path analysis
- Risk assessment
- Milestone planning
- Sprint planning
- Capacity planning
- Burndown charts
- Velocity tracking
- Agile ceremonies
- Stakeholder communication

**Used by**: project-planner, product-manager

## Agent Skills Assignment

### Planning & Product Agents

**product-manager**
- Skills: bmad-methodology, project-planning
- Why: Creates PRDs, briefs, epics, user stories + manages product roadmap

**project-planner**
- Skills: bmad-methodology, project-planning
- Why: Breaks down projects into tasks, manages dependencies

**architect**
- Skills: bmad-methodology, api-best-practices, devops-patterns
- Why: Creates technical architecture, chooses tech stack, designs systems

### Development Agents

**api-developer**
- Skills: api-best-practices, testing-strategy, security-checklist
- Why: Builds REST APIs following best practices with security and tests

**frontend-developer**
- Skills: frontend-patterns, testing-strategy, technical-writing
- Why: Builds UI components with testing and component documentation

**devops-engineer**
- Skills: devops-patterns, security-checklist
- Why: Sets up CI/CD, infrastructure, monitors systems securely

### Quality Agents

**code-reviewer**
- Skills: code-quality-standards, security-checklist, testing-strategy
- Why: Reviews for quality, security, and test coverage

**refactor**
- Skills: code-quality-standards, testing-strategy
- Why: Improves code structure while maintaining tests

**tdd-specialist**
- Skills: testing-strategy, code-quality-standards
- Why: Writes tests first, follows TDD methodology

**test-runner**
- Skills: testing-strategy, debugging-methodology
- Why: Runs tests, debugs failures

**security-scanner**
- Skills: security-checklist, code-quality-standards
- Why: Scans for vulnerabilities, recommends security improvements

**debugger**
- Skills: debugging-methodology, testing-strategy
- Why: Systematically finds and fixes bugs

### Documentation Agents

**doc-writer**
- Skills: technical-writing, bmad-methodology
- Why: Creates technical docs, may reference BMAD structure

**api-documenter**
- Skills: technical-writing, api-best-practices
- Why: Creates API documentation following API patterns

### Specialized Agents

**shadcn-ui-builder**
- Skills: frontend-patterns, technical-writing
- Why: Builds UI with shadcn components, documents components

**marketing-writer**
- Skills: technical-writing
- Why: Creates marketing content with clear writing

**meta-agent**
- Skills: (none - creates agents, shouldn't be constrained)
- Why: Generates agent configurations, needs flexibility

## Skill Priority Order

### Phase 1: Core Skills (Create First)
1. ✅ bmad-methodology (exists)
2. api-best-practices
3. frontend-patterns
4. testing-strategy
5. security-checklist

### Phase 2: Quality & Ops Skills
6. code-quality-standards
7. devops-patterns
8. debugging-methodology

### Phase 3: Documentation & Planning
9. technical-writing
10. project-planning

## Skill Naming Convention

Per Anthropic guidelines:
- **Directory**: `skills/{skill-name}/`
- **Main file**: `skills/{skill-name}/SKILL.md` (uppercase)
- **Supporting files**: `skills/{skill-name}/examples.md`, `reference.md`, etc.

## Skill Frontmatter Template

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include specific triggers like "Use when..." and relevant keywords.
---
```

## Next Steps

1. Create Phase 1 skills (api-best-practices, frontend-patterns, testing-strategy, security-checklist)
2. Create Phase 2 skills (code-quality-standards, devops-patterns, debugging-methodology)
3. Create Phase 3 skills (technical-writing, project-planning)
4. Update all agent frontmatter with skills references
5. Update slash commands to use subagent delegation pattern
6. Create new slash command: `/titanium:getting-started` explaining orchestration model
