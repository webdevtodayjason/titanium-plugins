---
name: project-planning
description: Project planning methodologies including work breakdown structure, task estimation, dependency management, risk assessment, sprint planning, and stakeholder communication. Use when breaking down projects, estimating work, planning sprints, or managing dependencies.
---

# Project Planning

This skill provides comprehensive guidance for planning and managing software development projects effectively.

## Work Breakdown Structure (WBS)

### Breaking Down Large Projects

```markdown
Project: E-commerce Platform
├── 1. User Management
│   ├── 1.1 Authentication
│   │   ├── 1.1.1 Email/Password Login
│   │   ├── 1.1.2 Social Login (Google, Facebook)
│   │   └── 1.1.3 Password Reset
│   ├── 1.2 User Profiles
│   │   ├── 1.2.1 Profile Creation
│   │   ├── 1.2.2 Profile Editing
│   │   └── 1.2.3 Avatar Upload
│   └── 1.3 Role Management
│       ├── 1.3.1 Admin Role
│       ├── 1.3.2 Customer Role
│       └── 1.3.3 Vendor Role
├── 2. Product Catalog
│   ├── 2.1 Product Listings
│   ├── 2.2 Product Details
│   ├── 2.3 Product Search
│   └── 2.4 Product Categories
├── 3. Shopping Cart
│   ├── 3.1 Add to Cart
│   ├── 3.2 Update Quantities
│   ├── 3.3 Remove Items
│   └── 3.4 Cart Persistence
├── 4. Checkout
│   ├── 4.1 Shipping Address
│   ├── 4.2 Payment Processing
│   ├── 4.3 Order Confirmation
│   └── 4.4 Email Notifications
└── 5. Order Management
    ├── 5.1 Order History
    ├── 5.2 Order Tracking
    └── 5.3 Order Cancellation
```

### WBS Best Practices

**1. Start with deliverables, not activities**
```markdown
❌ Wrong (activities):
- Write code
- Test features
- Deploy

✅ Right (deliverables):
- User Authentication System
- Product Search Feature
- Payment Integration
```

**2. Use the 8/80 rule**
- No task should take less than 8 hours (too granular)
- No task should take more than 80 hours (too large)
- Sweet spot: 1-5 days per task

**3. Break down until you can estimate**
```markdown
❌ Too vague:
- Build API (? days)

✅ Specific:
- Design API endpoints (1 day)
- Implement authentication (2 days)
- Create CRUD operations (3 days)
- Write API documentation (1 day)
- Add rate limiting (1 day)
Total: 8 days
```

## Task Estimation

### Story Points

**Fibonacci Scale**: 1, 2, 3, 5, 8, 13, 21

```markdown
1 point - Trivial
- Update documentation
- Fix typo
- Change button color

2 points - Simple
- Add validation to form field
- Create simple API endpoint
- Write unit tests for existing function

3 points - Moderate
- Implement login form
- Add pagination to list
- Create database migration

5 points - Complex
- Build user profile page
- Implement search functionality
- Add email notifications

8 points - Very Complex
- Build payment integration
- Implement complex reporting
- Create admin dashboard

13 points - Epic
- Build entire authentication system
- Create complete checkout flow
(Should be broken down further)
```

### T-Shirt Sizing

**Quick estimation for early planning**:

```markdown
XS (1-2 days)
- Bug fixes
- Minor UI updates
- Documentation updates

S (3-5 days)
- Small features
- Simple integrations
- Basic CRUD operations

M (1-2 weeks)
- Medium features
- Standard integrations
- Multiple related stories

L (2-4 weeks)
- Large features
- Complex integrations
- Multiple epics

XL (1-2 months)
- Major features
- System redesigns
(Should be broken down into smaller pieces)
```

### Planning Poker

**Collaborative estimation process**:

```markdown
1. Product Owner presents user story
2. Team asks clarifying questions
3. Each member privately selects estimate
4. All reveal simultaneously
5. Discuss differences (especially highest/lowest)
6. Re-estimate if needed
7. Reach consensus

Example Session:
Story: "As a user, I want to reset my password"

Round 1 Estimates: 2, 3, 3, 8, 3
Discussion: Why 8?
- "What about email templates?"
- "What if SMTP fails?"
- "Need password strength validation"

Round 2 Estimates: 5, 5, 5, 5, 5
Consensus: 5 points
```

