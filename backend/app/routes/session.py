from fastapi import APIRouter, Depends, status
import sqlalchemy.orm as so
from ..schemas.device_session import DeviceSessionIn, DeviceSessionOut, DeviceSessionUpdate, DeviceSessionWithReport, DeviceSessionTrashPurgeIn
from ..schemas.application import FullApplicationOut, ApplicationMiniOut
import app.models as md
import app.dependencies as d
from ..services import DeviceSessionService, DeviceService
from typing import Annotated
from pathlib import Path
from uuid import UUID

session_route = APIRouter(prefix="/session", tags=["session"])
SESSION_DOCS_PATH = Path(__file__).parent.parent.parent / "docs" / "session"
ACTIVE_SESSION_DOCS_PATH = SESSION_DOCS_PATH / "active"
BY_ID_SESSION_DOCS_PATH = SESSION_DOCS_PATH / "by-id"
BY_SLUG_SESSION_DOCS_PATH = SESSION_DOCS_PATH / "by-slug"

@session_route.get(
    "/",
    description=(SESSION_DOCS_PATH / "get_session_all.md").read_text(),
    summary="Retrieves a list of all saved sessions for the authenticated user's device.",
    response_model=list[DeviceSessionOut],
)
def get_all_sessions(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    deleted_only: bool = False
):
    return DeviceSessionService(db).get_all_sessions(device, deleted_only)


@session_route.post(
    "/",
    description=(SESSION_DOCS_PATH / "post_session_create.md").read_text(),
    summary=("Creates a new session for the authenticated user's device.",),
    status_code=status.HTTP_201_CREATED,
    response_model=DeviceSessionOut,
)
def create_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    device_session: DeviceSessionIn,
):
    return DeviceSessionService(db).create_session(device_session, device)


@session_route.delete(
    "/",
    description=(SESSION_DOCS_PATH / "delete_session_all.md").read_text(),
    summary="Deletes all saved sessions associated with the authenticated device.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_all_sessions(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
):
    DeviceSessionService(db).delete_all_sessions(device)


@session_route.post(
    "/trash/purge",
    description=(SESSION_DOCS_PATH / "post_session_trash_purge.md").read_text(),
    summary="Permanently deletes deleted sessions from trash.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def purge_trash_sessions(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    purge_data: DeviceSessionTrashPurgeIn,
):
    DeviceSessionService(db).purge_trash(device, purge_data)
    return None
    
@session_route.get(
    "/active",
    description=(ACTIVE_SESSION_DOCS_PATH / "get_active_session.md").read_text(),
    summary=(
        "Retrieves details about the current active session for the authenticated user's device.",
        "If no active session is found, the API returns a 404 error with a specific message.",
        "This behavior applies to all operations involving an active session.",
    ),
    response_model=DeviceSessionOut,
)
def get_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    return active_session

@session_route.patch(
    "/active",
    description=(ACTIVE_SESSION_DOCS_PATH / "patch_active_session.md").read_text(),
    response_model=DeviceSessionOut,
)
def update_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device_update: DeviceSessionUpdate,
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    return DeviceSessionService(db).update_session(active_session, device_update, device)

@session_route.delete(
    "/active",
    description=(ACTIVE_SESSION_DOCS_PATH / "delete_active_session.md").read_text(),
    summary="Deletes the current active session associated with the authenticated device.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    return DeviceSessionService(db).delete_session(active_session)

@session_route.post(
    "/active/stop",
    description=(ACTIVE_SESSION_DOCS_PATH / "stop_active_session.md").read_text(),
    summary=(
        "Optionally saves application usage data before stopping.",
        "Stops the current active session.",
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=DeviceSessionOut,
)
def stop_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)]
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).stop_session(active_session)


@session_route.post(
    "/active/restore",
    description=(ACTIVE_SESSION_DOCS_PATH / "restore_active_session.md").read_text(),
    summary="Restores the session associated with the authenticated device based on the stored slugname.",
    status_code=status.HTTP_201_CREATED,
    response_model=DeviceSessionWithReport,
)
def restore_active_session(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    active_session: Annotated[md.DeviceSession, Depends(d.get_active_session)],
):
    DeviceService(db).sync_applications(device)
    return DeviceSessionService(db).restore_session(
        active_session, device
    )

@session_route.get(
    "/{session_id}",
    description=(BY_ID_SESSION_DOCS_PATH / "get_session_by_id.md").read_text(),
    summary=("Retrieves details of a specific saved session based on its ID.",),
    response_model=DeviceSessionOut,
)
def get_session_by_id(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_id: UUID,
):
    return DeviceSessionService(db).get_session_by_id(session_id, device)

