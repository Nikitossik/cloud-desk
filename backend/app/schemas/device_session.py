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
    is_deleted: bool | None = Field(
        default=None,
        description="Flag indicating if the session should be deleted. If true, other fields are ignored.",
    )


class DeviceSessionTrashActionIn(BaseModel):
    session_ids: list[UUID] | None = Field(
        default=None,
        description="List of deleted session IDs to process.",
    )
    all: bool = Field(
        default=False,
        description="When true, applies action to all deleted sessions for the current device.",
    )

    @model_validator(mode="after")
    def validate_payload(self) -> Self:
        has_session_ids = bool(self.session_ids)

        if self.all and has_session_ids:
            raise ValueError("Provide either 'all=true' or 'session_ids', not both")

        if not self.all and not has_session_ids:
            raise ValueError("Provide 'all=true' or a non-empty 'session_ids' list")

        return self
        
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
    last_restored_at: datetime.datetime | None = Field(
        default=None,
        description="Timestamp when the session was last restored.",
    )
    last_active_at: datetime.datetime | None = Field(
        default=None,
        description="Timestamp when the session was last active.",
    )
    last_deleted_at: datetime.datetime | None = Field(
        default=None,
        description="Timestamp when the session was deleted. Null if the session is active.",
    )
    

class DeviceSessionWithReport(DeviceSessionOut):
    report: list[ApplicationRestoreReportOut]