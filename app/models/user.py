from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device


class User(Base):
    __tablename__ = "user"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(20))
    surname: so.Mapped[str] = so.mapped_column(sa.String(20))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    devices: so.Mapped[list["Device"]] = so.relationship(
        "Device", back_populates="user", cascade="all, delete-orphan"
    )
