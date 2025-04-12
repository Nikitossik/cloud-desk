from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __init__(self, **entries):
        # ignore extra keywords when creating an instance
        self.__dict__.update(entries)


from .user import User
from .device import Device
from .user_session import UserSession
from .application import Application
from .device_session import DeviceSession
from .device_session_apps import DeviceSessionApps
