from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..schemas.user import NewUser, UserResponse
from ..schemas.token import TokenData
from ..models.user import Users
from ..database.database import get_db
from ..core import security

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def newUser(user: NewUser, db: Session = Depends(get_db)):
    hash_pass = security.hash(user.password)
    user.password = hash_pass
    db_user = Users(**user.model_dump())
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )
    return db_user


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: TokenData = Depends(security.get_user),
    db: Session = Depends(get_db)
):
    """Return the authenticated user's profile. Never exposes password."""
    db_user = db.query(Users).filter(Users.id == current_user.id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user
