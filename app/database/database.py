from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.core.config import settings


DATABASE_URL=f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

