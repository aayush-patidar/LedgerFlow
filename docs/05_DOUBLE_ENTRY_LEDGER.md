# Chapter 05 — Double-Entry Ledger

## Objective

Implement an immutable accounting ledger.

---

# LedgerEntry

Fields:

id
transaction_id
wallet_id
entry_type
amount
balance_after
created_at

---

# Entry Types

DEBIT
CREDIT

---

# Transfer Example

₹500 from Wallet A to Wallet B:

Wallet A:

DEBIT 500

Wallet B:

CREDIT 500

---

# Rules

Every completed transaction must have:

one debit
one credit

Total debit amount must equal total credit amount.

Ledger entries must never be edited or deleted after creation.

Corrections must be represented using reversal transactions.

---

# Definition of Done

Every successful transfer creates matching ledger entries.

Ledger provides an auditable transaction history.