### Estimation Accuracy

**Cone of Uncertainty**:
```
Project Start: ±100% accuracy
Requirements: ±50% accuracy
Design: ±25% accuracy
Development: ±10% accuracy
Testing: ±5% accuracy
```

**Build in buffer**:
```markdown
Optimistic: 3 days
Realistic: 5 days
Pessimistic: 8 days

Formula: (Optimistic + 4×Realistic + Pessimistic) ÷ 6
Buffer: (3 + 4×5 + 8) ÷ 6 = 5.2 days

Use 6 days for planning
```

## Dependency Identification

### Types of Dependencies

```markdown
1. Finish-to-Start (FS) - Most common
   Task B cannot start until Task A finishes
   Example: Design → Development

2. Start-to-Start (SS)
   Task B cannot start until Task A starts
   Example: Development → Code Review (parallel)

3. Finish-to-Finish (FF)
   Task B cannot finish until Task A finishes
   Example: Development → Testing (testing continues)

4. Start-to-Finish (SF) - Rare
   Task B cannot finish until Task A starts
   Example: Old system → New system (overlap)
```

### Dependency Mapping

```markdown
Task Dependencies:

1. Database Schema Design
   └─► 2. API Development (FS)
       ├─► 3. Frontend Development (FS)
       └─► 4. Integration Tests (SS)
           └─► 5. End-to-End Tests (FS)

2. API Development
   └─► 6. API Documentation (SS)

3. Frontend Development
   └─► 7. UI/UX Review (FF)

Critical Path: 1 → 2 → 3 → 5
(Longest path through dependencies)
```

### Managing Dependencies

```typescript
// Dependency tracking in code
interface Task {
  id: string;
  name: string;
  dependencies: string[]; // IDs of tasks that must complete first
  status: 'pending' | 'in-progress' | 'completed' | 'blocked';
}

const tasks: Task[] = [
  {
    id: 'db-schema',
    name: 'Design database schema',
    dependencies: [],
    status: 'completed',
  },
  {
    id: 'api-dev',
    name: 'Develop API',
    dependencies: ['db-schema'],
    status: 'in-progress',
  },
  {
    id: 'frontend-dev',
    name: 'Develop frontend',
    dependencies: ['api-dev'],
    status: 'blocked', // Waiting for API
  },
];

function canStartTask(taskId: string): boolean {
  const task = tasks.find(t => t.id === taskId);
  if (!task) return false;

  // Check if all dependencies are completed
  return task.dependencies.every(depId => {
    const dep = tasks.find(t => t.id === depId);
    return dep?.status === 'completed';
  });
}
```

## Critical Path Analysis

### Finding the Critical Path

```markdown
Project: Launch Marketing Website

Tasks:
A. Design mockups (3 days)
B. Develop frontend (5 days) - depends on A
C. Write content (4 days) - independent
D. Set up hosting (1 day) - independent
E. Deploy website (1 day) - depends on B, C, D
F. Test website (2 days) - depends on E

Path 1: A → B → E → F = 3 + 5 + 1 + 2 = 11 days
Path 2: C → E → F = 4 + 1 + 2 = 7 days
Path 3: D → E → F = 1 + 1 + 2 = 4 days

Critical Path: A → B → E → F (11 days)
(Any delay in these tasks delays the entire project)
```

### Managing Critical Path

```markdown
Strategies:

1. Fast-track critical tasks
   - Assign best developers
   - Remove blockers immediately
   - Daily status checks

2. Crash critical tasks (add resources)
   - Pair programming
   - Additional team members
   - Overtime (carefully)

3. Parallelize where possible
   - Content writing during development
   - Documentation during testing

4. Monitor closely
   - Daily updates on critical path
   - Early warning of delays
   - Quick decision-making
```

## Risk Assessment and Mitigation

### Risk Matrix

