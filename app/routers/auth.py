from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas import token
from ..models  import user
from ..core import security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/",response_model=token.TokenRespo)
def login(sign:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    logged_in=db.query(user.Users).filter(user.Users.email==sign.username).first()
    if not logged_in :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"username doesn't exist")

    if not security.verify(sign.password,logged_in.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    token=security.create_token({"id":logged_in.id,"email":logged_in.email})

    return {"access_token":token,"token_type":"bearer"}
