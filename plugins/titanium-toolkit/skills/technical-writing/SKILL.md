---
name: technical-writing
description: Technical writing best practices including documentation structure, clear writing principles, API documentation, tutorials, changelogs, and markdown formatting. Use when writing documentation, creating READMEs, documenting APIs, or writing tutorials.
---

# Technical Writing

This skill provides comprehensive guidance for creating clear, effective technical documentation that helps users and developers.

## Documentation Structure

### The Four Types of Documentation

**1. Tutorials** (Learning-oriented)
- Goal: Help beginners learn
- Format: Step-by-step lessons
- Example: "Build your first API"

**2. How-to Guides** (Problem-oriented)
- Goal: Solve specific problems
- Format: Numbered steps
- Example: "How to deploy to production"

**3. Reference** (Information-oriented)
- Goal: Provide detailed information
- Format: Systematic descriptions
- Example: API reference, configuration options

**4. Explanation** (Understanding-oriented)
- Goal: Clarify concepts
- Format: Discursive explanations
- Example: Architecture decisions, design patterns

### README Structure

```markdown
# Project Name

Brief description of what the project does (1-2 sentences).

[![Build Status](badge)](link)
[![Coverage](badge)](link)
[![License](badge)](link)

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

```bash
# Installation
npm install project-name

# Usage
npx project-name init
```

## Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Redis 7+

## Installation

### Using npm

```bash
npm install project-name
```

### Using yarn

```bash
yarn add project-name
```

### From source

```bash
git clone https://github.com/user/project.git
cd project
npm install
npm run build
```

## Configuration

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/db
API_KEY=your_api_key
```

## Usage

### Basic Example

```typescript
import { createClient } from 'project-name';

const client = createClient({
  apiKey: process.env.API_KEY,
});

const result = await client.doSomething();
console.log(result);
```

### Advanced Example

[More complex example with explanations]

## API Reference

See [API.md](./API.md) for complete API documentation.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT © [Author Name]

## Support

- Documentation: https://docs.example.com
- Issues: https://github.com/user/project/issues
- Discussions: https://github.com/user/project/discussions
```

## Clear Writing Principles

### Use Active Voice

```markdown
❌ Passive: The data is validated by the function.
✅ Active: The function validates the data.

❌ Passive: Errors should be handled by your application.
✅ Active: Your application should handle errors.
```

### Use Simple Language

```markdown
❌ Complex: Utilize the aforementioned methodology to instantiate a novel instance.
✅ Simple: Use this method to create a new instance.

❌ Jargon: Leverage our SDK to synergize with the API ecosystem.
✅ Clear: Use our SDK to connect to the API.
```

### Be Concise

```markdown
❌ Wordy: In order to be able to successfully complete the installation process,
you will need to make sure that you have Node.js version 18 or higher installed
on your system.
✅ Concise: Install Node.js 18 or higher.

❌ Redundant: The function returns back a response.
✅ Concise: The function returns a response.
```

### Use Consistent Terminology

```markdown
❌ Inconsistent:
- Create a user
- Add an account
- Register a member
(All referring to the same action)

✅ Consistent:
- Create a user
- Update a user
- Delete a user
```

## Code Example Best Practices

### Complete, Runnable Examples

```typescript
// ❌ BAD - Incomplete example
user.save();

// ✅ GOOD - Complete example
import { User } from './models';

async function createUser() {
  const user = new User({
    email: 'user@example.com',
    name: 'John Doe',
  });

  await user.save();
  console.log('User created:', user.id);
}

createUser();
```

### Show Expected Output

```typescript
// Calculate fibonacci number
function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10));
// Output: 55
```

### Highlight Important Parts

```typescript
// Authenticate user with JWT
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // 👇 Important: Always use bcrypt for password comparison
  const isValid = await bcrypt.compare(password, user.passwordHash);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken(user);
  res.json({ token });
});
```

### Provide Context

```typescript
// ❌ BAD - No context
await client.query('SELECT * FROM users');

// ✅ GOOD - With context
// Fetch all active users who logged in within the last 30 days
const activeUsers = await client.query(`
  SELECT id, email, name, last_login
  FROM users
  WHERE status = 'active'
    AND last_login > NOW() - INTERVAL '30 days'
  ORDER BY last_login DESC
`);
```

## Tutorial Structure

### Learning Progression

**1. Introduction** (2-3 sentences)
- What will users learn?
- Why is it useful?

**2. Prerequisites**
- Required knowledge
- Required tools
- Time estimate

**3. Step-by-Step Instructions**
- Number each step
- One concept per step
- Show results after each step

**4. Next Steps**
- Links to related tutorials
- Advanced topics
- Additional resources

### Tutorial Example

```markdown
# Building a REST API with Express

In this tutorial, you'll build a REST API for managing a todo list.
You'll learn how to create routes, handle requests, and connect to a database.

**Time**: 30 minutes
**Level**: Beginner

## Prerequisites

- Node.js 18+ installed
- Basic JavaScript knowledge
- Code editor (VS Code recommended)

## Step 1: Set Up Project

