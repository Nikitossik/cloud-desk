from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid
from datetime import timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Application
    from .device_session import DeviceSession


class AppUsagePeriod(Base):
    __tablename__ = "app_usage_periods"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    application_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("applications.id")
    )
    session_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("device_sessions.id"), index=True
    )
    started_at = so.mapped_column(
        sa.DateTime(), nullable=False, server_default=sa.func.now()
    )
    ended_at = so.mapped_column(
        sa.DateTime(), nullable=True
    )

    application: so.Mapped["Application"] = so.relationship(
        "Application", back_populates="usage_periods"
    )
    session: so.Mapped["DeviceSession"] = so.relationship(
        "DeviceSession", back_populates="usage_periods"
    )

    @property
    def duration(self) -> timedelta:
        return self.ended_at - self.started_at
