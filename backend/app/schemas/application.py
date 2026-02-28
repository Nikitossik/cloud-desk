from pydantic import BaseModel, ConfigDict, Field
from ..models import SessionAppState
from datetime import datetime


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    name: str = Field(description="Name of the application.")
    exe: str = Field(description="Path to the executable file of the application.")
    cmdline: str = Field(description="Command line used to launch the application.")

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
    

class FullApplicationOut(ApplicationBase):
    is_active: bool = Field(
        description="Flag indicating if the application is currently active in the session."
    )
    usage_periods: list[ApplicationUsagePeriod] = Field(
        description="List of usage periods for the application during the session."
    )


