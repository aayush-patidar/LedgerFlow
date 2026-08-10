# Chapter 06 — Idempotency

## Objective

Prevent duplicate financial transfers caused by retries.

---

# API

POST /transaction/transfer

Required header:

Idempotency-Key

---

# Behavior

First request:

Execute transfer.

Repeated request with same key:

Do not execute again.

Return original result.

---

# Database

Create an idempotency record with:

id
user_id
key
request_hash
response
status
created_at

Unique constraint:

(user_id, key)

---

# Security

If the same key is reused with a different request payload:

Reject the request.

Do not execute the second operation.

---

# Definition of Done

Repeated identical requests produce one transfer.

Database guarantees uniqueness.