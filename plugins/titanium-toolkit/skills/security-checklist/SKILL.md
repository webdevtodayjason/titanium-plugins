---
name: security-checklist
description: Comprehensive security checklist covering OWASP Top 10, SQL injection, XSS, CSRF, authentication, authorization, secrets management, input validation, and security headers. Use when scanning for vulnerabilities, reviewing security, implementing authentication/authorization, or handling sensitive data.
---

# Security Checklist

This skill provides comprehensive security guidance to protect your applications from common vulnerabilities and attacks.

## OWASP Top 10 Vulnerabilities

### 1. Broken Access Control

**What it is**: Users can access resources or perform actions they shouldn't be authorized for.

**Examples**:
- Accessing another user's data by changing URL parameter
- Elevating privileges (user → admin)
- Bypassing authentication checks

**Prevention**:
```typescript
// ❌ BAD - No authorization check
app.get('/api/users/:id', async (req, res) => {
  const user = await db.user.findUnique({ where: { id: req.params.id } });
  res.json(user);
});

// ✅ GOOD - Verify ownership or admin
app.get('/api/users/:id', authenticate, async (req, res) => {
  const requestedId = req.params.id;
  const currentUserId = req.user.id;
  const isAdmin = req.user.role === 'admin';

  if (requestedId !== currentUserId && !isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const user = await db.user.findUnique({ where: { id: requestedId } });
  res.json(user);
});
```

**Checklist**:
- [ ] Enforce least privilege (deny by default)
- [ ] Verify user permissions on every request
- [ ] Never trust user IDs from client
- [ ] Log access control failures
- [ ] Use centralized access control logic

### 2. Cryptographic Failures

**What it is**: Exposing sensitive data due to weak or missing encryption.

**Examples**:
- Storing passwords in plain text
- Using weak hashing algorithms (MD5, SHA1)
- Transmitting sensitive data over HTTP

**Prevention**:
```typescript
import bcrypt from 'bcrypt';
import crypto from 'crypto';

// ✅ Password hashing
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12; // Increase for more security
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}

// ✅ Encrypt sensitive data at rest
function encrypt(text: string, key: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', Buffer.from(key), iv);

  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag().toString('hex');
  return `${iv.toString('hex')}:${authTag}:${encrypted}`;
}
```

**Checklist**:
- [ ] Use HTTPS everywhere
- [ ] Hash passwords with bcrypt (12+ rounds)
- [ ] Encrypt sensitive data at rest
- [ ] Use strong encryption algorithms (AES-256)
- [ ] Properly manage encryption keys
- [ ] Never commit secrets to version control

### 3. Injection Attacks

**See SQL Injection Prevention section below**

### 4. Insecure Design

**What it is**: Security flaws in the application architecture.

**Examples**:
- Missing rate limiting
- Unrestricted file uploads
- Insecure password reset flows

**Prevention**:
```typescript
// ✅ Rate limiting
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
});

app.post('/api/auth/login', loginLimiter, async (req, res) => {
  // Login logic
});

// ✅ Secure file upload
import multer from 'multer';

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB max
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    cb(null, true);
  },
});
```

**Checklist**:
- [ ] Implement rate limiting on all endpoints
- [ ] Validate file uploads (type, size, content)
- [ ] Use secure password reset flows (token-based)
- [ ] Implement account lockout after failed attempts
- [ ] Log and monitor security events

### 5. Security Misconfiguration

**What it is**: Insecure default configurations, unnecessary features enabled.

**Prevention**:
```typescript
// ✅ Secure Express configuration
import express from 'express';
import helmet from 'helmet';

const app = express();

// Security headers
app.use(helmet());

// Disable X-Powered-By
app.disable('x-powered-by');

// Environment-specific settings
if (process.env.NODE_ENV === 'production') {
  app.set('trust proxy', 1); // Trust first proxy
}

// CORS configuration
import cors from 'cors';

const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  credentials: true,
  optionsSuccessStatus: 200,
};

app.use(cors(corsOptions));
```

