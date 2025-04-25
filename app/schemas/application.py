from pydantic import BaseModel, ConfigDict
from ..models import DeviceSessionApps


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    name: str
    exe: str
    cmdline: str


class ApplicationOut(ApplicationBase):
    pass


class ApplicationOutWithState(ApplicationOut):
    is_active: bool

    @classmethod
    def from_state(cls, app_state: DeviceSessionApps):
        return {
            "name": app_state.application.name,
            "exe": app_state.application.exe,
            "cmdline": app_state.application.cmdline,
            "is_active": app_state.is_active,
        }
