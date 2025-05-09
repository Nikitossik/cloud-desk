from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device_session import DeviceSession
    from .application import Application
    from .app_usage_periods import AppUsagePeriods


class DeviceSessionApps(Base):
    __tablename__ = "device_session_apps"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    device_session_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("device_session.id")
    )
    application_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("application.id"))
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    device_session: so.Mapped["DeviceSession"] = so.relationship(
        "DeviceSession", back_populates="app_states"
    )
    application: so.Mapped["Application"] = so.relationship("Application")
    usage_periods: so.Mapped[list["AppUsagePeriods"]] = so.relationship(
        "AppUsagePeriods",
        back_populates="session_app",
        cascade="all, delete-orphan",
    )
