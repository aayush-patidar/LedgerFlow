# Chapter 10 — Testing

Use pytest.

---

# Test Categories

## Authentication

- registration
- duplicate email
- login
- wrong password
- wrong email
- expired JWT
- invalid JWT

## Wallet

- create wallet
- unauthorized creation
- retrieve wallet
- ownership

## Transaction

- successful transfer
- insufficient funds
- invalid wallet
- same wallet
- currency mismatch
- frozen wallet
- closed wallet

## Idempotency

- duplicate request
- same key different payload

## Concurrency

- simultaneous transfers
- double spending

---

# Definition of Done

All tests pass.

Critical financial logic has automated tests.