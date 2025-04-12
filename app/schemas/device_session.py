from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
import datetime


class DeviceSessionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None


class DeviceSessionIn(DeviceSessionBase):
    pass


class DeviceSessionOut(DeviceSessionBase):
    created_at: datetime.datetime
