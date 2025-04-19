from pydantic import BaseModel, Field, EmailStr, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class UserBase(BaseModel):
    name: str = Field(max_length=20)
    surname: str = Field(max_length=20)
    email: EmailStr


class UserIn(UserBase):
    password: str = Field(min_length=6)
