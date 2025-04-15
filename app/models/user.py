from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so


class User(Base):
    __tablename__ = "user"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(20))
    surname: so.Mapped[str] = so.mapped_column(sa.String(20))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    # devices = so.relationship("User", back_populates="user")
