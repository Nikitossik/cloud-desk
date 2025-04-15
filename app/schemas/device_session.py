from pydantic import BaseModel, ConfigDict, model_validator
import datetime
from typing_extensions import Self
from coolname import generate_slug
from slugify import slugify


class DeviceSessionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    slugname: str | None = None


class DeviceSessionIn(DeviceSessionBase):
    @model_validator(mode="after")
    def chec_session_name(self) -> Self:
        if not self.name or len(self.name.strip()) == 0:
            slugname = generate_slug(3)
            self.name = slugname
            self.slugname = slugname

        else:
            self.slugname = slugify(self.name, max_length=150, word_boundary=True)
        return self


class DeviceSessionOut(DeviceSessionBase):
    is_active: bool = False
    created_at: datetime.datetime
    saved_at: datetime.datetime | None
    restored_at: datetime.datetime | None
    last_active_at: datetime.datetime | None
