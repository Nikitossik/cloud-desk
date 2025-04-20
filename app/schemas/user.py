from pydantic import BaseModel, Field, EmailStr, ConfigDict
from .device import DeviceBase


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: int
    exp: int


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=20)
    surname: str = Field(max_length=20)
    email: EmailStr


class UserIn(UserBase):
    password: str = Field(min_length=6)


class UserOut(UserBase):
    id: int
    devices: list[DeviceBase]
