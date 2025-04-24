from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.schemas as sch
import app.models as md
import app.utils.core as uc
import app.dependencies as d
from ..services import DeviceService, DeviceSessionService


session_route = APIRouter(prefix="/session", tags=["session"])


@session_route.get("/active-apps", response_model=list[sch.ApplicationBase])
def get_all_active_apps_data(current_user: md.User = Depends(d.get_current_user)):
    return [app for app in uc.get_running_applications().values()]


@session_route.get("/", response_model=list[sch.DeviceSessionOut])
def get_all_sessions(*, device: md.Device = Depends(d.get_current_device)):
    return device.sessions


@session_route.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def create_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    device_session: sch.DeviceSessionIn,
):
    return DeviceSessionService(db).create_session(device_session, device)


@session_route.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_sessions(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
):
    DeviceSessionService(db).delete_all_sessions(device)


@session_route.get("/{session_slug}", response_model=sch.DeviceSessionOut)
def get_session_by_slug(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    session_slug: str,
):
    return DeviceSessionService(db).get_session_by_slugname(session_slug, device)


@session_route.post(
    "/{session_slug}/clone",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def clone_session_with_slugname(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    slugname: str,
    device_session: sch.DeviceSessionIn,
):
    return DeviceSessionService(db).clone_session_by_slugname(
        slugname, device_session, device
    )


@session_route.delete("/{session_slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session_by_slug(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    session_slug: str,
):
    DeviceSessionService(db).delete_session_by_slugname(session_slug, device)


@session_route.post("/{session_slug}/activate")
def activate_sessin_by_slug(
    *,
    session_slug: str,
    device: md.Device = Depends(d.get_current_device),
    db: so.Session = Depends(d.get_db),
):
    return DeviceSessionService(db).activate_session_by_slug(session_slug, device)


@session_route.post("/{session_slug}/restore")
def restore_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    session_slug: str,
):
    return DeviceSessionService(db).restore_session_by_slug(session_slug, device)
