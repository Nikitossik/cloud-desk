from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class StatisticsAppUsageOut(BaseModel):
    session_name: str = Field(description="Session name where this app was used.")
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
    usage: list[StatisticsSessionUsageOut] = Field(
        default_factory=list,
        description="Per-application usage totals for the session.",
    )
