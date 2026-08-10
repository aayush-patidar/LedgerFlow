# Chapter 07 — Concurrency Control

## Objective

Prevent race conditions and double spending.

---

# Problem

Two simultaneous requests may read the same wallet balance.

Example:

Balance = ₹1000

Request A wants ₹800.

Request B wants ₹700.

Without locking both may succeed.

This is invalid.

---

# Solution

Use PostgreSQL row-level locking:

SELECT ... FOR UPDATE

Lock all affected wallets before checking balance.

---

# Lock Ordering

Always lock wallet rows in deterministic order.

Example:

smaller wallet ID first.

This reduces deadlock risk.

---

# Required Tests

Concurrent transfers.

Concurrent insufficient balance requests.

Multiple transfers from same wallet.

---

# Definition of Done

Wallet balance can never become negative.

No money is created or destroyed.

Concurrent operations remain consistent.