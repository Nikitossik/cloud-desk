from . import Base
from .user import User
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, ForeignKey
from uuid import uuid4


class UserSession(Base):
    __tablename__ = "user_session"

    id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=uuid4
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User")

    def __repr__(self):
        return f"Session({self.id}, {self.user_id})"
