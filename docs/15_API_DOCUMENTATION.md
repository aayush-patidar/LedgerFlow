# Chapter 15 — API Documentation

Document every public API.

---

# Authentication

POST /user/
POST /login/
GET /user/me

# Wallet

POST /wallet/
GET /wallet/me
GET /wallet/{id}

# Transactions

POST /transaction/transfer
GET /transaction/{id}

# Ledger

GET /wallet/{id}/ledger

# Health

GET /health
GET /ready

---

# Every Endpoint

Document:

- authentication
- request
- response
- status codes
- validation errors
- authorization requirements