from pydantic import BaseModel, ConfigDict, Field
from ..models import DeviceSessionApps
from datetime import datetime


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    name: str = Field(description="Name of the application.")
    exe: str = Field(description="Path to the executable file of the application.")
    cmdline: str = Field(description="Command line used to launch the application.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Google Chrome",
                    "exe": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                    "cmdline": '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"',
                }
            ]
        }
    }


class ApplicationOut(ApplicationBase):
    pass


class ApplicationUsagePeriod(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    started_at: datetime = Field(
        description="Timestamp when the application usage period started."
    )
    ended_at: datetime = Field(
        description="Timestamp when the application usage period ended."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "started_at": "2024-04-26T10:00:00Z",
                    "ended_at": "2024-04-26T11:00:00Z",
                }
            ]
        }
    }


class ApplicationOutWithState(ApplicationOut):
    is_active: bool = Field(
        description="Flag indicating if the application is currently active in the session."
    )
    usage_periods: list[ApplicationUsagePeriod] = Field(
        description="List of periods when the application was actively used."
    )
    total_seconds: int = Field(
        description="Total number of seconds the application was actively used during the session."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Google Chrome",
                    "exe": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                    "cmdline": '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"',
                    "is_active": True,
                    "usage_periods": [
                        {
                            "started_at": "2024-04-26T10:00:00Z",
                            "ended_at": "2024-04-26T11:00:00Z",
                        }
                    ],
                    "total_seconds": 3600,
                }
            ]
        }
    }

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
