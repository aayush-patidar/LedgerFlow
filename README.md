# LedgerFlow

## Overview
LedgerFlow is a backend-focused financial ledger and core banking system. It is designed to handle user accounts, secure authentication, multi-currency wallets, transactional transfers, and an immutable double-entry accounting ledger. 

The project goes beyond a standard CRUD application by prioritizing **financial correctness, atomicity, strict database constraints, and cross-user data isolation**.

## Key Features
*   **Secure Authentication**: JWT-based authentication with bcrypt password hashing.
*   **Multi-Currency Wallets**: Users can own active wallets strictly segregated by currency.
*   **Atomic Transactions**: Fund transfers operate inside atomic database boundaries to guarantee partial financial states never occur.
*   **Double-Entry Accounting**: Every successful transfer is backed by immutable DEBIT and CREDIT ledger entries enforcing exact accounting invariants.
*   **Database-Level Integrity**: Critical business rules (positive amounts, valid currencies, valid entry types, duplicate detection) are enforced natively by PostgreSQL.

## Technology Stack
**Implemented:**
*   **Python 3**
*   **FastAPI**: Web framework for building APIs.
*   **PostgreSQL**: Primary relational database.
*   **SQLAlchemy**: ORM for database interaction and transaction management.
*   **Pydantic**: Request/response validation and serialization.
*   **Passlib (bcrypt) & python-jose**: Password hashing and JWT generation.

**Planned / Future Implementation:**
*   Redis (Caching & Idempotency replay)
*   Alembic (Database migrations)
*   Docker (Containerization)
*   Pytest (Official test suite)

## Architecture
The application follows a modular, domain-driven structure within the FastAPI ecosystem. Routes, schemas, and models are separated logically to support future scalability. Financial operations bypass floating-point math entirely in favor of fixed-precision numerics.

## Project Structure
```text
LedgerFlow/
├── .env                          # Local environment variables
├── .gitignore                    # Git exclusions
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application factory and router registration
│   ├── core/
│   │   ├── config.py             # Configuration and environment settings
│   │   └── security.py           # JWT encoding, decoding, and password verification
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py           # SQLAlchemy engine and SessionLocal setup
│   ├── models/                   # SQLAlchemy ORM Models
│   │   ├── ledger.py
│   │   ├── transaction.py
│   │   ├── user.py
│   │   └── wallet.py
│   ├── routers/                  # API Route Definitions
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── ledger.py
│   │   ├── transaction.py
│   │   ├── users.py
│   │   └── wallet.py
│   └── schemas/                  # Pydantic Schemas
│       ├── ledger.py
│       ├── token.py
│       ├── transaction.py
│       ├── user.py
│       └── wallet.py
└── scratch/                      # E2E Test Scripts
    └── verify_all.py             # Consolidated Chapter 01-05 verification script
```

## Database Design
| Table / Model | Purpose | Primary Key | Foreign Keys | Important Constraints |
| --- | --- | --- | --- | --- |
| `users` | Store user profiles | `id` | None | `UNIQUE(email)` |
| `wallet` | Track user balances | `id` | `user_id` -> `users.id` | `ck_wallet_status`, `ck_wallet_currency`, `UNIQUE(user_id, currency)` |
| `transaction` | Record transfer requests | `id` | `sender_wallet_id` -> `wallet.id`, <br> `receiver_wallet_id` -> `wallet.id` | `ck_transaction_status`, `ck_transaction_currency`, `UNIQUE(idempotency_key)` |
| `ledger_entry` | Immutable accounting trail | `id` | `transaction_id` -> `transaction.id`, <br> `wallet_id` -> `wallet.id` | `ck_ledger_entry_type`, `ck_ledger_currency`, `ck_ledger_amount_positive` |

## Authentication & Authorization
*   **Authentication**: Users authenticate via `POST /login/`. The server verifies the bcrypt hash and returns a JSON Web Token (JWT). All protected endpoints depend on `security.get_user`, which validates the token structure and expiration.
*   **Authorization**: API routes strictly enforce ownership. A user can only view their own wallets, read their own ledger entries, and send money from wallets belonging to their `current_user.id`. Cross-user access is safely rejected with HTTP 404 to prevent account enumeration.

## Wallet System
Users can create wallets for supported currencies (INR, USD, EUR). The database restricts users to **one wallet per currency**. All wallets initialize with an active status and a `0.00` balance. The API exposes read-only operations for wallet balances—clients cannot manually edit balance or status fields.

## Transaction System
The transaction engine handles moving funds between wallets.
*   **Validations**: It enforces that amounts are strictly positive, sender and receiver wallets are distinct, currencies match identically, and the sender has sufficient balance.
*   **Idempotency**: Clients must submit an `idempotency_key` with every transfer request. The database enforces uniqueness on this key to prevent duplicate processing.

## Double-Entry Ledger
The system enforces rigorous accounting via the `LedgerEntry` model.
Every successful transfer automatically creates exactly **two ledger entries**:
*   **Sender**: Logged as a `DEBIT`.
*   **Receiver**: Logged as a `CREDIT`.

Both entries share the exact same `transaction_id`, `amount`, and `currency`. They also capture the affected `wallet_id`, `entry_type`, `balance_after`, and `created_at` timestamp.

## Financial Invariants
To guarantee correctness, the following invariants are enforced:
*   **Fixed Precision**: All monetary fields (`balance`, `amount`, `balance_after`) utilize `Numeric(18,2)`. Floats are never used.
*   **Positive Amounts**: Enforced by Application (Pydantic) and Database (`ck_ledger_amount_positive`).
*   **Accounting Invariant**: `SUM(DEBIT) == SUM(CREDIT)`. Enforced by synchronous application logic instantiating exact equal entries during the transfer.
*   **Immutability**: `LedgerEntry` tables have no `PUT`, `PATCH`, or `DELETE` endpoints.

