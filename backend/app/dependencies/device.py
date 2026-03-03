from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from ..models import User
from .database import get_db
from .user import get_current_user
from ..services.device import DeviceService

def get_device_fingerprint(x_device_fingerprint: str | None = Header(default=None)) -> str:
    if not x_device_fingerprint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-Device-Fingerprint header",
        )
    return x_device_fingerprint

def get_current_device(
    *, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user), 
    device_fingerprint: str = Depends(get_device_fingerprint)
):
    return DeviceService(db).create_or_get_device(current_user.id, device_fingerprint)
