from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from ..services.device import DeviceService


def get_current_device(*, db: Session = Depends(get_db)):
    return DeviceService(db).create_or_get_device()