```markdown
Impact vs Probability:

        Low         Medium        High
High    Monitor     Mitigate      Immediate Action
Medium  Accept      Monitor       Mitigate
Low     Accept      Accept        Monitor

Example Risks:

1. API Integration Delays (High Impact, Medium Probability)
   → Mitigate: Start integration early, have backup plan

2. Key Developer Leaves (High Impact, Low Probability)
   → Monitor: Document knowledge, cross-train team

3. Library Deprecated (Medium Impact, Low Probability)
   → Accept: Will address if it happens
```

### Risk Register

```markdown
| ID | Risk | Impact | Prob | Status | Mitigation |
|----|------|--------|------|--------|------------|
| R1 | Third-party API unreliable | High | Medium | Active | Build fallback, cache responses |
| R2 | Database performance issues | High | Low | Monitor | Load testing, optimization plan |
| R3 | Requirements change | Medium | High | Active | Weekly stakeholder sync, flexible architecture |
| R4 | Security vulnerability | High | Low | Monitor | Security audits, dependency scanning |
| R5 | Team member unavailable | Medium | Medium | Active | Documentation, knowledge sharing |
```

### Risk Mitigation Strategies

```markdown
1. Avoidance - Eliminate risk
   Risk: Untested technology
   Action: Use proven technology stack

2. Reduction - Decrease likelihood/impact
   Risk: Integration failures
   Action: Early integration testing, CI/CD

3. Transfer - Share risk
   Risk: Infrastructure failure
   Action: Use cloud provider with SLA

4. Acceptance - Accept risk
   Risk: Minor UI inconsistencies
   Action: Document and fix in future release
```

## Milestone Planning

### Setting Milestones

```markdown
Project Timeline: 12 weeks

Week 2: M1 - Requirements Complete
- All user stories defined
- Mockups approved
- Technical design ready
✓ Milestone met when: PRD signed off

Week 4: M2 - Foundation Complete
- Database schema implemented
- Authentication working
- Basic API endpoints created
✓ Milestone met when: Users can log in

Week 7: M3 - Core Features Complete
- All CRUD operations working
- Main user flows implemented
- Integration tests passing
✓ Milestone met when: Alpha testing can begin

Week 10: M4 - Feature Complete
- All features implemented
- Bug fixes complete
- Documentation written
✓ Milestone met when: Beta testing ready

Week 12: M5 - Launch
- Production deployment
- Monitoring in place
- Support processes ready
✓ Milestone met when: Live to users
```

## Sprint Planning

### Sprint Structure (2-week sprint)

```markdown
Day 1 - Monday: Sprint Planning
- Review backlog
- Estimate stories
- Commit to sprint goal

Days 2-9: Development
- Daily standups
- Development work
- Code reviews
- Testing

Day 10 - Friday Week 2: Sprint Review & Retrospective
- Demo completed work
- Discuss what went well/poorly
- Plan improvements
```

### Sprint Planning Meeting

```markdown
Agenda (2 hours):

Part 1: Sprint Goal (30 min)
- Review product roadmap
- Define sprint goal
- Identify high-priority items

Example Sprint Goal:
"Enable users to browse and search products"

Part 2: Story Selection (60 min)
- Review top backlog items
- Estimate stories
- Check capacity
- Commit to stories

Team Capacity:
- 5 developers × 8 days × 6 hours = 240 hours
- Velocity: 40 story points per sprint
- Buffer: 20% for bugs/meetings = 32 points

Selected Stories:
- Product list page (5 pts)
- Product search (8 pts)
- Product filters (8 pts)
- Product pagination (3 pts)
- Product sort (3 pts)
- Bug fixes (5 pts)
Total: 32 points

Part 3: Task Breakdown (30 min)
- Break stories into tasks
- Identify blockers
- Assign initial tasks
```

## Capacity Planning

### Calculating Team Capacity

```markdown
Team: 5 Developers
Sprint: 2 weeks (10 working days)

Available Hours:
5 developers × 10 days × 8 hours = 400 hours

Subtract Non-Dev Time:
- Meetings: 2 hours/day × 10 days × 5 people = 100 hours
- Code reviews: 1 hour/day × 10 days × 5 people = 50 hours
- Planning/retro: 4 hours × 5 people = 20 hours

Actual Development Time:
400 - 100 - 50 - 20 = 230 hours

Story Points:
If 1 point ≈ 6 hours
Capacity: 230 ÷ 6 ≈ 38 points

Add 20% buffer: 30 points safe commitment
```

