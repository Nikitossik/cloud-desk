from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __init__(self, **entries):
        # ignore extra keywords when creating an instance
        self.__dict__.update(entries)


from .user import User
from .session import Session
