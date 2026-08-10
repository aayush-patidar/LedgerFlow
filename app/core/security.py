from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from passlib.context import CryptContext
context=CryptContext(schemes=["bcrypt"],deprecated="auto")
from .config import settings
from datetime import datetime,timezone,timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer

from ..schemas.token import TokenData

oauth_scheme=OAuth2PasswordBearer(tokenUrl="/login")


def hash(password:str):
    return context.hash(password)

def verify(pass1:str,pass2):
    return context.verify(pass1,pass2)


def create_token(data:dict):
    to_encode=data.copy();
    exp_min=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"]=int(exp_min.timestamp())
    token=jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM)

    return token
def verify_token(token:str,credentials_exception):
    try:
        check=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        id=check.get("id")
        email=check.get("email")

        if not id:
            raise credentials_exception

        token_data=TokenData(id=id,email=email)
        return token_data

    except JWTError as e:
        return e

def get_user(token:str=Depends(oauth_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"user is not authorised to perform this action")

    return verify_token(token,credentials_exception)
