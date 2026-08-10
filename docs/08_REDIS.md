# Chapter 08 — Redis

## Objective

Introduce Redis for non-authoritative high-speed operations.

PostgreSQL remains the financial source of truth.

---

# Uses

Redis may be used for:

- Rate limiting
- Idempotency response caching
- Short-lived cache
- Token/session revocation if implemented

---

# Important Rule

Never use Redis as the source of truth for:

wallet balance
ledger entries
transaction records

PostgreSQL remains authoritative.

---

# Rate Limiting

Protect:

POST /login
POST /transaction/transfer

from excessive requests.

---

# Definition of Done

Redis is connected.

Rate limiting works.

Redis failure does not corrupt financial data.