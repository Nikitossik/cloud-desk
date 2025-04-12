from . import Base
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.utils as u
import uuid
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .application import Application


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

    def __repr__(self):
        return f"Device({self.mac_address})"
