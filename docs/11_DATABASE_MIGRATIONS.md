# Chapter 11 — Database Migrations

Use Alembic.

---

# Rules

Do not rely on:

Base.metadata.create_all()

for production schema management.

All schema changes must be represented by migrations.

---

# Migration Requirements

Initial migration.

User changes.

Wallet changes.

Transaction changes.

Ledger changes.

Idempotency changes.

Indexes.

Constraints.

---

# Definition of Done

Fresh database can be created from migrations.

Existing database can be upgraded using migrations.