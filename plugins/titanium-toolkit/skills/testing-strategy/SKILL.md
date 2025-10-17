---
name: testing-strategy
description: Comprehensive testing strategies including test pyramid, TDD methodology, testing patterns, coverage goals, and CI/CD integration. Use when writing tests, implementing TDD, reviewing test coverage, debugging test failures, or setting up testing infrastructure.
---

# Testing Strategy

This skill provides comprehensive guidance for implementing effective testing strategies across your entire application stack.

## Test Pyramid

### The Testing Hierarchy

```
        /\
       /  \
      /E2E \       10% - End-to-End Tests (slowest, most expensive)
     /______\
    /        \
   /Integration\  20% - Integration Tests (medium speed/cost)
  /____________\
 /              \
/   Unit Tests   \ 70% - Unit Tests (fast, cheap, focused)
/__________________\
```

**Rationale**:
- **70% Unit Tests**: Fast, isolated, catch bugs early
- **20% Integration Tests**: Test component interactions
- **10% E2E Tests**: Test critical user journeys

### Why This Distribution?

**Unit tests are cheap**:
- Run in milliseconds
- No external dependencies
- Easy to debug
- High code coverage per test

**Integration tests are moderate**:
- Test real interactions
- Catch integration bugs
- Slower than unit tests
- More complex setup

**E2E tests are expensive**:
- Test entire system
- Catch UX issues
- Very slow (seconds/minutes)
- Brittle and hard to maintain

## TDD (Test-Driven Development)

### Red-Green-Refactor Cycle

**1. Red - Write a failing test**:
```typescript
describe('Calculator', () => {
  test('adds two numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5); // FAILS - method doesn't exist
  });
});
```

**2. Green - Write minimal code to pass**:
```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b; // Simplest implementation
  }
}
// Test now PASSES
```

**3. Refactor - Improve the code**:
```typescript
class Calculator {
  add(a: number, b: number): number {
    // Add validation
    if (!Number.isFinite(a) || !Number.isFinite(b)) {
      throw new Error('Arguments must be finite numbers');
    }
    return a + b;
  }
}
```

### TDD Benefits

**Design benefits**:
- Forces you to think about API before implementation
- Leads to more testable, modular code
- Encourages SOLID principles

**Quality benefits**:
- 100% test coverage by design
- Catches bugs immediately
- Provides living documentation

**Workflow benefits**:
- Clear next step (make test pass)
- Confidence when refactoring
- Prevents over-engineering

## Arrange-Act-Assert Pattern

### The AAA Pattern

Every test should follow this structure:

```typescript
test('user registration creates account and sends welcome email', async () => {
  // ARRANGE - Set up test conditions
  const userData = {
    email: 'test@example.com',
    password: 'SecurePass123',
    name: 'Test User',
  };
  const mockEmailService = jest.fn();
  const userService = new UserService(mockEmailService);

  // ACT - Execute the behavior being tested
  const result = await userService.register(userData);

  // ASSERT - Verify the outcome
  expect(result.id).toBeDefined();
  expect(result.email).toBe(userData.email);
  expect(mockEmailService).toHaveBeenCalledWith({
    to: userData.email,
    subject: 'Welcome!',
    template: 'welcome',
  });
});
```

### Why AAA?

- **Clear structure**: Easy to understand what's being tested
- **Consistent**: All tests follow same pattern
- **Maintainable**: Easy to modify and debug

## Mocking Strategies

### When to Mock

**✅ DO mock**:
- External APIs
- Databases
- File system operations
- Time/dates
- Random number generators
- Network requests
- Third-party services

```typescript
// Mock external API
jest.mock('axios');

test('fetches user data from API', async () => {
  const mockData = { id: 1, name: 'John' };
  (axios.get as jest.Mock).mockResolvedValue({ data: mockData });

  const user = await fetchUser(1);

  expect(user).toEqual(mockData);
});
```

### When NOT to Mock

**❌ DON'T mock**:
- Pure functions (test them directly)
- Simple utility functions
- Domain logic
- Value objects
- Internal implementation details

