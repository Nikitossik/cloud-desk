from fastapi import APIRouter, Depends, status, Query, HTTPException
import sqlalchemy.orm as so
import app.schemas as sch
import app.models as md
import app.dependencies as d
from ..services import DeviceService, DeviceSessionService
from typing import Annotated
from pathlib import Path

active_session_route = APIRouter(prefix="/active-session", tags=["active session"])
DOCS_PATH = Path(__file__).parent.parent.parent / "api_docs" / "active_session"


@active_session_route.get(
    "/",
    description=(DOCS_PATH / "get_active_session.md").read_text(),
    summary=(
        "Retrieves details about the current active session for the authenticated user's device.",
        "If no active session is found, the API returns a 404 error with a specific message.",
        "This behavior applies to all operations involving an active session.",
    ),
    response_model=sch.DeviceSessionOut,
)
def get_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
):
    return DeviceSessionService(db).get_active_session(device)


@active_session_route.get(
    "/apps",
    description=(DOCS_PATH / "get_active_session_apps.md").read_text(),
    summary="Retrieves a list of applications linked to the current active session, along with usage statistics.",
    response_model=list[sch.ApplicationOutWithState],
)
def get_active_session_apps(
    *,
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    return [
        sch.ApplicationOutWithState.from_state(app_state)
        for app_state in active_session.app_states
    ]


@active_session_route.delete(
    "/",
    description=(DOCS_PATH / "delete_active_session.md").read_text(),
    summary="Deletes the current active session associated with the authenticated device.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    return DeviceSessionService(db).delete_session(active_session)


@active_session_route.post(
    "/clone",
    description=(DOCS_PATH / "clone_active_session.md").read_text(),
    summary=(
        "Creates a new session by cloning the current active session.",
        "If no session name is provided, a slugified name will be automatically generated.",
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def clone_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    device_session: sch.DeviceSessionIn,
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    return DeviceSessionService(db).clone_session_by_slugname(
        active_session.slugname, device_session, device
    )


@active_session_route.post(
    "/save",
    description=(DOCS_PATH / "save_active_session.md").read_text(),
    summary="Saves the list of currently active applications for the active session.",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def save_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).save_session(active_session)


@active_session_route.post(
    "/enable-tracking",
    description=(DOCS_PATH / "enable_active_session_tracking.md").read_text(),
    summary="Enables tracking of active application usage within the current session.",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def enable_active_session_tracking(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).enable_session_tracking(active_session)


@active_session_route.post(
    "/disable-tracking",
    description=(DOCS_PATH / "disable_active_session_tracking.md").read_text(),
    summary=(
        "Disables tracking of active application usage within the current session.",
        "Optionally saves the application usage data before disabling tracking.",
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def disable_active_session_tracking(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
    save_usage: Annotated[bool, Query()] = True,
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).disable_session_tracking(active_session, save_usage)


@active_session_route.post(
    "/deactivate",
    description=(DOCS_PATH / "deactivate_active_session.md").read_text(),
    summary=(
        "Optionally saves application usage data before deactivation.",
        "Deactivates the current active session.",
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def deactivate_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
    save_usage: Annotated[bool, Query()] = True,
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).deactivate_session(active_session, save_usage)


@active_session_route.post(
    "/restore",
    description=(DOCS_PATH / "restore_active_session.md").read_text(),
    summary="Restores the session associated with the authenticated device based on the stored slugname.",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def restore_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).restore_session_by_slug(
        active_session.slugname, device
    )
