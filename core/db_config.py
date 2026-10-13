from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.engine import create_engine
from typing import Annotated
from fastapi import Depends
from .config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def init_db():
    Base.metadata.create_all(bind=engine)