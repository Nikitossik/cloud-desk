from fastapi import APIRouter, Depends, status
import sqlalchemy.orm as so
import app.schemas as sch
import app.models as md
from ..services import DeviceService
from ..dependencies.database import get_db
from ..dependencies.device import get_current_device


device_route = APIRouter(prefix="/device", tags=["device"])


@device_route.get("/", response_model=sch.DeviceBase)
def get_device(device=Depends(get_current_device)):
    return device


@device_route.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_device(
    db: so.Session = Depends(get_db), device=Depends(get_current_device)
):
    DeviceService(db).delete(device)


@device_route.get("/apps")
def get_device_apps(
    db: so.Session = Depends(get_db),
    device: md.Device = Depends(get_current_device),
):
    return DeviceService(db).sync_applications(device)
