from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import DB_URL


engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_all_tables() -> None:
    Base.metadata.create_all(bind=engine)
