from . import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .device_session_apps import DeviceSessionApps
    from .application import Application


class DeviceSession(Base):
    __tablename__ = "device_session"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    name: so.Mapped[str] = so.mapped_column(unique=True)
    description: so.Mapped[str | None]

    created_at = so.mapped_column(sa.DateTime(), server_default=sa.func.now())

    device_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("device.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    device: so.Mapped["Device"] = so.relationship(back_populates="sessions")
    app_states: so.Mapped["DeviceSessionApps"] = so.relationship(
        back_populates="device_session"
    )
    apps: so.Mapped[list["Application"]] = so.relationship(
        secondary="device_session_apps",
        # back_populates="sessions",
    )
