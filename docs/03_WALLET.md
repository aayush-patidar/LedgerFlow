# Chapter 03 — Wallet Management

## Objective

Implement secure wallet creation and retrieval.

---

# Wallet Model

Required fields:

id
user_id
balance
currency
status
created_at
updated_at

---

# Constraints

balance:

NUMERIC(18,2)

balance >= 0

user_id:

Foreign Key → users.id

currency:

Valid supported currency.

status:

ACTIVE
FROZEN
CLOSED

---

# API

POST /wallet/

Create wallet for authenticated user.

Initial balance:

0.00

---

GET /wallet/me

Return wallets owned by current user.

---

GET /wallet/{wallet_id}

Return wallet only if it belongs to authenticated user.

---

# Security

Never allow client to provide:

user_id

balance

created_at

updated_at

for wallet creation.

The authenticated user determines ownership.

---

# Definition of Done

Authenticated user can create wallet.

Unauthenticated user cannot create wallet.

User can retrieve own wallet.

User cannot retrieve another user's wallet.

Balance starts at zero.
