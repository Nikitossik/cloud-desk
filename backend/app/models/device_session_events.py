from __future__ import annotations

from ..database import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid
import enum
from datetime import datetime

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .device_session import DeviceSession

class SessionEventType(enum.Enum):
    STARTED = "started"
    STOPPED = "stopped"
    RESTORED = "restored"
    MOVED_TO_TRASH = "moved_to_trash"
    RESTORED_FROM_TRASH = "restored_from_trash"

class DeviceSessionEvent(Base):
    __tablename__ = "device_session_events"

    
    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    session_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("device_sessions.id")
    )
    
    session: so.Mapped["DeviceSession"] = so.relationship(
        "DeviceSession", back_populates="events")
    event_type: so.Mapped[SessionEventType] = so.mapped_column(sa.Enum(SessionEventType))
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), server_default=sa.func.now())