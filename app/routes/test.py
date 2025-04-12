from fastapi import APIRouter, Depends, status
import sqlalchemy.orm as so
import sqlalchemy as sa
import app.schemas as sch
import app.models as md
import app.utils as u
import app.dependencies as deps


test_route = APIRouter(prefix="/test", tags=["test"])

# app layering

# save active apps to the session - update status
# post/put /session/save

# open/close the apps of the session on desktop
# post /session/restore

# creation/cloning states
# switching between sesstions, switch+restore


@test_route.get("/current-apps")
def get_current_apps():
    return u.get_running_applications()


@test_route.get("/device", response_model=sch.DeviceBase)
def get_device(device=Depends(deps.get_current_device)):
    return device


@test_route.get("/device/apps")
def get_device_apps(
    db: so.Session = Depends(deps.get_db),
    device: md.Device = Depends(deps.get_current_device),
):
    apps = u.get_running_applications()

    # updating applications data in db

    for app in apps:
        found_app = (
            db.query(md.Application)
            .filter(
                md.Application.device_id == device.id, md.Application.exe == app["exe"]
            )
            .first()
        )

        if not found_app:
            new_app = md.Application(**app, device_id=device.id)
            db.add(new_app)
            db.commit()

    return device.apps


@test_route.post("/device/session", status_code=status.HTTP_201_CREATED)
def create_session(
    *,
    db: so.Session = Depends(deps.get_db),
    device: md.Device = Depends(deps.get_current_device),
    device_session: sch.DeviceSessionIn,
):
    device_session_data = device_session.model_dump()
    new_device_session = md.DeviceSession(**device_session_data, device_id=device.id)
    db.add(new_device_session)
    db.commit()

    return {"message": "ok"}


@test_route.post("/device/session/save", status_code=status.HTTP_201_CREATED)
def save_session(
    *,
    db: so.Session = Depends(deps.get_db),
    device: md.Device = Depends(deps.get_current_device),
):
    current_device_session = device.sessions[0]
    apps = u.get_running_applications()

    # updating applications data in db

    for app in apps:
        found_app = (
            db.query(md.Application)
            .filter(
                md.Application.device_id == device.id, md.Application.exe == app["exe"]
            )
            .first()
        )

        if not found_app:
            new_app = md.Application(**app, device_id=device.id)
            db.add(new_app)
            db.commit()

    # deleting all states
    old_session_apps = db.query(md.DeviceSessionApps).all()

    for app in old_session_apps:
        db.delete(app)
        db.commit()

    # adding new states

    for app in apps:
        found_app = (
            db.query(md.Application)
            .filter(
                md.Application.device_id == device.id, md.Application.exe == app["exe"]
            )
            .first()
        )

        if found_app:
            app_state = md.DeviceSessionApps(
                device_session_id=current_device_session.id, application_id=found_app.id
            )
            db.add(app_state)
            db.commit()

    return {"message": "saved"}


@test_route.post("/device/session/restore")
def restore_session(
    *,
    db: so.Session = Depends(deps.get_db),
    device: md.Device = Depends(deps.get_current_device),
):
    current_device_session = device.sessions[0]

    apps_to_restore = [
        sch.ApplicationBase.model_validate(app).model_dump()
        for app in current_device_session.apps
    ]

    u.run_applications(apps_to_restore)

    return {"message": "restored"}


@test_route.get("/device/session", response_model=list[sch.DeviceSessionOut])
def get_sessions(
    device: md.Device = Depends(deps.get_current_device),
):
    return device.sessions
