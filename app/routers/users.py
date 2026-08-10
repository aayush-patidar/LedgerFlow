from fastapi import APIRouter,Depends,HTTPException,status
from ..schemas.user import NewUser,UserResponse
from ..models.user import Users
from ..database.database import get_db
from ..core import security
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def newUser(user:NewUser,db:Session=Depends(get_db)):
    hash_pass=security.hash(user.password)
    user.password=hash_pass
    user=Users(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

    
