from pydantic import BaseModel,EmailStr

class TokenData(BaseModel):
    id:int
    email:EmailStr

class TokenRespo(BaseModel):
    access_token:str
    token_type:str