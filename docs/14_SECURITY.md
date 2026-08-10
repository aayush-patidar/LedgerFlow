# Chapter 14 — Security

Implement production security controls.

---

## Authentication

JWT.

---

## Passwords

Strong password hashing.

Never store plaintext.

---

## Authorization

Every protected resource verifies ownership.

---

## Secrets

Never commit:

.env

Use:

.env.example

---

## Database

Use parameterized SQL/SQLAlchemy.

Never construct SQL using untrusted string concatenation.

---

## Rate Limiting

Protect authentication and financial endpoints.

---

## Input Validation

Validate:

amount
currency
wallet IDs
idempotency keys

---

## Definition of Done

Security-sensitive endpoints are protected and tested.