@session_route.patch(
    "/{session_id}",
    description=(BY_ID_SESSION_DOCS_PATH / "patch_session_by_id.md").read_text(),
    response_model=DeviceSessionOut,
)
def update_session_by_id(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device_update: DeviceSessionUpdate,
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_id: UUID,
):
    session = DeviceSessionService(db).get_session_by_id(session_id, device)
    return DeviceSessionService(db).update_session(session, device_update, device)


@session_route.delete(
    "/{session_id}",
    description=(BY_ID_SESSION_DOCS_PATH / "delete_session_by_id.md").read_text(),
    summary="Deletes a saved session based on its ID.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session_by_id(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_id: UUID,
):
    session = DeviceSessionService(db).get_session_by_id(session_id, device)
    DeviceSessionService(db).delete_session(session)


@session_route.post(
    "/{session_id}/start",
    description=(BY_ID_SESSION_DOCS_PATH / "post_session_by_id_start.md").read_text(),
    summary="Starts the selected saved session for the authenticated device.",
    response_model=DeviceSessionOut,
)
def start_session_by_id(
    *,
    session_id: UUID,
    device: Annotated[md.Device, Depends(d.get_current_device)],
    db: Annotated[so.Session, Depends(d.get_db)],
):
    session = DeviceSessionService(db).get_session_by_id(session_id, device)
    return DeviceSessionService(db).start_session(session, device)


@session_route.post(
    "/{session_id}/restore",
    description=(BY_ID_SESSION_DOCS_PATH / "post_session_by_id_restore.md").read_text(),
    summary="Restores a saved session and optionally reopens applications according to the saved session state.",
    response_model=DeviceSessionWithReport,
)
def restore_session_by_id(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_id: UUID,
):
    session = DeviceSessionService(db).get_session_by_id(session_id, device)
    return DeviceSessionService(db).restore_session(session, device)
    


@session_route.get(
    "/by-slug/{session_slug}",
    description=(BY_SLUG_SESSION_DOCS_PATH / "get_session_by_slug.md").read_text(),
    summary=("Retrieves details of a specific saved session based on its slugname.",),
    response_model=DeviceSessionOut,
)
def get_session_by_slug(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    return DeviceSessionService(db).get_session_by_slugname(session_slug, device)

@session_route.patch(
    "/by-slug/{session_slug}",
    description=(BY_SLUG_SESSION_DOCS_PATH / "patch_session_by_slug.md").read_text(),
    response_model=DeviceSessionOut,
)
def update_session_by_slug(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device_update: DeviceSessionUpdate,
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    session = DeviceSessionService(db).get_session_by_slugname(session_slug, device)
    return DeviceSessionService(db).update_session(session, device_update, device)


@session_route.get(
    "/by-slug/{session_slug}/apps",
    description=(BY_SLUG_SESSION_DOCS_PATH / "get_session_by_slug_apps.md").read_text(),
    response_model=list[ApplicationMiniOut],
)
def get_session_apps(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    session = DeviceSessionService(db).get_session_by_slugname(session_slug, device)
    return DeviceSessionService(db).get_apps(session)


@session_route.delete(
    "/by-slug/{session_slug}",
    description=(BY_SLUG_SESSION_DOCS_PATH / "delete_session_by_slug.md").read_text(),
    summary="Deletes a saved session based on its slugname.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session_by_slug(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    session = DeviceSessionService(db).get_session_by_slugname(session_slug, device)
    DeviceSessionService(db).delete_session(session)


@session_route.post(
    "/by-slug/{session_slug}/start",
    description=(BY_SLUG_SESSION_DOCS_PATH / "post_session_by_slug_start.md").read_text(),
    summary="Starts the selected saved session for the authenticated device.",
    response_model=DeviceSessionOut,
)
def start_session_by_slug(
    *,
    session_slug: str,
    device: Annotated[md.Device, Depends(d.get_current_device)],
    db: Annotated[so.Session, Depends(d.get_db)],
):
    session = DeviceSessionService(db).get_session_by_slugname(session_slug, device)
    return DeviceSessionService(db).start_session(session, device)


@session_route.post(
    "/by-slug/{session_slug}/restore",
    description=(BY_SLUG_SESSION_DOCS_PATH / "post_session_by_slug_restore.md").read_text(),
    summary="Restores a saved session and optionally reopens applications according to the saved session state.",
    response_model=DeviceSessionWithReport,
)
def restore_session_by_slug(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    session_slug: str,
):
    session = DeviceSessionService(db).get_session_by_slugname(session_slug, device)
    return DeviceSessionService(db).restore_session(session, device)