Create a new project directory and initialize npm:

```bash
mkdir todo-api
cd todo-api
npm init -y
```

Install Express:

```bash
npm install express
```

You should see `express` added to your `package.json`.

## Step 2: Create Basic Server

Create `index.js`:

```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

Run the server:

```bash
node index.js
```

Visit http://localhost:3000 in your browser. You should see:
```json
{ "message": "Hello, World!" }
```

## Step 3: Add Todo Routes

[Continue with more steps...]

## What You Learned

- How to set up an Express server
- How to create REST API routes
- How to connect to a database

## Next Steps

- [Authentication with JWT](./auth-tutorial.md)
- [Deploy to Production](./deploy-guide.md)
- [API Best Practices](./api-best-practices.md)
```

## API Documentation Patterns

### Endpoint Documentation

```markdown
## Create User

Creates a new user account.

**Endpoint**: `POST /api/v1/users`

**Authentication**: Not required

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address (must be valid) |
| password | string | Yes | Password (min 8 characters) |
| name | string | Yes | User's full name (max 100 characters) |

**Example Request**:

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "name": "John Doe"
  }'
```

**Success Response** (201 Created):

```json
{
  "id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2025-10-16T10:30:00Z"
}
```

**Error Responses**:

**400 Bad Request** - Invalid input:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "field": "email"
  }
}
```

**409 Conflict** - Email already exists:
```json
{
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email address already registered"
  }
}
```

**Rate Limit**: 5 requests per minute
```

### Function/Method Documentation

```typescript
/**
 * Calculates the total price of items including tax.
 *
 * @param items - Array of items to calculate total for
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @returns Total price including tax
 *
 * @throws {Error} If items array is empty
 * @throws {Error} If taxRate is negative
 *
 * @example
 * ```typescript
 * const items = [
 *   { price: 10, quantity: 2 },
 *   { price: 15, quantity: 1 }
 * ];
 * const total = calculateTotal(items, 0.08);
 * console.log(total); // 37.80
 * ```
 */
function calculateTotal(
  items: Array<{ price: number; quantity: number }>,
  taxRate: number
): number {
  if (items.length === 0) {
    throw new Error('Items array cannot be empty');
  }
  if (taxRate < 0) {
    throw new Error('Tax rate cannot be negative');
  }

  const subtotal = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  return subtotal * (1 + taxRate);
}
```

## Changelog Best Practices

### Keep a Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature X for Y use case

### Changed
- Improved performance of Z operation

### Fixed
- Fixed bug where A caused B

## [2.1.0] - 2025-10-16

