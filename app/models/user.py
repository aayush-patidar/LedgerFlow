from sqlalchemy import Column,Integer,String,TIMESTAMP,text
from app.database.database import Base


class Users(Base):
    __tablename__="users"
    id=Column(Integer,autoincrement=True,index=True,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