**Checklist**:
- [ ] Remove default accounts and passwords
- [ ] Disable directory listing
- [ ] Remove unnecessary features/endpoints
- [ ] Keep all software updated
- [ ] Use security headers (see section below)

### 6. Vulnerable and Outdated Components

**Prevention**:
```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix

# Update dependencies
npm update

# Use automated tools
npm install -g snyk
snyk test
snyk monitor
```

**Checklist**:
- [ ] Regularly update dependencies
- [ ] Monitor security advisories
- [ ] Remove unused dependencies
- [ ] Use dependabot or renovate
- [ ] Pin dependency versions in production

### 7. Identification and Authentication Failures

**See Authentication Best Practices section below**

### 8. Software and Data Integrity Failures

**Prevention**:
```typescript
// ✅ Verify package integrity
// package-lock.json ensures same versions

// ✅ Use Subresource Integrity (SRI) for CDN
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
  crossorigin="anonymous"
></script>

// ✅ Validate data from external sources
import { z } from 'zod';

const ExternalDataSchema = z.object({
  id: z.string().uuid(),
  amount: z.number().positive(),
  status: z.enum(['pending', 'completed', 'failed']),
});

function processExternalData(data: unknown) {
  const validated = ExternalDataSchema.parse(data);
  // Now safe to use
}
```

### 9. Security Logging and Monitoring Failures

**Prevention**:
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// ✅ Log security events
logger.warn('Failed login attempt', {
  email: req.body.email,
  ip: req.ip,
  userAgent: req.get('user-agent'),
  timestamp: new Date().toISOString(),
});

logger.error('SQL injection attempt detected', {
  query: sanitizedQuery,
  ip: req.ip,
  endpoint: req.path,
});
```

**Checklist**:
- [ ] Log authentication events (login, logout, failures)
- [ ] Log authorization failures
- [ ] Log input validation failures
- [ ] Monitor for suspicious patterns
- [ ] Set up alerts for security events

### 10. Server-Side Request Forgery (SSRF)

**Prevention**:
```typescript
import validator from 'validator';

// ❌ BAD - Allows SSRF
app.post('/api/fetch-url', async (req, res) => {
  const url = req.body.url;
  const response = await fetch(url);
  res.json(await response.json());
});

// ✅ GOOD - Validate and whitelist
app.post('/api/fetch-url', async (req, res) => {
  const url = req.body.url;

  // Validate URL format
  if (!validator.isURL(url, { protocols: ['https'] })) {
    return res.status(400).json({ error: 'Invalid URL' });
  }

  // Whitelist allowed domains
  const allowedDomains = ['api.trusted-service.com'];
  const urlObj = new URL(url);

  if (!allowedDomains.includes(urlObj.hostname)) {
    return res.status(403).json({ error: 'Domain not allowed' });
  }

  // Block internal IPs
  const hostname = urlObj.hostname;
  if (
    hostname === 'localhost' ||
    hostname.startsWith('192.168.') ||
    hostname.startsWith('10.') ||
    hostname.startsWith('172.')
  ) {
    return res.status(403).json({ error: 'Internal IPs not allowed' });
  }

  const response = await fetch(url);
  res.json(await response.json());
});
```

## SQL Injection Prevention

### Parameterized Queries

```typescript
// ❌ VULNERABLE - String concatenation
const email = req.body.email;
const query = `SELECT * FROM users WHERE email = '${email}'`;
// Attacker can input: ' OR '1'='1
// Resulting query: SELECT * FROM users WHERE email = '' OR '1'='1'

// ✅ SAFE - Parameterized query
const email = req.body.email;
const query = 'SELECT * FROM users WHERE email = ?';
const user = await db.execute(query, [email]);

// ✅ SAFE - ORM (Prisma)
const user = await prisma.user.findUnique({
  where: { email: req.body.email },
});
```

### Input Validation

```typescript
import { z } from 'zod';

const UserQuerySchema = z.object({
  email: z.string().email(),
  id: z.string().uuid().optional(),
  name: z.string().max(100).optional(),
});

