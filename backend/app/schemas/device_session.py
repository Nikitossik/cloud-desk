from pydantic import BaseModel, ConfigDict, model_validator, Field
import datetime
from typing_extensions import Self
from uuid import UUID
from .application import ApplicationRestoreReportOut


class DeviceSessionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(
        default=None,
        description="Name of the session. If not provided - backend generates an automatic slugified name",
    )
    description: str | None = Field(
        default=None, description="Description of the session. Can be null."
    )

class DeviceSessionIn(DeviceSessionBase):
    start: bool = Field(
        default=True,
        description="Flag indicating if the session should be started upon creation.",
    )

class DeviceSessionUpdate(DeviceSessionBase):
    pass
        
class DeviceSessionOut(DeviceSessionBase):
    id: UUID = Field(description="Unique identifier for the session.")
    slugname: str = Field(
        default=None,
        description="Slugified version of the session name used for URLs and identifiers.",
    )
    is_active: bool = Field(
        default=True, description="Flag indicating if the session is currently active."
    )
    created_at: datetime.datetime = Field(
        description="Timestamp when the session was created."
    )
    saved_at: datetime.datetime | None = Field(
        default=None,
        description="Timestamp when the session was last saved.",
    )
    restored_at: datetime.datetime | None = Field(
        default=None,
        description="Timestamp when the session was last restored.",
    )
    last_active_at: datetime.datetime | None = Field(
        default=None,
        description="Timestamp when the session was last active.",
    )
    

class DeviceSessionWithReport(DeviceSessionOut):
    report: list[ApplicationRestoreReportOut]