import enum
from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class EntryType(str, enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class LedgerEntry(Base):
    __tablename__ = "ledger_entry"

    __table_args__ = (
        CheckConstraint(
            "entry_type IN ('DEBIT', 'CREDIT')",
            name="ck_ledger_entry_type"
        ),
        CheckConstraint(
            "currency IN ('INR', 'USD', 'EUR')",
            name="ck_ledger_currency"
        ),
        CheckConstraint(
            "amount > 0",
            name="ck_ledger_amount_positive"
        )
    )

    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
    
    entry_type = Column(String, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String, nullable=False)
    balance_after = Column(Numeric(18, 2), nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    transaction = relationship("Transaction")
    wallet = relationship("Wallet")
