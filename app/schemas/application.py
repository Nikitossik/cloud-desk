from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    name: str
    exe: str
    cmdline: str
