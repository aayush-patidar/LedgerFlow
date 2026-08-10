# LedgerFlow

## High-Throughput Distributed Ledger & Wallet System

LedgerFlow is a backend-focused financial ledger and wallet system built with **Python, FastAPI, PostgreSQL, SQLAlchemy, Redis, and JWT authentication**.

The project is being developed to understand and implement production-oriented backend concepts such as **secure authentication, wallet management, financial transactions, database consistency, idempotency, caching, and scalable API design**.

---

## 🚀 Project Goals

The main goal of LedgerFlow is to build a reliable backend system capable of handling financial operations while maintaining:

- Data consistency
- Transaction integrity
- Secure authentication
- Authorization
- Idempotent operations
- Fast data access
- Traceable financial records
- Clean and maintainable architecture

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Primary relational database |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Request/response validation |
| JWT | Authentication |
| Redis | Caching |
| Docker | Containerization |
| Pytest | Testing |
| Uvicorn | ASGI server |

---

## 📂 Project Structure

The current project follows a modular FastAPI structure:

```text
LEDGERFLOW/
│
├── .venv/
│
├── app/
│   │
│   ├── core/
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── models/
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── users.py
│   │
│   ├── schemas/
│   │
│   ├── __init__.py
│   └── main.py
│
├── .env
├── .gitignore
└── README.md