## API Reference

| Method | Endpoint | Purpose | Auth Required | Success | Important Errors |
| --- | --- | --- | --- | --- | --- |
| POST | `/user/` | Register user | No | 201 | 409 (Duplicate Email) |
| POST | `/login/` | Login | No | 200 | 401 (Bad Credentials) |
| GET | `/user/me` | Current user profile | Yes | 200 | 401 (Invalid Token) |
| POST | `/wallet/` | Create a wallet | Yes | 201 | 409 (Duplicate Currency) |
| GET | `/wallet/me` | List owned wallets | Yes | 200 | 401 |
| GET | `/wallet/{id}` | Get specific wallet | Yes | 200 | 404 (Not Found / Unowned) |
| POST | `/transaction/transfer` | Transfer funds | Yes | 201 | 400 (Balance), 409 (Idempotency) |
| GET | `/ledger/{wallet_id}` | View ledger history | Yes | 200 | 404 (Not Found / Unowned) |

## Transaction Flow
1. **Request** → Client calls `POST /transaction/transfer`.
2. **Authentication** → JWT verified, user identified.
3. **Sender/Receiver Validation** → Wallets fetched; sender ownership verified.
4. **Balance Validation** → Overdrafts rejected.
5. **Balance Updates** → Sender balance decreased, receiver balance increased.
6. **Transaction Creation** → `Transaction` record created as `completed`.
7. **Ledger Creation** → `DEBIT` entry created for sender, `CREDIT` entry created for receiver.
8. **Commit** → Database transaction committed atomically.

## Atomicity & Consistency
The entire transfer pipeline (updating two wallet balances, inserting one transaction log, and inserting two ledger entries) occurs within a single SQLAlchemy `Session`. 
*   **Success**: The `db.commit()` finalizes the entire batch safely.
*   **Failure**: If any constraint fails (e.g., an `IntegrityError` due to a duplicate `idempotency_key`), the `except` block catches it and executes a `db.rollback()`.
*   **Result**: Partial financial states are impossible.

## Testing
Extensive end-to-end Python test scripts exist in `scratch/`. These scripts execute HTTPX requests against a live local Uvicorn server connected to a real PostgreSQL instance.

**Chapter 05 Verification Checks Status (22/22 PASSED):**
1. Successful transfer succeeds
2. Transaction record is created
3. Exactly two ledger entries are created
4. Sender has exactly one DEBIT entry
5. Receiver has exactly one CREDIT entry
6. Debit amount equals transfer amount
7. Credit amount equals transfer amount
8. Debit equals credit
9. Transaction currency matches ledger currency
10. Sender balance_after is correct
11. Receiver balance_after is correct
12. Both entries reference the correct transaction
13. Total debit equals total credit
14. Insufficient balance creates no ledger entries
15. Self-transfer creates no ledger entries
16. Invalid currency creates no ledger entries
17. Failed transfer leaves no partial ledger state
18. Existing authentication still works
19. Existing wallet APIs still work
20. Existing transaction API still works
21. Invalid JWT returns 401
22. Cross-user ledger retrieval is rejected

## Production Readiness
LedgerFlow possesses a rigorous financial core, but it is not yet a fully production-ready system. 

| Area | Status | Explanation |
| --- | --- | --- |
| User Management | Implemented | Passwords safely hashed; duplicates blocked. |
| JWT Authentication | Implemented | Fast, stateless, and secure. |
| Authorization | Implemented | Cross-user data isolation strictly enforced. |
| Wallets & Transactions | Implemented | Secure API routing with deep logic checks. |
| Double-Entry Ledger | Implemented | Database-level integrity constraints active. |
| Atomicity | Implemented | SQLAlchemy session boundaries protect state. |
| Basic Idempotency | Implemented | Duplicates blocked by DB constraint. |
| Idempotency Replay | **Not Implemented** | Does not cache/replay the original HTTP 201. |
| Concurrency Locking | **Not Implemented** | Lacks `SELECT FOR UPDATE`. |
| Alembic Migrations | **Not Implemented** | Schema evolution requires manual DB resets. |
| Redis / Docker / CI | **Not Implemented** | Infrastructure components deferred. |

## Current Limitations
*   **Idempotency Handling**: Duplicate `idempotency_key` submissions correctly trigger an `IntegrityError` and are rejected with an HTTP 409 Conflict. However, a true production system should cache and replay the original successful response.
*   **Concurrency**: There is currently no row-level database locking (e.g., `SELECT FOR UPDATE`). Concurrent transfer requests could theoretically bypass balance checks, leading to double-spending overdrafts.
*   **Migrations**: Alembic is missing. Any database schema updates currently require destructively recreating tables.
*   **Observability**: There is no structured logging, health checks, metrics, or rate-limiting middleware in place.

## Development Roadmap
*   Chapter 01 — Foundation              ✅ COMPLETE
*   Chapter 02 — Users                   ✅ COMPLETE
*   Chapter 03 — Authentication          ✅ COMPLETE
*   Chapter 04 — Wallets + Transactions  ✅ COMPLETE
*   Chapter 05 — Double-Entry Ledger     ✅ COMPLETE
*   Chapter 06 — Production Idempotency  🔄 **NEXT**
*   Chapter 07 — Concurrency Control     🔄 FUTURE
*   Future — Redis / Caching
*   Future — Alembic Migrations
*   Future — Observability & Rate Limiting
*   Future — Docker / Deployment

## Setup & Running Locally
*(Instructions pending finalization of Docker and Alembic integration)*