from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import UserSession

from .schemas import UserInDB
import app.utils as u
from .models import Device

from typing import Annotated


def get_current_user(
    *, db: Session = Depends(get_db), session_id: Annotated[str | None, Cookie()] = None
):
    if not session_id:
        return None

    user_session = db.query(UserSession).where(UserSession.id == session_id).first()

    return user_session.user


def get_current_device(*, db: Session = Depends(get_db)):
    mac_address = u.get_mac_address()
    device = db.query(Device).filter(Device.mac_address == mac_address).first()

    if not device:
        device_info = u.get_device_info()
        device = Device(**device_info)
        db.add(device)
        db.commit()

    return device


def get_active_session(*, device: Device = Depends(get_current_device)):
    active_session = device.get_active_session()

    if not active_session:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No active sessions at the moment",
        )

    return active_session
