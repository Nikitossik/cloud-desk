from fastapi import APIRouter, Depends, status
import sqlalchemy.orm as so
from typing import Annotated
import app.schemas as sch
import app.models as md
from ..services import DeviceService
from ..dependencies.database import get_db
from ..dependencies.device import get_current_device
from pathlib import Path

device_route = APIRouter(prefix="/device", tags=["device"])
DOCS_PATH = Path(__file__).parent.parent.parent / "api_docs" / "device"


@device_route.get(
    "/",
    description=(DOCS_PATH / "get_device.md").read_text(),
    summary="Retrieves details about the currently registered device.",
    response_model=sch.DeviceBase,
)
def get_device(device: Annotated[md.Device, Depends(get_current_device)]):
    return device


@device_route.delete(
    "/",
    description=(DOCS_PATH / "delete_device.md").read_text(),
    summary="Deletes the currently registered device from the system.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_current_device(
    db: Annotated[so.Session, Depends(get_db)],
    device: Annotated[md.Device, Depends(get_current_device)],
):
    DeviceService(db).delete_device(device)


@device_route.get(
    "/apps",
    description=(DOCS_PATH / "get_device_apps.md").read_text(),
    summary="Synchronizes the device's applications that were opened in sessions so far and retrieves the list.",
)
def get_device_apps(
    db: Annotated[so.Session, Depends(get_db)],
    device: Annotated[md.Device, Depends(get_current_device)],
):
    return DeviceService(db).sync_applications(device)
