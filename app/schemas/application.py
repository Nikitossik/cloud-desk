from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    exe: str
    cmdline: str


class ApplicationInDB(ApplicationBase):
    uuid: UUID = Field(default_factory=uuid4)
