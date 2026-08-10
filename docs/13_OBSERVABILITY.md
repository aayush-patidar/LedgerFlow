# Chapter 13 — Observability

Implement:

- structured logging
- request logging
- transaction logging
- error logging
- health endpoint
- readiness endpoint

---

# Endpoints

GET /health
GET /ready

---

# Do Not Log

Passwords
JWT secrets
Authorization headers
Sensitive credentials

---

# Definition of Done

Application health can be monitored.

Important failures are visible in logs.