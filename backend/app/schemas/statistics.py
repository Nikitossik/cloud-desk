from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID


class StatisticsAppUsageOut(BaseModel):
    session_id: UUID = Field(description="Session identifier.")
    session_name: str = Field(description="Session name where this app was used.")
    last_deleted_at: datetime | None = Field(default=None, description="Soft-delete timestamp if the session is in trash.")
    total_time: int = Field(description="Total usage time in seconds for this app in the session.")


class StatisticsAppOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    app_id: UUID = Field(description="Application identifier.")
    display_name: str = Field(description="Application display name.")
    total_time: int = Field(description="Total usage time in seconds for this app across all sessions.")
    usage: list[StatisticsAppUsageOut] = Field(
        default_factory=list,
        description="Per-session usage totals for the application.",
    )


class StatisticsSessionUsageOut(BaseModel):
    app_id: UUID = Field(description="Application identifier.")
    display_name: str = Field(description="Application display name.")
    total_time: int = Field(description="Total usage time in seconds for this app in the session.")


class StatisticsSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: UUID = Field(description="Session identifier.")
    session_name: str = Field(description="Session display name.")
    last_deleted_at: datetime | None = Field(default=None, description="Soft-delete timestamp if the session is in trash.")
    start_count: int = Field(default=0, description="Number of times the session was started.")
    restore_count: int = Field(default=0, description="Number of times the session was restored.")
    total_active_time: int = Field(default=0, description="Total active usage time in seconds.")
    usage: list[StatisticsSessionUsageOut] = Field(
        default_factory=list,
        description="Per-application usage totals for the session.",
    )