app.get('/api/users', async (req, res) => {
  try {
    const params = UserQuerySchema.parse(req.query);
    const users = await db.user.findMany({ where: params });
    res.json(users);
  } catch (error) {
    res.status(400).json({ error: 'Invalid query parameters' });
  }
});
```

## XSS (Cross-Site Scripting) Prevention

### Types of XSS

**1. Stored XSS**: Malicious script stored in database
**2. Reflected XSS**: Malicious script in URL/input reflected back
**3. DOM-based XSS**: Script manipulates DOM directly

### Prevention

```typescript
// ✅ React automatically escapes by default
function Comment({ text }: { text: string }) {
  return <p>{text}</p>; // Safe - React escapes HTML
}

// ❌ DANGEROUS - dangerouslySetInnerHTML
function Comment({ html }: { html: string }) {
  return <p dangerouslySetInnerHTML={{ __html: html }} />; // UNSAFE
}

// ✅ Sanitize HTML before rendering
import DOMPurify from 'dompurify';

function Comment({ html }: { html: string }) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href'],
  });
  return <p dangerouslySetInnerHTML={{ __html: clean }} />;
}

// ✅ Server-side sanitization
import sanitizeHtml from 'sanitize-html';

app.post('/api/comments', async (req, res) => {
  const clean = sanitizeHtml(req.body.content, {
    allowedTags: ['b', 'i', 'em', 'strong', 'a'],
    allowedAttributes: {
      'a': ['href'],
    },
  });

  const comment = await db.comment.create({
    data: { content: clean },
  });

  res.json(comment);
});
```

### Content Security Policy (CSP)

```typescript
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", 'https://trusted-cdn.com'],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.example.com'],
      fontSrc: ["'self'", 'https://fonts.gstatic.com'],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  })
);
```

## CSRF (Cross-Site Request Forgery) Protection

### CSRF Token Pattern

```typescript
import csrf from 'csurf';
import cookieParser from 'cookie-parser';

const csrfProtection = csrf({ cookie: true });

app.use(cookieParser());

// Get CSRF token
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// Protect state-changing endpoints
app.post('/api/users', csrfProtection, async (req, res) => {
  // Token automatically verified by middleware
  const user = await createUser(req.body);
  res.json(user);
});
```

### SameSite Cookies

```typescript
// ✅ Set SameSite attribute
res.cookie('sessionId', token, {
  httpOnly: true,
  secure: true, // HTTPS only
  sameSite: 'strict', // or 'lax'
  maxAge: 24 * 60 * 60 * 1000, // 24 hours
});
```

## Authentication Best Practices

### Password Requirements

```typescript
import { z } from 'zod';

const PasswordSchema = z
  .string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Password must contain uppercase letter')
  .regex(/[a-z]/, 'Password must contain lowercase letter')
  .regex(/[0-9]/, 'Password must contain number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain special character');

// Check against common passwords
import { isCommonPassword } from 'common-passwords';

function validatePassword(password: string): boolean {
  if (isCommonPassword(password)) {
    throw new Error('Password is too common');
  }
  return true;
}
```

### JWT Best Practices

```typescript
import jwt from 'jsonwebtoken';

// ✅ Short-lived access tokens
function generateAccessToken(userId: string): string {
  return jwt.sign(
    { userId, type: 'access' },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' } // Short expiry
  );
}

// ✅ Long-lived refresh tokens
function generateRefreshToken(userId: string): string {
  return jwt.sign(
    { userId, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }
  );
}

