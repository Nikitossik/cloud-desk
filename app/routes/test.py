from fastapi import APIRouter, Depends
import sqlalchemy.orm as so
import app.schemas as sch
import app.models as md
import app.utils as u
import app.dependencies as deps


test_route = APIRouter(prefix="/test", tags=["test"])

# app layering

# create session model
# get /session - get the current db session

# save active apps to the session - update status
# post/put /session/save

# open/close the apps of the session on desktop
# post /session/restore


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
