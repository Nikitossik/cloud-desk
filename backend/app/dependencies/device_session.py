from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .device import get_current_device
from ..services import DeviceSessionService

from ..models import Device


def get_active_session(
    *, db: Session = Depends(get_db), device: Device = Depends(get_current_device)
):
    return DeviceSessionService(db).get_active_session(device)
