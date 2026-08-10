from pydantic import BaseModel,EmailStr

class NewUser(BaseModel):
    email:EmailStr
    password:str
