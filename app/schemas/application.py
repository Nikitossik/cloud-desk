from pydantic import BaseModel, ConfigDict
from ..models import DeviceSessionApps
from datetime import datetime, timedelta


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    name: str
    exe: str
    cmdline: str


class ApplicationUsagePeriod(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    started_at: datetime
    ended_at: datetime


class ApplicationOut(ApplicationBase):
    pass


class ApplicationOutWithState(ApplicationOut):
    is_active: bool
    usage_periods: list[ApplicationUsagePeriod]
    total_seconds: int

    @classmethod
    def from_state(cls, app_state: DeviceSessionApps):
        return {
            "name": app_state.application.name,
            "exe": app_state.application.exe,
            "cmdline": app_state.application.cmdline,
            "is_active": app_state.is_active,
            "usage_periods": app_state.usage_periods,
            "total_seconds": int(
                sum(
                    [
                        period.duration.total_seconds()
                        for period in app_state.usage_periods
                    ]
                )
            ),
        }
