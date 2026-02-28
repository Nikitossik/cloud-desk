from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device_session import DeviceSession
    from .application import Application
    from .app_usage_period import AppUsagePeriod


class SessionAppState(Base):
    __tablename__ = "session_app_states"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    session_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("device_sessions.id")
    )
    application_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("applications.id"))
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    device_session: so.Mapped["DeviceSession"] = so.relationship(
        "DeviceSession", back_populates="session_app_states"
    )
    application: so.Mapped["Application"] = so.relationship(
        "Application", back_populates="session_app_states"
    )
    
    __table_args__ = (
        sa.UniqueConstraint("session_id", "application_id", name="uq_session_application"),
    )
