from pydantic import BaseModel, Field
from uuid import UUID

class ResolveDeviceRebindIn(BaseModel):
    target_device_id: UUID
    new_fingerprint: str = Field(min_length=1)


class ResolveDeviceCreateIn(BaseModel):
    new_fingerprint: str = Field(min_length=1)
    display_name: str | None = Field(default=None, max_length=60)


class ResolveDeviceCancelIn(BaseModel):
    remove_user: bool = False