```typescript
// ❌ BAD - Over-mocking
test('validates email', () => {
  const validator = new EmailValidator();
  jest.spyOn(validator, 'isValid').mockReturnValue(true);
  expect(validator.isValid('test@example.com')).toBe(true);
  // This test is useless - you're testing the mock, not the code
});

// ✅ GOOD - Test real implementation
test('validates email', () => {
  const validator = new EmailValidator();
  expect(validator.isValid('test@example.com')).toBe(true);
  expect(validator.isValid('invalid')).toBe(false);
});
```

### Mocking Patterns

**Stub** (return predetermined values):
```typescript
const mockDatabase = {
  findUser: jest.fn().mockResolvedValue({ id: 1, name: 'John' }),
  saveUser: jest.fn().mockResolvedValue(true),
};
```

**Spy** (track calls, use real implementation):
```typescript
const emailService = new EmailService();
const sendSpy = jest.spyOn(emailService, 'send');

await emailService.send('test@example.com', 'Hello');

expect(sendSpy).toHaveBeenCalledTimes(1);
expect(sendSpy).toHaveBeenCalledWith('test@example.com', 'Hello');
```

**Fake** (lightweight implementation):
```typescript
class FakeDatabase {
  private data = new Map();

  async save(key: string, value: any) {
    this.data.set(key, value);
  }

  async get(key: string) {
    return this.data.get(key);
  }
}
```

## Test Coverage Goals

### Coverage Metrics

**Line Coverage**: Percentage of code lines executed
- **Target**: 80-90% for critical paths

**Branch Coverage**: Percentage of if/else branches tested
- **Target**: 80%+ (more important than line coverage)

**Function Coverage**: Percentage of functions called
- **Target**: 90%+

**Statement Coverage**: Percentage of statements executed
- **Target**: 80%+

### Coverage Configuration

```json
// package.json
{
  "jest": {
    "collectCoverage": true,
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 90,
        "lines": 80,
        "statements": 80
      },
      "./src/critical/": {
        "branches": 95,
        "functions": 95,
        "lines": 95,
        "statements": 95
      }
    },
    "coveragePathIgnorePatterns": [
      "/node_modules/",
      "/tests/",
      "/migrations/",
      "/.config.ts$/"
    ]
  }
}
```

### What to Prioritize

**High priority** (aim for 95%+ coverage):
- Business logic
- Security-critical code
- Payment/billing code
- Data validation
- Authentication/authorization

**Medium priority** (aim for 80%+ coverage):
- API endpoints
- Database queries
- Utility functions
- Error handling

**Low priority** (optional coverage):
- UI components (use integration tests instead)
- Configuration files
- Type definitions
- Third-party library wrappers

## Integration Testing

### Database Integration Tests

```typescript
import { PrismaClient } from '@prisma/client';

describe('UserRepository', () => {
  let prisma: PrismaClient;
  let repository: UserRepository;

  beforeAll(async () => {
    // Use test database
    prisma = new PrismaClient({
      datasources: { db: { url: process.env.TEST_DATABASE_URL } },
    });
    repository = new UserRepository(prisma);
  });

  beforeEach(async () => {
    // Clean database before each test
    await prisma.user.deleteMany();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  test('creates user and retrieves by email', async () => {
    // ARRANGE
    const userData = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'hashed_password',
    };

    // ACT
    const created = await repository.create(userData);
    const retrieved = await repository.findByEmail(userData.email);

    // ASSERT
    expect(retrieved).toBeDefined();
    expect(retrieved?.id).toBe(created.id);
    expect(retrieved?.email).toBe(userData.email);
  });
});
```

### API Integration Tests

```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('User API', () => {
  test('POST /api/users creates user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123',
        name: 'Test User',
      })
      .expect(201);

    expect(response.body).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
    expect(response.body.password).toBeUndefined(); // Never return password
  });

  test('POST /api/users returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid-email',
        password: 'SecurePass123',
        name: 'Test User',
      })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

### Service Integration Tests

```typescript
describe('OrderService Integration', () => {
  test('complete order flow', async () => {
    // Create order
    const order = await orderService.create({
      userId: 'user_123',
      items: [{ productId: 'prod_1', quantity: 2 }],
    });

    // Process payment
    const payment = await paymentService.process({
      orderId: order.id,
      amount: order.total,
    });

    // Verify inventory updated
    const product = await inventoryService.getProduct('prod_1');
    expect(product.stock).toBe(originalStock - 2);

    // Verify order status updated
    const updatedOrder = await orderService.getById(order.id);
    expect(updatedOrder.status).toBe('paid');
  });
});
```

## E2E Testing

### Playwright Setup

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
});
```

