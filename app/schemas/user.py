from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserBase(BaseModel):
    name: str = Field(max_length=20)
    surname: str = Field(max_length=20)
    email: EmailStr


class UserInDB(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="allow")


class UserIn(UserBase):
    password: str = Field(min_length=6)
