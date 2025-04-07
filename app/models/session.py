from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Uuid
from uuid import uuid4
from .user import User


class Session(Base):
    __tablename__ = "session"

    id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=uuid4
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    user: Mapped[User] = relationship("User")

    def __repr__(self):
        return f"Session({self.id}, {self.user_id})"
