# Chapter 01 — Foundation

## Objective

Stabilize the existing LedgerFlow project before adding new business functionality.

This chapter must not implement transactions, ledger, Redis, or Docker.

---

## Current State

Already implemented:

- FastAPI application
- PostgreSQL
- SQLAlchemy
- User model
- User registration
- Password hashing
- Login
- JWT creation
- JWT verification
- get_user()
- Wallet model

---

# Tasks

## 1. Project Dependencies

Create:

requirements.txt

It must contain all direct runtime and development dependencies.

Do not blindly depend on packages that are not actually used.

---

## 2. Environment Configuration

Create:

.env.example

It must document required variables without containing real credentials.

Example categories:

DATABASE configuration
JWT configuration
Redis configuration

Never commit real secrets.

---

## 3. Database Configuration

Move database host and port into configuration.

Avoid hardcoding:

localhost
5432

Database URL should be constructed from configuration.

---

## 4. Authentication Security

Fix JWT verification.

Invalid JWT:

HTTP 401

Expired JWT:

HTTP 401

Tampered JWT:

HTTP 401

Never return JWT exceptions as normal values.

---

## 5. User Email

Make email unique and non-null.

Duplicate registration must fail safely.

---

## 6. Login Errors

Wrong email:

401

Wrong password:

401

Both should return the same generic message.

Do not expose account existence.

---

## 7. Wallet Model Registration

Ensure all models are imported before metadata operations.

Wallet must be visible to SQLAlchemy metadata.

---

## 8. Wallet Balance

New wallets start at:

0.00

Use Decimal/Numeric.

Never use float.

---

## 9. Code Quality

Fix:

- duplicate assignments
- inconsistent imports
- incorrect naming
- unused imports
- unsafe exception handling

Do not perform unrelated refactoring.

---

# Verification

Verify:

- application starts
- /docs works
- registration works
- duplicate registration is rejected
- correct login works
- wrong password returns 401
- nonexistent user returns 401
- invalid JWT returns 401
- Wallet metadata exists

---

# Definition of Done

All tests/checks pass.

No existing authentication functionality is broken.

No future feature should be implemented in this chapter.