### Handling Vacation and Absences

```markdown
Team Capacity with Absences:

Regular Capacity: 40 points

Developer A: Out entire sprint (-8 points)
Developer B: Out 3 days (-5 points)
Holiday: 1 day for everyone (-8 points)

Adjusted Capacity:
40 - 8 - 5 - 8 = 19 points

Plan accordingly:
- Smaller sprint goal
- Fewer stories
- Focus on high priority
- Avoid risky work
```

## Burndown Charts

### Creating Burndown Charts

```markdown
Sprint Burndown:

Day | Remaining Points | Ideal Burn
----|------------------|------------
0   | 40              | 40
1   | 38              | 36
2   | 35              | 32
3   | 32              | 28
4   | 28              | 24
5   | 28              | 20  ← Weekend
6   | 28              | 16  ← Weekend
7   | 25              | 12
8   | 20              | 8
9   | 12              | 4
10  | 0               | 0

Ideal line: Straight from start to finish
Actual line: Based on completed work

Analysis:
- Days 3-6: Slow progress (blocker?)
- Day 7: Back on track
- Day 9: Ahead of schedule
```

### Interpreting Burndown Trends

```markdown
Scenarios:

1. Line below ideal
   → Ahead of schedule
   → May have underestimated
   → Consider pulling in more work

2. Line above ideal
   → Behind schedule
   → May have overcommitted
   → Identify blockers
   → Consider removing stories

3. Flat line
   → No progress
   → Blocker or team unavailable
   → Immediate intervention needed

4. Increasing line
   → Scope creep
   → Stories added mid-sprint
   → Review sprint boundaries
```

## Velocity Tracking

### Measuring Velocity

```markdown
Historical Velocity:

Sprint 1: 28 points completed
Sprint 2: 32 points completed
Sprint 3: 30 points completed
Sprint 4: 35 points completed
Sprint 5: 33 points completed

Average Velocity: (28+32+30+35+33) ÷ 5 = 31.6 points

Use for Planning:
- Conservative: 28 points (lowest recent)
- Realistic: 32 points (average)
- Optimistic: 35 points (highest recent)

Recommend: Use 32 points for next sprint
```

### Velocity Trends

```markdown
Improving Velocity:
Sprint 1: 20 → Sprint 2: 25 → Sprint 3: 30
- Team learning
- Process improvements
- Good trend

Declining Velocity:
Sprint 1: 35 → Sprint 2: 30 → Sprint 3: 25
- Technical debt accumulating
- Team burnout
- Need intervention

Stable Velocity:
Sprint 1: 30 → Sprint 2: 31 → Sprint 3: 29
- Sustainable pace
- Predictable
- Ideal state
```

## Agile Ceremonies

### Daily Standup (15 minutes)

```markdown
Format: Each person answers:
1. What did I complete yesterday?
2. What will I work on today?
3. What blockers do I have?

Example:
"Yesterday I completed the login form.
Today I'll start on the password reset flow.
I'm blocked on the email template approval."

Anti-patterns:
❌ Status reports to manager
❌ Problem-solving discussions
❌ More than 15 minutes

Best practices:
✓ Same time, same place
✓ Everyone participates
✓ Park detailed discussions
✓ Update task board
```

### Sprint Review (1 hour)

```markdown
Agenda:
1. Demo completed work (40 min)
   - Show working software
   - Get stakeholder feedback
   - Note requested changes

2. Review sprint metrics (10 min)
   - Velocity
   - Completed vs planned
   - Quality metrics

3. Update product backlog (10 min)
   - Adjust priorities
   - Add new items
   - Remove obsolete items

Tips:
- Focus on working software
- No PowerPoint presentations
- Encourage feedback
- Keep it informal
```

### Sprint Retrospective (1 hour)

```markdown
Format: What went well / What to improve / Action items

Example:

What Went Well:
✓ Completed all planned stories
✓ Good collaboration on complex feature
✓ Improved code review process

What to Improve:
⚠ Too many meetings interrupted flow
⚠ Test environment was unstable
⚠ Requirements unclear on story X

Action Items:
1. Block "focus time" 2-4pm daily (Owner: Scrum Master)
2. Fix test environment stability (Owner: DevOps)
3. Refine stories with PO before sprint (Owner: Team Lead)

Follow-up:
- Review action items at next retro
- Track completion
- Celebrate improvements
```

