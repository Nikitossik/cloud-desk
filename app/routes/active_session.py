from fastapi import APIRouter, Depends, status, HTTPException, Query
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.schemas as sch
import app.models as md
import app.utils.core as uc
import app.dependencies as d
from ..services import DeviceService, DeviceSessionService
from typing import Annotated

active_session_route = APIRouter(prefix="/active-session", tags=["active session"])


@active_session_route.get("/", response_model=sch.DeviceSessionOut)
def get_active_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
):
    return DeviceSessionService(db).get_active_session(device)


@active_session_route.get("/apps", response_model=list[sch.ApplicationOutWithState])
def get_active_session_apps(
    *,
    active_session: md.DeviceSession = Depends(d.get_active_session),
):
    return [
        sch.ApplicationOutWithState.from_state(app_state)
        for app_state in active_session.app_states
    ]


@active_session_route.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_active_session(
    *,
    db: so.Session = Depends(d.get_db),
    active_session: md.DeviceSession = Depends(d.get_active_session),
):
    return DeviceSessionService(db).delete_session(active_session)


@active_session_route.post(
    "/clone",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def clone_active_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    device_session: sch.DeviceSessionIn,
    active_session: md.DeviceSession = Depends(get_active_session),
):
    return DeviceSessionService(db).clone_session_by_slugname(
        active_session.slugname, device_session, device
    )


@active_session_route.post(
    "/save",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def save_active_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    active_session: md.DeviceSession = Depends(d.get_active_session),
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).save_session(active_session)


@active_session_route.post(
    "/enable-tracking",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def enable_active_session_tracking(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    active_session: md.DeviceSession = Depends(d.get_active_session),
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).enable_session_tracking(active_session)


@active_session_route.post(
    "/disable-tracking",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def disable_active_session_tracking(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    active_session: md.DeviceSession = Depends(d.get_active_session),
    save_usage: Annotated[bool, Query()] = True,
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).disable_session_tracking(active_session, save_usage)


@active_session_route.post(
    "/deactivate",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def deactivate_active_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    active_session: md.DeviceSession = Depends(d.get_active_session),
    save_usage: Annotated[bool, Query()] = True,
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).deactivate_session(active_session, save_usage)


@active_session_route.post(
    "/restore",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def restore_active_session(
    *,
    db: so.Session = Depends(d.get_db),
    device: md.Device = Depends(d.get_current_device),
    active_session: md.DeviceSession = Depends(get_active_session),
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).restore_session_by_slug(
        active_session.slugname, device
    )
