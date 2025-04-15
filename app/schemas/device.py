from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DeviceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mac_address: str = Field(max_length=17)
    name: str | None
    os_name: str
    os_release: str
    os_release_ver: str
    architecture: str
    created_at: datetime
