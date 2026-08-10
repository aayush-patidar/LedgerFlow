import enum
from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.wallet import WalletCurrency




class TransactionStatus(str, enum.Enum):
    """Allowed lifecycle states for a transaction."""
    pending = "pending"
    completed = "completed"
    failed = "failed"
    reversed = "reversed"




class Transaction(Base):
    __tablename__ = "transaction"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed', 'failed', 'reversed')",
            name="ck_transaction_status"
        ),
        CheckConstraint(
            "currency IN ('INR', 'USD', 'EUR')",
            name="ck_transaction_currency"
        ),
    )

    id                 = Column(Integer, autoincrement=True, index=True, primary_key=True)
    sender_wallet_id   = Column(Integer, ForeignKey("wallet.id"), nullable=False)
    receiver_wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
    
    
    amount             = Column(Numeric(18, 2), nullable=False)
    currency           = Column(String, nullable=False)
    status             = Column(String, nullable=False)
    
    
    idempotency_key    = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

 
    sender_wallet = relationship("Wallet", foreign_keys=[sender_wallet_id])
    receiver_wallet = relationship("Wallet", foreign_keys=[receiver_wallet_id])
