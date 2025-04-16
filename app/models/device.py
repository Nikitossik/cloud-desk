from __future__ import annotations

from ..database import Base
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.utils.core as uc
import uuid

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Application
    from .device_session import DeviceSession


class Device(Base):
    __tablename__ = "device"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    mac_address: so.Mapped[str] = so.mapped_column(
        sa.String(17), default=uc.get_mac_address, unique=True
    )
    name: so.Mapped[str | None]
    os_name: so.Mapped[str]
    os_release: so.Mapped[str]
    os_release_ver: so.Mapped[str]
    architecture: so.Mapped[str]
    created_at = so.mapped_column(sa.DateTime(), server_default=sa.func.now())

    apps: so.Mapped[list["Application"]] = so.relationship(
        "Application", back_populates="device", cascade="all, delete-orphan"
    )
    sessions: so.Mapped[list["DeviceSession"]] = so.relationship(
        "DeviceSession", back_populates="device", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Device({self.mac_address})"
