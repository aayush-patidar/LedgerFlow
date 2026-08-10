from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ..models.wallet import WalletCurrency
from ..models.ledger import EntryType

class LedgerEntryResponse(BaseModel):
    id: int
    transaction_id: int
    wallet_id: int
    entry_type: EntryType
    amount: Decimal
    currency: WalletCurrency
    balance_after: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
