from fastapi import Depends
from sqlalchemy.orm import Session
from ..models import User
from .database import get_db
from .user import get_current_user
from ..services.device import DeviceService


def get_current_device(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return DeviceService(db).create_or_get_device(current_user.id)
