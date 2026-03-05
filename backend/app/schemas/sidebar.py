from pydantic import BaseModel, Field, ConfigDict
from .device import DeviceBaseExtended

class DeviceForSidebar(DeviceBaseExtended):
    is_current: bool = Field(description="Indicates whether this device is the current device being used.")

class SessionForSidebar(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    slugname: str = Field(description="The slug name of the session, used for URL paths.")
    name: str = Field(description="The display name of the session.")
    is_active: bool = Field(description="Indicates whether the session is currently active.")

class UserSidebarOut(BaseModel):
    devices: list[DeviceForSidebar]
    sessions: list[SessionForSidebar]