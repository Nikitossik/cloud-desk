from __future__ import annotations
from ..database import Base
import sqlalchemy.orm as so
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .session_app_state import SessionAppState
    from .app_usage_period import AppUsagePeriod

class Application(Base):
    __tablename__ = "applications"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    name: so.Mapped[str]
    exe: so.Mapped[str]
    cmdline: so.Mapped[str | None]
    icon_key: so.Mapped[str | None]

    device_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("devices.id"))

    device: so.Mapped["Device"] = so.relationship("Device", back_populates="apps")
    session_app_states: so.Mapped[list["SessionAppState"]] = so.relationship(
        "SessionAppState",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    usage_periods: so.Mapped[list["AppUsagePeriod"]] = so.relationship(
        "AppUsagePeriod",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        sa.UniqueConstraint("device_id", "exe", name="uq_device_exe"),
    )
    
    @hybrid_property
    def display_name(self):
        base_name = self.name[:-4].strip() if self.name.lower().endswith(".exe") else self.name.strip()

        if not base_name:
            return "Unknown app"

        return base_name[0].upper() + base_name[1:]
    