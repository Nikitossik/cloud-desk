from pydantic import BaseModel, Field, ConfigDict


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    exe: str
    cmdline: str