### Added
- User profile avatars (#123)
- Email notification settings (#125)
- Two-factor authentication support (#130)

### Changed
- Updated UI for settings page (#124)
- Improved API response times by 40% (#128)

### Deprecated
- `oldFunction()` will be removed in v3.0 - use `newFunction()` instead

### Fixed
- Fixed memory leak in session management (#126)
- Corrected timezone handling in reports (#129)

### Security
- Updated dependencies to patch security vulnerabilities (#127)

## [2.0.0] - 2025-09-01

### Added
- Complete redesign of dashboard
- GraphQL API support

### Changed
- **BREAKING**: Renamed `create_user` to `createUser` for consistency
- **BREAKING**: Changed date format from `DD/MM/YYYY` to ISO 8601

### Removed
- **BREAKING**: Removed deprecated v1 API endpoints

[Unreleased]: https://github.com/user/project/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/user/project/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/user/project/releases/tag/v2.0.0
```

### Version Numbering

**Semantic Versioning (MAJOR.MINOR.PATCH)**:
- **MAJOR**: Breaking changes (2.0.0 → 3.0.0)
- **MINOR**: New features, backwards compatible (2.0.0 → 2.1.0)
- **PATCH**: Bug fixes, backwards compatible (2.0.0 → 2.0.1)

## Markdown Formatting

### Headers

```markdown
# H1 - Main title
## H2 - Section
### H3 - Subsection
#### H4 - Sub-subsection
```

### Emphasis

```markdown
**Bold text** or __bold__
*Italic text* or _italic_
***Bold and italic***
~~Strikethrough~~
`Inline code`
```

### Lists

```markdown
Unordered list:
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3

Ordered list:
1. First item
2. Second item
   1. Nested item
   2. Another nested item
3. Third item

Task list:
- [x] Completed task
- [ ] Incomplete task
```

### Links and Images

```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title text")

![Alt text](image.jpg)
![Alt text](image.jpg "Image title")
```

### Code Blocks

````markdown
Inline code: `const x = 5;`

Code block:
```javascript
function greet(name) {
  console.log(`Hello, ${name}!`);
}
```

With line highlighting:
```javascript {2}
function greet(name) {
  console.log(`Hello, ${name}!`); // This line is highlighted
}
```
````

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Data     | More     |

Alignment:
| Left | Center | Right |
|:-----|:------:|------:|
| L    | C      | R     |
```

### Blockquotes

```markdown
> Single line quote

> Multi-line
> quote with
> several lines

> **Note**: Important information
```

### Admonitions

```markdown
> **⚠️ Warning**: This action cannot be undone.

> **💡 Tip**: Use keyboard shortcuts to speed up your workflow.

> **🚨 Danger**: Never commit secrets to version control.

> **ℹ️ Info**: This feature requires Node.js 18+.
```

## Diagrams and Visuals

### When to Use Diagrams

**Use diagrams for**:
- System architecture
- Data flow
- Process flows
- Component relationships
- Complex concepts

**Don't use diagrams for**:
- Simple concepts (text is better)
- Things that change frequently
- Content that can be code

### Mermaid Diagrams

````markdown
```mermaid
graph TD
    A[User Request] --> B{Authenticated?}
    B -->|Yes| C[Process Request]
    B -->|No| D[Return 401]
    C --> E[Return Response]
```

```mermaid
sequenceDiagram
    Client->>API: POST /users
    API->>Database: INSERT user
    Database-->>API: User created
    API->>Email: Send welcome email
    API-->>Client: 201 Created
```
````

### ASCII Diagrams

```markdown
┌─────────────┐      ┌──────────────┐      ┌──────────┐
│   Client    │─────▶│   API Server │─────▶│ Database │
│  (Browser)  │◀─────│   (Express)  │◀─────│ (Postgres)│
└─────────────┘      └──────────────┘      └──────────┘
```

## Progressive Disclosure

### Start Simple, Add Details

```markdown
## Installation

Install via npm:

```bash
npm install package-name
```

<details>
<summary>Advanced installation options</summary>

### Install from source

```bash
git clone https://github.com/user/package.git
cd package
npm install
npm run build
npm link
```

### Install specific version

```bash
npm install package-name@2.1.0
```

### Install with peer dependencies

```bash
npm install package-name react react-dom
```
</details>
```

### Organize by Skill Level

```markdown
## Quick Start (Beginner)

Get up and running in 5 minutes:

[Simple example]

## Advanced Usage

For experienced users:

[Complex example]

## Expert Topics

Deep dive into internals:

[Very advanced example]
```

## User-Focused Language

### Address the Reader

```markdown
❌ Impersonal: The configuration file should be updated.
✅ Personal: Update your configuration file.

❌ Distant: One must install the dependencies.
✅ Direct: Install the dependencies.
```

### Use "You" Not "We"

```markdown
❌ We: Now we'll create a new user.
✅ You: Now you'll create a new user.

❌ We: We recommend using TypeScript.
✅ You: We recommend you use TypeScript.
```

### Be Helpful

```markdown
❌ Vague: An error occurred.
✅ Helpful: Connection failed. Check your network and try again.

❌ Blaming: You entered invalid data.
✅ Helpful: The email field requires a valid email address (e.g., user@example.com).
```

## Avoiding Jargon

### Define Technical Terms

```markdown
❌ Assumes knowledge:
"Use the ORM to query the RDBMS."

✅ Explains terms:
"Use the ORM (Object-Relational Mapping tool) to query the database.
An ORM lets you interact with your database using code instead of SQL."
```

### Use Common Words

```markdown
❌ Technical jargon:
"Leverage the API to facilitate data ingestion."

✅ Plain English:
"Use the API to import data."
```

## Version Documentation

### Document Version Changes

```markdown
## Version Compatibility

| Version | Node.js | Features |
|---------|---------|----------|
| 3.x     | 18+     | Full feature set |
| 2.x     | 16+     | Legacy API (deprecated) |
| 1.x     | 14+     | No longer supported |

## Upgrading from 2.x to 3.x

### Breaking Changes

**1. Renamed functions**

```typescript
// v2.x
import { create_user } from 'package';

// v3.x
import { createUser } from 'package';
```

**2. Changed date format**

Dates now use ISO 8601 format:
- Old: `01/15/2025`
- New: `2025-01-15T00:00:00Z`

### Migration Guide

1. Update imports:
   ```bash
   # Run this command to update your code
   npx package-migrate-v3
   ```

2. Update date handling:
   ```typescript
   // Before
   const date = '01/15/2025';

   // After
   const date = '2025-01-15T00:00:00Z';
   ```

3. Test thoroughly before deploying.
```

## Documentation Checklist

**Before Writing**:
- [ ] Who is the audience (beginner/intermediate/expert)?
- [ ] What do they need to accomplish?
- [ ] What do they already know?

**While Writing**:
- [ ] Use active voice
- [ ] Use simple language
- [ ] Be concise
- [ ] Provide examples
- [ ] Show expected output

**After Writing**:
- [ ] Read it aloud
- [ ] Have someone else review it
- [ ] Test all code examples
- [ ] Check all links
- [ ] Spell check

## When to Use This Skill

Use this skill when:
- Writing project READMEs
- Creating API documentation
- Writing tutorials
- Documenting code
- Creating user guides
- Writing changelogs
- Contributing to open source
- Creating internal documentation
- Writing blog posts about technical topics
- Training others on technical writing

---

**Remember**: Good documentation is empathetic. Always write for the person reading your docs at 2 AM who just wants to get their code working. Be clear, be helpful, and be kind.
