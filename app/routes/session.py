from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.schemas as sch
import app.models as md
import app.utils as u
from ..dependencies.database import get_db
from ..dependencies.device import get_current_device

from ..services import DeviceService, DeviceSessionService


session_route = APIRouter(prefix="/session", tags=["session"])


@session_route.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def create_session(
    *,
    db: so.Session = Depends(get_db),
    device: md.Device = Depends(get_current_device),
    device_session: sch.DeviceSessionIn,
):
    DeviceService(db).deactivate_sessions(device)
    return DeviceSessionService(db).create(device_session, device)


@session_route.get("/", response_model=list[sch.DeviceSessionOut])
def get_all_sessions(*, device: md.Device = Depends(get_current_device)):
    return device.sessions


@session_route.get("/{session_slug}", response_model=sch.DeviceSessionOut)
def get_session_by_slug(
    *,
    db: so.Session = Depends(get_db),
    device: md.Device = Depends(get_current_device),
    session_slug: str,
):
    return DeviceSessionService(db).get_by_slug(session_slug, device)


@session_route.post("/{session_slug}/activate")
def activate_sessin_by_slug(
    *,
    session_slug: str,
    device: md.Device = Depends(get_current_device),
    db: so.Session = Depends(get_db),
):
    return DeviceSessionService(db).activate_by_slug(session_slug, device)


@session_route.post(
    "/active/save",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def save_session(
    *, db: so.Session = Depends(get_db), device: md.Device = Depends(get_current_device)
):
    device_service = DeviceService(db)
    device_session_service = DeviceSessionService(db)

    device_service.sync_applications(device)
    return device_session_service.save_state(device)


@session_route.post("/{session_slug}/restore")
def restore_session(
    *,
    db: so.Session = Depends(get_db),
    device: md.Device = Depends(get_current_device),
    session_slug: str,
):
    return DeviceSessionService(db).restore_state(session_slug, device)