## Stakeholder Communication

### Status Reports

```markdown
Weekly Status Report - Week of Oct 16, 2025

Sprint Progress:
- Completed: 18/32 points (56%)
- On Track: Yes
- Sprint Goal: Enable product browsing

Completed This Week:
✓ Product list page with pagination
✓ Basic search functionality
✓ Product filters (category, price)

In Progress:
• Advanced search with autocomplete (90% done)
• Product sort options (started today)

Upcoming Next Week:
○ Complete remaining search features
○ Begin product detail page
○ Integration testing

Blockers/Risks:
⚠ Designer out sick - UI reviews delayed 1 day
⚠ Third-party API slow - investigating alternatives

Metrics:
- Velocity: 32 points/sprint (stable)
- Bug count: 3 (all low priority)
- Test coverage: 85%

Next Milestone:
M3 - Core Features (Week 7) - On track
```

### Stakeholder Matrix

```markdown
| Stakeholder | Role | Interest | Influence | Communication |
|-------------|------|----------|-----------|---------------|
| CEO | Sponsor | High | High | Monthly exec summary |
| Product Manager | Owner | High | High | Daily collaboration |
| Engineering Manager | Lead | High | High | Daily standup |
| Marketing Director | User | Medium | Medium | Weekly demo |
| Customer Support | User | Medium | Low | Sprint review |
| End Users | Consumer | High | Low | Beta feedback |
```

## Project Tracking Tools

### Issue/Task Management

```markdown
GitHub Issues / Jira / Linear:

Epic: User Authentication
├── Story: Email/Password Login (8 pts)
│   ├── Task: Design login form
│   ├── Task: Implement API endpoint
│   ├── Task: Add validation
│   └── Task: Write tests
├── Story: Social Login (5 pts)
└── Story: Password Reset (5 pts)

Labels:
- Priority: P0 (Critical), P1 (High), P2 (Normal), P3 (Low)
- Type: Feature, Bug, Tech Debt, Documentation
- Status: Todo, In Progress, In Review, Done
- Component: Frontend, Backend, Database, DevOps
```

### Documentation

```markdown
Essential Project Documents:

1. Product Requirements Document (PRD)
   - Features and requirements
   - User stories
   - Acceptance criteria

2. Technical Design Document
   - Architecture
   - Technology choices
   - API design

3. Project Charter
   - Goals and objectives
   - Scope
   - Timeline
   - Resources

4. Risk Register
   - Identified risks
   - Mitigation plans
   - Status

5. Sprint Plans
   - Sprint goals
   - Committed stories
   - Capacity
```

## Planning Checklist

**Project Initiation**:
- [ ] Define project goals and objectives
- [ ] Identify stakeholders
- [ ] Create project charter
- [ ] Define scope and requirements
- [ ] Estimate timeline and budget

**Planning Phase**:
- [ ] Create work breakdown structure
- [ ] Estimate tasks
- [ ] Identify dependencies
- [ ] Assess risks
- [ ] Define milestones
- [ ] Allocate resources

**Sprint Planning**:
- [ ] Review and refine backlog
- [ ] Define sprint goal
- [ ] Estimate stories
- [ ] Check team capacity
- [ ] Commit to sprint backlog
- [ ] Break down into tasks

**During Execution**:
- [ ] Track progress daily
- [ ] Update burndown chart
- [ ] Address blockers immediately
- [ ] Communicate with stakeholders
- [ ] Adjust plan as needed

**Sprint Close**:
- [ ] Demo completed work
- [ ] Conduct retrospective
- [ ] Update velocity metrics
- [ ] Plan next sprint

## When to Use This Skill

Use this skill when:
- Starting new projects
- Breaking down large initiatives
- Estimating work effort
- Planning sprints
- Managing dependencies
- Assessing risks
- Tracking progress
- Communicating with stakeholders
- Running agile ceremonies
- Improving team processes

---

**Remember**: Plans are useless, but planning is essential. Stay flexible, communicate often, and adjust course based on reality. The goal is not perfect adherence to the plan, but successfully delivering value to users.
