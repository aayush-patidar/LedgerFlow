from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database.database import get_db
from ..core import security
from ..schemas.token import TokenData
from ..schemas.wallet import WalletCreate, WalletResponse
from ..models.wallet import Wallet, WalletStatus

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WalletResponse)
def create_wallet(
    wallet_in: WalletCreate,
    current_user: TokenData = Depends(security.get_user),
    db: Session = Depends(get_db)
):
    new_wallet = Wallet(
        user_id=current_user.id,
        balance=Decimal("0.00"),
        currency=wallet_in.currency,
        status=WalletStatus.active
    )
    db.add(new_wallet)
    try:
        db.commit()
        db.refresh(new_wallet)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Wallet for currency {wallet_in.currency.value} already exists for this user."
        )
    return new_wallet

@router.get("/me", response_model=List[WalletResponse])
def get_my_wallets(
    current_user: TokenData = Depends(security.get_user),
    db: Session = Depends(get_db)
):
    wallets = db.query(Wallet).filter(Wallet.user_id == current_user.id).all()
    return wallets

@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(
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
    return wallet
