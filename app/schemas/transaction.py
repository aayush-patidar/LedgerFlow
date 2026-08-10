from pydantic import BaseModel, condecimal, constr
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ..models.wallet import WalletCurrency
from ..models.transaction import TransactionStatus

class TransactionCreate(BaseModel):
    receiver_wallet_id: int
    # Enforce amount > 0 directly in the schema
    amount: condecimal(gt=0, decimal_places=2, max_digits=18)
    currency: WalletCurrency
    idempotency_key: constr(min_length=1)

class TransactionResponse(BaseModel):
    id: int
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: Decimal
    currency: WalletCurrency
    status: TransactionStatus
    idempotency_key: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
