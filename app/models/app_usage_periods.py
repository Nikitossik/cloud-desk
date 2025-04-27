from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid
from datetime import timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device_session_apps import DeviceSessionApps


class AppUsagePeriods(Base):
    __tablename__ = "app_usage_periods"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    session_app_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("device_session_apps.id")
    )
    started_at = so.mapped_column(
        sa.DateTime(), nullable=False, server_default=sa.func.now()
    )
    ended_at = so.mapped_column(
        sa.DateTime(), nullable=False, server_default=sa.func.now()
    )

    session_app: so.Mapped["DeviceSessionApps"] = so.relationship(
        "DeviceSessionApps", back_populates="usage_periods"
    )

    @property
    def duration(self) -> timedelta:
        return self.ended_at - self.started_at
