from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import setting

engine = create_engine(setting.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    def __init__(self, **entries):
        # ignore extra keywords when creating an instance
        self.__dict__.update(entries)
