from __future__ import annotations

from ..database import Base
import sqlalchemy.orm as so
import sqlalchemy as sa
import uuid

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Application
    from .device_session import DeviceSession
    from .user import User


class Device(Base):
    __tablename__ = "devices"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    fingerprint: so.Mapped[str] = so.mapped_column(index=True) 
    display_name: so.Mapped[str | None] = so.mapped_column(sa.String(60), nullable=True)
    
    mac_address: so.Mapped[str] = so.mapped_column(sa.String(17))
    os_name: so.Mapped[str] = so.mapped_column(sa.String(50))
    os_release: so.Mapped[str]
    os_release_ver: so.Mapped[str]
    architecture: so.Mapped[str]
    created_at = so.mapped_column(sa.DateTime(), server_default=sa.func.now())
    last_seen_at = so.mapped_column(sa.DateTime(), nullable=True)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    
    user: so.Mapped["User"] = so.relationship("User", back_populates="devices")
    apps: so.Mapped[list["Application"]] = so.relationship(
        "Application", back_populates="device", cascade="all, delete-orphan"
    )
    sessions: so.Mapped[list["DeviceSession"]] = so.relationship(
        "DeviceSession", back_populates="device", cascade="all, delete-orphan"
    )

    __table_args__ = (
        sa.UniqueConstraint("user_id", "fingerprint", name="uq_user_fingerprint"),
    )

