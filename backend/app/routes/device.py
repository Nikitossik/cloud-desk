from fastapi import APIRouter, Depends, status
import sqlalchemy.orm as so
from typing import Annotated
from ..schemas.device import DeviceOut, DeviceUpdate
from ..schemas.application import ApplicationBase
import app.models as md
from ..services import DeviceService
from ..dependencies.database import get_db
from ..dependencies.device import get_current_device
from pathlib import Path

device_route = APIRouter(prefix="/device", tags=["device"])
DOCS_PATH = Path(__file__).parent.parent.parent / "api_docs" / "device"


@device_route.get(
    "/current",
    description=(DOCS_PATH / "get_device.md").read_text(),
    summary="Retrieves details about the currently registered device.",
    response_model=DeviceOut,
)
def get_device(current_device: Annotated[md.Device, Depends(get_current_device)]):
    return current_device


@device_route.patch(
    "/current",
    summary="Updates details about the currently registered device.",
    response_model=DeviceOut,
)
def update_device(
    device_update: DeviceUpdate,
    current_device: Annotated[md.Device, Depends(get_current_device)],
    db: Annotated[so.Session, Depends(get_db)],
):
    return DeviceService(db).update_current_device(current_device, device_update)

@device_route.delete(
    "/current",
    description=(DOCS_PATH / "delete_device.md").read_text(),
    summary="Deletes the currently registered device from the system.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_current_device(
    db: Annotated[so.Session, Depends(get_db)],
    current_device: Annotated[md.Device, Depends(get_current_device)],
):
    DeviceService(db).delete_device(current_device)


@device_route.get(
    "/current/apps",
    description=(DOCS_PATH / "get_device_apps.md").read_text(),
    summary="Retrieves the list of the device's applications.",
    response_model=list[ApplicationBase],
)
def get_device_apps(
    db: Annotated[so.Session, Depends(get_db)],
    current_device: Annotated[md.Device, Depends(get_current_device)],
):
    return current_device.apps