### E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('user can register and login', async ({ page }) => {
    // Navigate to registration page
    await page.goto('/register');

    // Fill registration form
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123');
    await page.fill('[name="confirmPassword"]', 'SecurePass123');
    await page.fill('[name="name"]', 'Test User');

    // Submit form
    await page.click('button[type="submit"]');

    // Wait for redirect to dashboard
    await page.waitForURL('/dashboard');

    // Verify welcome message
    await expect(page.locator('h1')).toContainText('Welcome, Test User');
  });

  test('shows validation errors for invalid input', async ({ page }) => {
    await page.goto('/register');

    await page.fill('[name="email"]', 'invalid-email');
    await page.fill('[name="password"]', '123'); // Too short

    await page.click('button[type="submit"]');

    // Verify error messages displayed
    await expect(page.locator('[data-testid="email-error"]'))
      .toContainText('Invalid email');
    await expect(page.locator('[data-testid="password-error"]'))
      .toContainText('at least 8 characters');
  });
});
```

### Critical E2E Scenarios

Test these critical user journeys:
- User registration and login
- Checkout and payment flow
- Password reset
- Profile updates
- Critical business workflows

## Performance Testing

### Load Testing with k6

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up to 20 users
    { duration: '1m', target: 20 },    // Stay at 20 users
    { duration: '30s', target: 100 },  // Ramp up to 100 users
    { duration: '1m', target: 100 },   // Stay at 100 users
    { duration: '30s', target: 0 },    // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% error rate
  },
};

export default function() {
  const response = http.get('https://api.example.com/users');

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

### Benchmark Testing

```typescript
import { performance } from 'perf_hooks';

describe('Performance Benchmarks', () => {
  test('database query completes in under 100ms', async () => {
    const start = performance.now();

    await database.query('SELECT * FROM users WHERE email = ?', ['test@example.com']);

    const duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });

  test('API endpoint responds in under 200ms', async () => {
    const start = performance.now();

    await request(app).get('/api/users/123');

    const duration = performance.now() - start;
    expect(duration).toBeLessThan(200);
  });
});
```

## Flaky Test Prevention

### Common Causes of Flaky Tests

**1. Race Conditions**:
```typescript
// ❌ BAD - Race condition
test('displays data', async () => {
  fetchData();
  expect(screen.getByText('Data loaded')).toBeInTheDocument();
  // Fails intermittently if fetchData takes longer than expected
});

// ✅ GOOD - Wait for async operation
test('displays data', async () => {
  fetchData();
  await screen.findByText('Data loaded'); // Waits up to 1 second
});
```

**2. Time Dependencies**:
```typescript
// ❌ BAD - Depends on current time
test('shows message for new users', () => {
  const user = { createdAt: new Date() };
  expect(isNewUser(user)).toBe(true);
  // Fails if test runs slowly
});

// ✅ GOOD - Mock time
test('shows message for new users', () => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2025-10-16'));

  const user = { createdAt: new Date('2025-10-15') };
  expect(isNewUser(user)).toBe(true);

  jest.useRealTimers();
});
```

**3. Shared State**:
```typescript
// ❌ BAD - Tests share state
let counter = 0;

test('increments counter', () => {
  counter++;
  expect(counter).toBe(1);
});

test('increments counter again', () => {
  counter++;
  expect(counter).toBe(1); // Fails if first test ran
});

// ✅ GOOD - Isolated state
test('increments counter', () => {
  const counter = new Counter();
  counter.increment();
  expect(counter.value).toBe(1);
});
```

### Flaky Test Best Practices

1. **Always clean up after tests**:
```typescript
afterEach(async () => {
  await database.truncate();
  jest.clearAllMocks();
  jest.useRealTimers();
});
```

2. **Use explicit waits, not delays**:
```typescript
// ❌ BAD
await sleep(1000);

