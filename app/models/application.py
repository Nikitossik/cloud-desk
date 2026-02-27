from __future__ import annotations
from ..database import Base
import sqlalchemy.orm as so
import sqlalchemy as sa
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .device_session_apps import DeviceSessionApps

class Application(Base):
    __tablename__ = "application"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    name: so.Mapped[str]
    exe: so.Mapped[str]
    cmdline: so.Mapped[str | None]

    device_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("device.id"))

    device: so.Mapped["Device"] = so.relationship("Device", back_populates="apps")
    session_states: so.Mapped[list["DeviceSessionApps"]] = so.relationship(
        "DeviceSessionApps",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    

    def __repr__(self):
        return f"Application({self.name})"
