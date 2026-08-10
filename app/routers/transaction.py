from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database.database import get_db
from ..core import security
from ..schemas.token import TokenData
from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..models.wallet import Wallet, WalletStatus
from ..models.transaction import Transaction, TransactionStatus
from ..models.ledger import LedgerEntry, EntryType

router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"]
)

@router.post("/transfer", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse)
def transfer(
    transfer_in: TransactionCreate,
    current_user: TokenData = Depends(security.get_user),
    db: Session = Depends(get_db)
):
    sender_wallet = db.query(Wallet).filter(
        Wallet.user_id == current_user.id,
        Wallet.currency == transfer_in.currency.value,
        Wallet.status == WalletStatus.active.value
    ).first()

    if not sender_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active sender wallet not found for the specified currency"
        )

    receiver_wallet = db.query(Wallet).filter(
        Wallet.id == transfer_in.receiver_wallet_id,
        Wallet.status == WalletStatus.active.value
    ).first()

    if not receiver_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active receiver wallet not found"
        )

    if sender_wallet.id == receiver_wallet.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sender and receiver wallets cannot be the same"
        )

    if receiver_wallet.currency != transfer_in.currency.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Receiver wallet currency mismatch"
        )

    if sender_wallet.balance < transfer_in.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    sender_wallet.balance -= transfer_in.amount
    receiver_wallet.balance += transfer_in.amount

    new_tx = Transaction(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=transfer_in.amount,
        currency=transfer_in.currency.value,
        status=TransactionStatus.completed.value,
        idempotency_key=transfer_in.idempotency_key
    )

    db.add(new_tx)

    try:
        db.flush()

        sender_ledger = LedgerEntry(
            transaction_id=new_tx.id,
            wallet_id=sender_wallet.id,
            entry_type=EntryType.DEBIT.value,
            amount=transfer_in.amount,
            currency=transfer_in.currency.value,
            balance_after=sender_wallet.balance
        )
        
        receiver_ledger = LedgerEntry(
            transaction_id=new_tx.id,
            wallet_id=receiver_wallet.id,
            entry_type=EntryType.CREDIT.value,
            amount=transfer_in.amount,
            currency=transfer_in.currency.value,
            balance_after=receiver_wallet.balance
        )

        db.add(sender_ledger)
        db.add(receiver_ledger)
        
        db.commit()
        db.refresh(new_tx)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transaction with this idempotency key already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transfer failed due to an internal error"
        )

    return new_tx
