# Chapter 04 — Transaction Engine

## Objective

Implement wallet-to-wallet money transfers safely.

---

# Transfer

POST /transaction/transfer

Request:

receiver_wallet_id
amount
currency

Authentication is required.

Sender wallet is determined from the authenticated user.

---

# Validation

Reject:

- amount <= 0
- nonexistent receiver
- sender == receiver
- currency mismatch
- inactive wallet
- frozen wallet
- closed wallet
- insufficient balance

---

# Atomicity

The complete operation must occur inside one database transaction.

Operations:

1. Lock wallets.
2. Validate balance.
3. Debit sender.
4. Credit receiver.
5. Create transaction.
6. Create ledger entries.
7. Commit.

Any failure:

ROLLBACK

No partial state is allowed.

---

# Financial Invariant

Before transfer:

sender_balance + receiver_balance

After transfer:

sender_balance - amount
receiver_balance + amount

Total system money must remain unchanged by a transfer.

---

# Concurrency

Use PostgreSQL row-level locking.

Use:

SELECT FOR UPDATE

Lock wallets in deterministic order.

---

# Definition of Done

Concurrent transfers cannot cause double spending.

Insufficient balance is rejected.

Successful transfer updates both wallets atomically.

Failed transfer changes nothing.