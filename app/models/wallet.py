from sqlalchemy import Column,Integer,String,text,TIMESTAMP,ForeignKey,Numeric,func


from app.database.database import Base

class Wallet(Base):
    __tablename__="Wallet"
    id=id=Column(Integer,autoincrement=True,index=True,primary_key=True)
    user_id=Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    balance=Column(Numeric(18,2),nullable=False)
    currency=Column(String,nullable=False)
    status=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),onupdate=func.now())

