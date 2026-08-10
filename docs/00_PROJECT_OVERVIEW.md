# LedgerFlow — Project Overview

## 1. Project

LedgerFlow is a production-oriented high-throughput wallet and financial ledger backend built with:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- JWT
- Docker
- Pytest

The system provides secure user authentication, wallet management, wallet-to-wallet transfers, double-entry ledger accounting, idempotent transaction processing, concurrency protection, caching, rate limiting, testing, observability, and production deployment.

---

# 2. Engineering Goal

LedgerFlow should not be treated as a simple CRUD application.

The primary goal is to demonstrate production backend engineering concepts:

- Authentication and authorization
- Database integrity
- Financial precision
- Atomic transactions
- Concurrency control
- Idempotency
- Double-entry accounting
- Redis
- Rate limiting
- Database migrations
- Automated testing
- Containerization
- Observability
- Security
- API documentation
- Production deployment

Correctness is more important than feature count.

---

# 3. Core Architecture

The target architecture is:

Client
    |
    v
FastAPI API
    |
    +-------------------+
    |                   |
    v                   v
PostgreSQL            Redis
    |
    +-------------------+
    |
    v
Ledger / Wallet / Transaction data

The application follows a modular architecture:

API Layer
    |
Service Layer
    |
Repository / Database Layer
    |
PostgreSQL

Cross-cutting concerns:

- Authentication
- Authorization
- Validation
- Error handling
- Logging
- Metrics
- Rate limiting
- Idempotency
- Transactions

---

# 4. Core Financial Principle

Money must never be represented using floating-point types.

Use:

NUMERIC(18,2)

or an equivalent fixed-precision Decimal representation.

Never use:

float
double

for wallet balances or transaction amounts.

---

# 5. Transaction Correctness

Every transfer must satisfy:

1. Sender wallet exists.
2. Receiver wallet exists.
3. Sender and receiver are valid.
4. Amount is positive.
5. Currency matches.
6. Sender has sufficient balance.
7. Sender balance is debited.
8. Receiver balance is credited.
9. Transaction record is created.
10. Ledger entries are created.
11. All changes happen inside ONE database transaction.
12. Either everything succeeds or everything rolls back.

No partial transfer is allowed.

---

# 6. Double-Entry Principle

Every successful transfer creates at least two ledger entries.

Example:

Transfer ₹500:

Sender:

DEBIT 500

Receiver:

CREDIT 500

Total debits must equal total credits.

The ledger is the accounting source of truth.

Wallet balance is the current operational balance.

---

# 7. Idempotency

Financial operations must be safe against duplicate requests.

The transfer API must accept an idempotency key.

Example:

POST /transactions/transfer

Header:

Idempotency-Key: abc-123

If the same key is submitted again for the same operation:

- Do not execute the transfer again.
- Return the original result.

Idempotency must be enforced at the database level using a unique constraint.

---

# 8. Concurrency

Concurrent transfers must not cause:

- Negative balances
- Double spending
- Lost updates
- Incorrect balances

Use PostgreSQL row-level locking where required.

Expected mechanism:

SELECT ... FOR UPDATE

Wallet rows involved in a transfer must be locked before modifying balances.

Lock ordering must be deterministic to reduce deadlock risk.

---

# 9. Database Rules

PostgreSQL is the source of truth.

Do not rely on application memory for financial state.

All important financial constraints should be enforced as close to the database as practical.

Use:

- Primary keys
- Foreign keys
- Unique constraints
- Check constraints
- NOT NULL constraints
- Database transactions
- Appropriate indexes

---

# 10. API Rules

All APIs should:

- Validate input using Pydantic.
- Return appropriate HTTP status codes.
- Use consistent response formats.
- Never expose passwords or password hashes.
- Never expose secrets.
- Use authentication for protected resources.
- Verify resource ownership.
- Return meaningful but safe errors.

---

# 11. Security Rules

Authentication:

JWT Bearer tokens.

Password storage:

bcrypt/passlib or another approved password hashing mechanism.

Never store plaintext passwords.

Never return password hashes through API responses.

Never expose JWT secrets.

Never commit `.env`.

Provide `.env.example`.

Sensitive authentication errors should not reveal whether a user exists.

---

# 12. Architecture Rules

Keep responsibilities separated.

Routers:

- HTTP layer
- Request validation
- Dependency injection
- Response handling

Services:

- Business logic
- Financial operations
- Transfer logic

Models:

- Database representation
- Database constraints

Schemas:

- API request/response validation

Core:

- Security
- Configuration
- Cross-cutting utilities

Do not put large business operations directly inside route functions.

---

# 13. Production Requirements

The final project should include:

- PostgreSQL
- Redis
- Alembic
- Docker
- Docker Compose
- Pytest
- Environment configuration
- Structured logging
- Health checks
- API documentation
- Error handling
- Security controls
- Database indexes
- Automated tests

---

# 14. Development Strategy

Implement the project chapter by chapter.

Do not implement future chapters early unless required by the current chapter.

For every chapter:

1. Inspect existing code.
2. Identify required changes.
3. Implement the chapter.
4. Run tests.
5. Run the application.
6. Verify API behavior.
7. Check database changes.
8. Update documentation.
9. Do not break previous functionality.

---

# 15. Definition of Done

A chapter is complete only when:

- Code is implemented.
- Existing functionality still works.
- Relevant tests pass.
- Database behavior is verified.
- API behavior is verified.
- Error cases are handled.
- Security implications are considered.
- Documentation is updated.

Do not mark a feature complete simply because the code was generated.

---

# 16. Antigravity Instructions

When implementing any chapter:

1. Read this project overview.
2. Read the current chapter.
3. Inspect the existing code before modifying it.
4. Never overwrite working functionality unnecessarily.
5. Follow the existing project architecture.
6. Make the smallest clean changes necessary.
7. Do not implement future chapters.
8. Run tests after changes.
9. Report all modified files.
10. Report tests performed.
11. Report remaining issues.
12. Do not claim completion without verification.

---

# 17. Final Target

The completed LedgerFlow system should support:

Authentication
    ↓
Users
    ↓
Wallets
    ↓
Transfers
    ↓
Transactions
    ↓
Double-entry Ledger
    ↓
Idempotency
    ↓
Concurrency Control
    ↓
Redis
    ↓
Testing
    ↓
Observability
    ↓
Docker
    ↓
Production Deployment