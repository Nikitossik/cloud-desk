from typing import Annotated

from fastapi import Depends, Query, WebSocketException
from sqlalchemy.orm import Session

from .database import get_db
from .user import get_current_user_by_token
from ..models import Device, DeviceSession, User
from ..services import DeviceService, DeviceSessionService


def get_ws_access_token(token: str | None = Query(default=None)) -> str:
    if not token:
        raise WebSocketException(code=4401, reason="Missing access token")

    return token


def get_device_fingerprint_ws(device_fingerprint: str | None = Query(default=None)) -> str:
    if not device_fingerprint:
        raise WebSocketException(code=4400, reason="Missing device fingerprint")

    return device_fingerprint


def get_current_user_ws(
    *,
    db: Session = Depends(get_db),
    token: Annotated[str, Depends(get_ws_access_token)],
) -> User:
    try:
        return get_current_user_by_token(db=db, token=token)
    except Exception as exc:
        raise WebSocketException(code=4401, reason="Could not validate credentials") from exc


def get_current_device_ws(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_ws),
    device_fingerprint: Annotated[str, Depends(get_device_fingerprint_ws)],
) -> Device:
    return DeviceService(db).create_or_get_device(current_user.id, device_fingerprint)


def get_supported_device_ws(
    *,
    device: Device = Depends(get_current_device_ws),
) -> Device:
    if device.is_supported_os:
        return device

    raise WebSocketException(code=4403, reason="DEVICE_OS_NOT_SUPPORTED")


def get_active_session_ws(
    *,
    db: Session = Depends(get_db),
    device: Device = Depends(get_current_device_ws),
) -> DeviceSession:
    try:
        return DeviceSessionService(db).get_active_session(device)
    except Exception as exc:
        raise WebSocketException(code=4404, reason="No active session") from exc
