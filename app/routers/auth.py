from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas.token import TokenRespo
from ..models  import user
from ..core import security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    prefix="/login",
    tags=["Login"]
)

_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
    headers={"WWW-Authenticate": "Bearer"},
)

@router.post("/",response_model=TokenRespo)
def login(sign:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    logged_in=db.query(user.Users).filter(user.Users.email==sign.username).first()

    if not logged_in:
        raise _INVALID_CREDENTIALS

    if not security.verify(sign.password,logged_in.password):
        raise _INVALID_CREDENTIALS

    access_token=security.create_token({"id":logged_in.id,"email":logged_in.email})

    return {"access_token":access_token,"token_type":"bearer"}
