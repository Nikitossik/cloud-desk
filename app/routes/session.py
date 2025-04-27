from fastapi import APIRouter, Depends, status
import sqlalchemy.orm as so
import app.schemas as sch
import app.models as md
import app.dependencies as d
from ..services import DeviceSessionService
from typing import Annotated
from pathlib import Path

session_route = APIRouter(prefix="/session", tags=["session"])
DOCS_PATH = Path(__file__).parent.parent.parent / "api_docs" / "session"


@session_route.get(
    "/",
    description=(DOCS_PATH / "get_session_all.md").read_text(),
    summary="Retrieves a list of all saved sessions for the authenticated user's device.",
    response_model=list[sch.DeviceSessionOut],
)
def get_all_sessions(
    *,
    device: Annotated[md.Device, Depends(d.get_current_device)],
):
    return device.sessions


@session_route.post(
    "/",
    description=(DOCS_PATH / "post_session_create.md").read_text(),
    summary=("Creates a new session for the authenticated user's device.",),
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def create_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    device_session: sch.DeviceSessionIn,
):
    return DeviceSessionService(db).create_session(device_session, device)


@session_route.delete(
    "/",
    description=(DOCS_PATH / "delete_session_all.md").read_text(),
    summary="Deletes all saved sessions associated with the authenticated device.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_all_sessions(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
):
    DeviceSessionService(db).delete_all_sessions(device)


@session_route.get(
    "/{session_slug}",
    description=(DOCS_PATH / "get_session_by_slug.md").read_text(),
    summary=("Retrieves details of a specific saved session based on its slugname.",),
    response_model=sch.DeviceSessionOut,
)
def get_session_by_slug(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    return DeviceSessionService(db).get_session_by_slugname(session_slug, device)


@session_route.get(
    "/{session_slug}/apps",
    description=(DOCS_PATH / "get_session_apps.md").read_text(),
    summary=("Retrieves a list of applications associated with the given session.",),
    response_model=list[sch.ApplicationOutWithState],
)
def get_session_apps(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    session = DeviceSessionService(db).get_session_by_slugname(session_slug, device)
    return [
        sch.ApplicationOutWithState.from_state(app_state)
        for app_state in session.app_states
    ]


@session_route.post(
    "/{session_slug}/clone",
    description=(DOCS_PATH / "post_session_clone.md").read_text(),
    summary=(
        "Creates a new session by cloning an existing saved session.",
        "If no session name is provided for the clone, a slugified name will be automatically generated.",
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def clone_session_with_slugname(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    slugname: str,
    device_session: sch.DeviceSessionIn,
):
    return DeviceSessionService(db).clone_session_by_slugname(
        slugname, device_session, device
    )


@session_route.delete(
    "/{session_slug}",
    description=(DOCS_PATH / "delete_session_by_slug.md").read_text(),
    summary="Deletes a saved session based on its slugname.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session_by_slug(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    DeviceSessionService(db).delete_session_by_slugname(session_slug, device)


@session_route.post(
    "/{session_slug}/activate",
    description=(DOCS_PATH / "post_session_activate.md").read_text(),
    summary="Activates the selected saved session for the authenticated device.",
    response_model=sch.DeviceSessionOut,
)
def activate_sessin_by_slug(
    *,
    session_slug: str,
    device: Annotated[md.Device, Depends(d.get_current_device)],
    db: Annotated[so.Session, Depends(d.get_db)],
):
    return DeviceSessionService(db).activate_session_by_slug(session_slug, device)


@session_route.post(
    "/{session_slug}/restore",
    description=(DOCS_PATH / "post_session_restore.md").read_text(),
    summary="Restores a saved session and optionally reopens applications according to the saved session state.",
    response_model=sch.DeviceSessionOut,
)
def restore_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    return DeviceSessionService(db).restore_session_by_slug(session_slug, device)
