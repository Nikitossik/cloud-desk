from pydantic import BaseModel, ConfigDict, model_validator, Field
import datetime
from typing_extensions import Self
from typing import Any
from coolname import generate_slug
from slugify import slugify
from .application import ApplicationBase


class DeviceSessionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(
        default=None,
        description="Name of the session. If not provided - backend generates an automatic slugified name",
    )
    description: str | None = Field(
        default=None, description="Description of the session. Can be null."
    )
    slugname: str | None = Field(
        default=None,
        description="Slugified version of the session name used for URLs and identifiers.",
    )


class DeviceSessionIn(DeviceSessionBase):
    activate: bool = Field(
        default=True,
        description="Flag indicating if the session should be activated upon creation.",
    )

    @model_validator(mode="after")
    def check_session_name(self) -> Self:
        if not self.name or len(self.name.strip()) == 0:
            slugname = generate_slug(3)
            self.name = slugname
            self.slugname = slugname
        else:
            self.slugname = slugify(self.name, max_length=150, word_boundary=True)
        return self

class DeviceSessionOut(DeviceSessionBase):
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
