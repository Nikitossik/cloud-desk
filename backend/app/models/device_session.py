from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid
from sqlalchemy.ext.hybrid import hybrid_property

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .session_app_state import SessionAppState
    from .application import Application
    from .app_usage_period import AppUsagePeriod
    from .device_session_events import DeviceSessionEvent

from .device_session_events import SessionEventType

class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id: so.Mapped[str] = so.mapped_column(sa.Uuid(), primary_key=True, default=uuid.uuid4)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    slugname: so.Mapped[str]
    description: so.Mapped[str | None]
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)

    created_at = so.mapped_column(sa.DateTime(), server_default=sa.func.now())
    last_active_at = so.mapped_column(sa.DateTime(), nullable=True)
    last_restored_at = so.mapped_column(sa.DateTime(), nullable=True)
    last_deleted_at = so.mapped_column(sa.DateTime(), nullable=True)

    # relations

    device_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("devices.id"))
    device: so.Mapped["Device"] = so.relationship("Device", back_populates="sessions")
    session_app_states: so.Mapped[list["SessionAppState"]] = so.relationship(
        "SessionAppState",
        back_populates="device_session",
        cascade="all, delete-orphan",
    )
    apps: so.Mapped[list["Application"]] = so.relationship(
        "Application",
        secondary="session_app_states",
    )
    usage_periods: so.Mapped[list["AppUsagePeriod"]] = so.relationship(
        "AppUsagePeriod",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    events: so.Mapped[list["DeviceSessionEvent"]] = so.relationship(
        "DeviceSessionEvent",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    __table_args__ = (
        sa.UniqueConstraint("device_id", "name", name="uq_device_name"),
        sa.UniqueConstraint("device_id", "slugname", name="uq_device_slugname"),
    )
    
    # hybrid properties

    @hybrid_property
    def start_count(self) -> int:
        return sum(1 for event in self.events if event.event_type == SessionEventType.STARTED)

    @hybrid_property
    def restore_count(self) -> int:
        return sum(1 for event in self.events if event.event_type == SessionEventType.RESTORED)

    @hybrid_property
    def total_active_time(self) -> int:
        total_seconds = 0
        started_at = None
        sorted_events = sorted(
            (event for event in self.events if event.timestamp is not None),
            key=lambda event: event.timestamp,
        )

        for event in sorted_events:
            if event.event_type == SessionEventType.STARTED:
                if started_at is None:
                    started_at = event.timestamp
                continue

            if event.event_type != SessionEventType.STOPPED:
                continue

            if started_at is None:
                continue

            seconds = int((event.timestamp - started_at).total_seconds())
            if seconds > 0:
                total_seconds += seconds

            started_at = None

        return total_seconds
