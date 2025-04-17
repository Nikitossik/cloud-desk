from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .device_session_apps import DeviceSessionApps
    from .application import Application


class DeviceSession(Base):
    __tablename__ = "device_session"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)
    slugname: so.Mapped[str] = so.mapped_column(unique=True, index=True)
    description: so.Mapped[str | None]
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)

    created_at = so.mapped_column(sa.DateTime(), server_default=sa.func.now())
    saved_at = so.mapped_column(sa.DateTime(), nullable=True)
    last_active_at = so.mapped_column(sa.DateTime(), nullable=True)
    restored_at = so.mapped_column(sa.DateTime(), nullable=True)

    # relations

    device_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("device.id"))
    device: so.Mapped["Device"] = so.relationship("Device", back_populates="sessions")
    app_states: so.Mapped[list["DeviceSessionApps"]] = so.relationship(
        "DeviceSessionApps",
        back_populates="device_session",
        cascade="all, delete-orphan",
    )
    apps: so.Mapped[list["Application"]] = so.relationship(
        "Application",
        secondary="device_session_apps",
        # back_populates="sessions",
    )
