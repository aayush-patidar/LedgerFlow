from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ..models.wallet import WalletCurrency, WalletStatus

class WalletCreate(BaseModel):
    currency: WalletCurrency


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: Decimal
    currency: WalletCurrency
    status: WalletStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
