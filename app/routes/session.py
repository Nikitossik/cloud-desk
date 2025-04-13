from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.schemas as sch
import app.models as md
import app.utils as u
import app.dependencies as deps
from ..database import get_db


session_route = APIRouter(prefix="/session", tags=["session"])


@session_route.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.DeviceSessionOut,
)
def create_session(
    *,
    db: so.Session = Depends(get_db),
    device: md.Device = Depends(deps.get_current_device),
    device_session: sch.DeviceSessionIn,
):
    device_session_data = device_session.model_dump()

    session = md.DeviceSession(
        **device_session_data, device_id=device.id
    )  # already active by default

    # deactivating sessions before adding new one

    device.deactivate_sessions(db)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@session_route.get("/", response_model=list[sch.DeviceSessionOut])
def get_all_sessions(*, device: md.Device = Depends(deps.get_current_device)):
    return device.sessions


@session_route.get("/{session_slug}", response_model=sch.DeviceSessionOut)
def get_session_by_slug(
    *,
    device: md.Device = Depends(deps.get_current_device),
    session_slug: str,
):
    session_to_find = None

    for session in device.sessions:
        if session.slug_name == session_slug:
            session_to_find = session
            break

    if not session_to_find:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session with the given name was not found",
        )

    return session


@session_route.post("/{session_slug}/activate")
def activate_sessin_by_slug(
    *,
    session_slug: str,
    device: md.Device = Depends(deps.get_current_device),
    db: so.Session = Depends(get_db),
):
    session_to_find = None

    for session in device.sessions:
        if session.slug_name == session_slug:
            session_to_find = session
            break

    if not session_to_find:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session with the given name was not found",
        )

    device.activate_session(session_to_find.id, db)

    return {"message": "activated"}


@session_route.post("/save", status_code=status.HTTP_201_CREATED)
def save_session(
    *,
    db: so.Session = Depends(deps.get_db),
    active_session: md.DeviceSession = Depends(deps.get_active_session),
):
    apps = u.get_running_applications()

    # updating applications data in db

    active_session.device.update_applications(apps, db)

    # deleting all states
    old_session_apps = (
        db.query(md.DeviceSessionApps)
        .filter(md.DeviceSessionApps.device_session_id == active_session.id)
        .all()
    )

    for app in old_session_apps:
        db.delete(app)
        db.commit()

    # adding new states

    for app in apps:
        found_app = (
            db.query(md.Application)
            .filter(
                md.Application.device_id == active_session.device.id,
                md.Application.exe == app["exe"],
            )
            .first()
        )

        if found_app:
            app_state = md.DeviceSessionApps(
                device_session_id=active_session.id, application_id=found_app.id
            )
            db.add(app_state)
            db.commit()

    return {"message": "saved"}


@session_route.post("/{session_slug}/restore")
def restore_session(
    *,
    db: so.Session = Depends(deps.get_db),
    active_session: md.DeviceSession = Depends(deps.get_active_session),
    session_slug: str,
):
    session_to_find = None

    for session in active_session.device.sessions:
        if session.slug_name == session_slug:
            session_to_find = session
            break

    if not session_to_find:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session with the given name was not found",
        )

    apps_to_restore = [
        sch.ApplicationBase.model_validate(app).model_dump()
        for app in active_session.apps
    ]

    active_session.device.activate_session(session_to_find.id, db)

    u.run_applications(apps_to_restore)

    return {"message": "restored"}