// ✅ Verify token
function verifyAccessToken(token: string) {
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    if (payload.type !== 'access') {
      throw new Error('Invalid token type');
    }
    return payload;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// ✅ Blacklist tokens on logout
const tokenBlacklist = new Set<string>();

app.post('/api/auth/logout', authenticate, (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (token) {
    tokenBlacklist.add(token);
  }
  res.json({ message: 'Logged out' });
});
```

### Multi-Factor Authentication (MFA)

```typescript
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

// Generate MFA secret
async function enableMFA(userId: string) {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${user.email})`,
  });

  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url!);

  // Save secret to database (encrypted)
  await db.user.update({
    where: { id: userId },
    data: { mfaSecret: encrypt(secret.base32) },
  });

  return { secret: secret.base32, qrCode };
}

// Verify MFA token
function verifyMFAToken(secret: string, token: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 2, // Allow 2 time steps before/after
  });
}
```

## Authorization Patterns

### Role-Based Access Control (RBAC)

```typescript
enum Role {
  USER = 'user',
  MODERATOR = 'moderator',
  ADMIN = 'admin',
}

const permissions = {
  [Role.USER]: ['read:own', 'write:own'],
  [Role.MODERATOR]: ['read:own', 'write:own', 'read:all', 'delete:others'],
  [Role.ADMIN]: ['*'], // All permissions
};

function authorize(requiredPermission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.user.role;
    const userPermissions = permissions[userRole];

    if (!userPermissions.includes('*') && !userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

// Usage
app.delete('/api/posts/:id', authenticate, authorize('delete:others'), async (req, res) => {
  await deletePost(req.params.id);
  res.json({ success: true });
});
```

### Attribute-Based Access Control (ABAC)

```typescript
interface AccessPolicy {
  subject: { role: string; department?: string };
  resource: { type: string; owner?: string };
  action: string;
  conditions?: Record<string, any>;
}

function checkAccess(
  user: User,
  resource: Resource,
  action: string
): boolean {
  // User can access own resources
  if (resource.ownerId === user.id) {
    return true;
  }

  // Admins can access everything
  if (user.role === 'admin') {
    return true;
  }

  // Department managers can access department resources
  if (
    user.role === 'manager' &&
    user.department === resource.department
  ) {
    return true;
  }

  return false;
}
```

## Secrets Management

### Environment Variables

```typescript
// ✅ .env file (NOT committed to git)
DATABASE_URL=postgresql://user:password@localhost:5432/db
JWT_SECRET=super-secret-key-change-in-production
API_KEY=sk_live_abc123xyz

// ✅ .env.example (committed to git)
DATABASE_URL=
JWT_SECRET=
API_KEY=

// ✅ Load environment variables
import dotenv from 'dotenv';
dotenv.config();

// ✅ Validate required env vars
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

### Key Vault Integration

```typescript
// ✅ AWS Secrets Manager
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

async function getSecret(secretName: string): Promise<string> {
  const client = new SecretsManager({ region: 'us-east-1' });
  const response = await client.getSecretValue({ SecretId: secretName });
  return response.SecretString!;
}

// ✅ Azure Key Vault
import { SecretClient } from '@azure/keyvault-secrets';

async function getAzureSecret(secretName: string): Promise<string> {
  const client = new SecretClient(vaultUrl, credential);
  const secret = await client.getSecret(secretName);
  return secret.value!;
}
```

## Input Validation

### Validation Schema

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).max(100),
  name: z.string().min(1).max(100),
  age: z.number().int().min(18).max(120),
  phone: z.string().regex(/^\+?[1-9]\d{1,14}$/).optional(),
  website: z.string().url().optional(),
});

app.post('/api/users', async (req, res) => {
  try {
    const data = CreateUserSchema.parse(req.body);
    const user = await createUser(data);
    res.json(user);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.errors,
      });
    }
    throw error;
  }
});
```

### Sanitization

```typescript
import validator from 'validator';

function sanitizeInput(input: string): string {
  // Trim whitespace
  let clean = input.trim();

  // Escape HTML entities
  clean = validator.escape(clean);

  // Remove null bytes
  clean = clean.replace(/\0/g, '');

  return clean;
}
```

## Security Headers

### Comprehensive Header Configuration

```typescript
import helmet from 'helmet';

app.use(
  helmet({
    // Content Security Policy
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },

    // HTTP Strict Transport Security
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true,
    },

    // X-Frame-Options
    frameguard: {
      action: 'deny', // or 'sameorigin'
    },

    // X-Content-Type-Options
    noSniff: true,

    // X-XSS-Protection
    xssFilter: true,

    // Referrer-Policy
    referrerPolicy: {
      policy: 'strict-origin-when-cross-origin',
    },
  })
);

// Additional custom headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  next();
});
```

## Rate Limiting

### Endpoint-Specific Rate Limits

```typescript
import rateLimit from 'express-rate-limit';

// Strict limit for authentication
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5,
  message: 'Too many authentication attempts',
  standardHeaders: true,
  legacyHeaders: false,
});

// Moderate limit for API endpoints
const apiLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 60,
  message: 'Too many requests',
});

// Apply rate limiters
app.post('/api/auth/login', authLimiter, loginHandler);
app.post('/api/auth/register', authLimiter, registerHandler);
app.use('/api', apiLimiter);
```

## Logging Security Events

### What NOT to Log

**❌ Never log**:
- Passwords (plain or hashed)
- Credit card numbers
- Social Security numbers
- API keys/secrets
- Session tokens
- Personally identifiable information (PII) in clear text

```typescript
// ❌ BAD - Logs sensitive data
logger.info('User login', { email, password });

// ✅ GOOD - Logs non-sensitive data
logger.info('User login attempt', {
  email,
  ip: req.ip,
  userAgent: req.get('user-agent'),
  success: true,
});
```

### Security Event Logging

```typescript
enum SecurityEvent {
  LOGIN_SUCCESS = 'login_success',
  LOGIN_FAILURE = 'login_failure',
  PASSWORD_RESET = 'password_reset',
  ACCOUNT_LOCKED = 'account_locked',
  PERMISSION_DENIED = 'permission_denied',
  SUSPICIOUS_ACTIVITY = 'suspicious_activity',
}

function logSecurityEvent(
  event: SecurityEvent,
  userId: string | null,
  metadata: Record<string, any>
) {
  logger.warn({
    type: 'security',
    event,
    userId,
    timestamp: new Date().toISOString(),
    ip: metadata.ip,
    userAgent: metadata.userAgent,
    ...metadata,
  });
}
```

## Dependency Scanning

### Automated Security Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0' # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
```

## Security Checklist Summary

### Pre-Deployment Checklist

**Authentication & Authorization**:
- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] JWT tokens have short expiry (15 minutes)
- [ ] Refresh tokens properly implemented
- [ ] MFA available for sensitive accounts
- [ ] Authorization checks on all endpoints
- [ ] Rate limiting on auth endpoints

**Input Validation**:
- [ ] All inputs validated with schemas
- [ ] SQL queries use parameterized statements
- [ ] File uploads restricted (type, size)
- [ ] HTML content sanitized
- [ ] No eval() or Function() with user input

**Security Headers**:
- [ ] HTTPS enforced
- [ ] CSP configured
- [ ] HSTS enabled
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options set

**Data Protection**:
- [ ] Sensitive data encrypted at rest
- [ ] Secrets stored in environment variables/vault
- [ ] No secrets in version control
- [ ] PII handled according to regulations
- [ ] Database backups encrypted

**Logging & Monitoring**:
- [ ] Security events logged
- [ ] No sensitive data in logs
- [ ] Failed auth attempts monitored
- [ ] Unusual activity alerts configured
- [ ] Log retention policy defined

**Dependencies**:
- [ ] All dependencies up to date
- [ ] No known vulnerabilities (npm audit)
- [ ] Dependabot/Renovate configured
- [ ] Unused dependencies removed

**API Security**:
- [ ] CORS properly configured
- [ ] CSRF protection enabled
- [ ] Rate limiting implemented
- [ ] API keys rotated regularly
- [ ] Endpoints documented

## When to Use This Skill

Use this skill when:
- Conducting security audits
- Implementing authentication/authorization
- Reviewing code for vulnerabilities
- Setting up new projects
- Handling sensitive data
- Responding to security incidents
- Training team on security
- Preparing for compliance audits
- Deploying to production
- Integrating third-party services

---

**Remember**: Security is not a one-time task but an ongoing process. Stay informed about new vulnerabilities, keep dependencies updated, and always assume malicious actors are trying to exploit your application.