// ✅ GOOD
await waitFor(() => expect(element).toBeInTheDocument());
```

3. **Isolate test data**:
```typescript
test('creates user', async () => {
  const uniqueEmail = `test-${Date.now()}@example.com`;
  const user = await createUser({ email: uniqueEmail });
  expect(user.email).toBe(uniqueEmail);
});
```

## Test Data Management

### Test Fixtures

```typescript
// fixtures/users.ts
export const testUsers = {
  admin: {
    email: 'admin@example.com',
    password: 'AdminPass123',
    role: 'admin',
  },
  regular: {
    email: 'user@example.com',
    password: 'UserPass123',
    role: 'user',
  },
};

// Usage in tests
import { testUsers } from './fixtures/users';

test('admin can delete users', async () => {
  const admin = await createUser(testUsers.admin);
  // Test admin functionality
});
```

### Factory Pattern

```typescript
class UserFactory {
  static create(overrides = {}) {
    return {
      id: faker.datatype.uuid(),
      email: faker.internet.email(),
      name: faker.name.fullName(),
      createdAt: new Date(),
      ...overrides,
    };
  }

  static createMany(count: number, overrides = {}) {
    return Array.from({ length: count }, () => this.create(overrides));
  }
}

// Usage
test('displays user list', () => {
  const users = UserFactory.createMany(5);
  render(<UserList users={users} />);
  expect(screen.getAllByRole('listitem')).toHaveLength(5);
});
```

### Database Seeding

```typescript
// seeds/test-seed.ts
export async function seedTestDatabase() {
  // Create admin user
  const admin = await prisma.user.create({
    data: { email: 'admin@test.com', role: 'admin' },
  });

  // Create test products
  const products = await Promise.all([
    prisma.product.create({ data: { name: 'Product 1', price: 10 } }),
    prisma.product.create({ data: { name: 'Product 2', price: 20 } }),
  ]);

  return { admin, products };
}

// Usage
beforeEach(async () => {
  await prisma.$executeRaw`TRUNCATE TABLE users CASCADE`;
  const { admin, products } = await seedTestDatabase();
});
```

## CI/CD Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          fail_ci_if_error: true
```

### Test Scripts Organization

```json
// package.json
{
  "scripts": {
    "test": "npm run test:unit && npm run test:integration && npm run test:e2e",
    "test:unit": "jest --testPathPattern=\\.test\\.ts$",
    "test:integration": "jest --testPathPattern=\\.integration\\.ts$",
    "test:e2e": "playwright test",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2"
  }
}
```

### Test Performance in CI

**Parallel execution**:
```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

**Cache dependencies**:
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

## Test Organization

### File Structure

```
tests/
├── unit/                   # Fast, isolated tests
│   ├── services/
│   │   ├── user-service.test.ts
│   │   └── order-service.test.ts
│   └── utils/
│       ├── validator.test.ts
│       └── formatter.test.ts
├── integration/            # Database, API tests
│   ├── api/
│   │   ├── users.integration.ts
│   │   └── orders.integration.ts
│   └── database/
│       └── repository.integration.ts
├── e2e/                   # End-to-end tests
│   ├── auth.spec.ts
│   ├── checkout.spec.ts
│   └── profile.spec.ts
├── fixtures/              # Test data
│   ├── users.ts
│   └── products.ts
└── helpers/               # Test utilities
    ├── setup.ts
    └── factories.ts
```

### Test Naming Conventions

```typescript
// Pattern: describe('Component/Function', () => test('should...when...'))

describe('UserService', () => {
  describe('register', () => {
    test('should create user when valid data provided', async () => {
      // Test implementation
    });

    test('should throw error when email already exists', async () => {
      // Test implementation
    });

    test('should hash password before saving', async () => {
      // Test implementation
    });
  });

  describe('login', () => {
    test('should return token when credentials are valid', async () => {
      // Test implementation
    });

    test('should throw error when password is incorrect', async () => {
      // Test implementation
    });
  });
});
```

## When to Use This Skill

Use this skill when:
- Setting up testing infrastructure
- Writing unit, integration, or E2E tests
- Implementing TDD methodology
- Reviewing test coverage
- Debugging flaky tests
- Optimizing test performance
- Configuring CI/CD pipelines
- Establishing testing standards
- Training team on testing practices
- Improving code quality through testing

---

**Remember**: Good tests give you confidence to refactor, catch bugs early, and serve as living documentation. Invest in your test suite and it will pay dividends throughout the project lifecycle.
