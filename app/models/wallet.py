import enum

from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey, Numeric, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func

from app.database.database import Base


# ---------------------------------------------------------------------------
# Application-level enums
# Shared by schemas and business logic to avoid raw string literals.
# ---------------------------------------------------------------------------

class WalletStatus(str, enum.Enum):
    """Allowed lifecycle states for a wallet."""
    active = "active"
    frozen = "frozen"
    closed = "closed"


class WalletCurrency(str, enum.Enum):
    """Supported ISO-4217 currency codes.
    Add new members here to extend support; CheckConstraint below must be
    updated in sync (or replaced with Alembic migration once that is set up).
    """
    INR = "INR"
    USD = "USD"
    EUR = "EUR"


# ---------------------------------------------------------------------------
# ORM model
# ---------------------------------------------------------------------------

class Wallet(Base):
    __tablename__ = "wallet"

    # DB-level CHECK constraints mirror the Python enums above.
    # These are enforced by PostgreSQL on every INSERT/UPDATE,
    # even if the code bypasses the ORM.
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'frozen', 'closed')",
            name="ck_wallet_status"
        ),
        CheckConstraint(
            "currency IN ('INR', 'USD', 'EUR')",
            name="ck_wallet_currency"
        ),
        UniqueConstraint(
            "user_id", "currency",
            name="uq_user_currency"
        )
    )

    id         = Column(Integer, autoincrement=True, index=True, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    balance    = Column(Numeric(18, 2), nullable=False, server_default=text("0.00"))
    currency   = Column(String, nullable=False)
    status     = Column(String, nullable=False)

    # created_at: set once by the DB on INSERT, never changed.
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # updated_at:
    #   server_default=func.now() → DB sets it on INSERT.
    #   onupdate=func.now()       → SQLAlchemy injects `updated_at = now()` into
    #                               every ORM-issued UPDATE statement automatically.
    #   This is reliable for all application-level wallet mutations.
    #   Raw SQL UPDATEs that bypass the ORM will NOT trigger it; a PostgreSQL
    #   trigger would be needed for that, but is not required for this project.
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
