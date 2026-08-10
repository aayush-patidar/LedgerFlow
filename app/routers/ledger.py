from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..core import security
from ..schemas.token import TokenData
from ..schemas.ledger import LedgerEntryResponse
from ..models.wallet import Wallet
from ..models.ledger import LedgerEntry

router = APIRouter(
    prefix="/ledger",
    tags=["Ledger"]
)

@router.get("/{wallet_id}", response_model=List[LedgerEntryResponse])
def get_wallet_ledger(
    wallet_id: int,
    current_user: TokenData = Depends(security.get_user),
    db: Session = Depends(get_db)
):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    
    if not wallet or wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
        
    entries = db.query(LedgerEntry).filter(LedgerEntry.wallet_id == wallet_id).order_by(LedgerEntry.created_at.asc()).all()
    
    return entries
