from . import Base
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.utils as u
import uuid
from ..database import get_db
from datetime import datetime

from typing import TYPE_CHECKING

from .user import User
from .application import Application
from .device_session import DeviceSession


class Device(Base):
    __tablename__ = "device"

    id: so.Mapped[str] = so.mapped_column(
        sa.Uuid(), primary_key=True, default=uuid.uuid4
    )
    mac_address: so.Mapped[str] = so.mapped_column(
        sa.String(17), default=u.get_mac_address, unique=True
    )
    name: so.Mapped[str | None]
    os_name: so.Mapped[str]
    os_release: so.Mapped[str]
    os_release_ver: so.Mapped[str]
    architecture: so.Mapped[str]
    created_at = so.mapped_column(sa.DateTime(), server_default=sa.func.now())

    # user = so.relationship("User", back_populates="devices")
    apps: so.Mapped[list["Application"]] = so.relationship(back_populates="device")
    sessions: so.Mapped[list["DeviceSession"]] = so.relationship(
        back_populates="device"
    )

    def update_applications(self, applications_data, db):
        for app in applications_data:
            found_app = list(filter(lambda x: x.exe == app["exe"], self.apps))

            if len(found_app) != 0:
                continue

            new_app = Application(**app)
            self.apps.append(new_app)
            db.commit()
            db.refresh(new_app)

    def deactivate_sessions(self, db):
        for session in self.sessions:
            session.is_active = False
            db.commit()
            db.refresh(session)

    def activate_session(self, session_id: str, db):
        for session in self.sessions:
            session.is_active = session.id == session_id
            db.commit()
            db.refresh(session)

    def get_active_session(self):
        for session in self.sessions:
            if session.is_active:
                return session

        return None

    def __repr__(self):
        return f"Device({self.mac_address})"
