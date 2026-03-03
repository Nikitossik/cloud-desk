from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        max_length=20,
        description="The user's first name. Must be a string of maximum 20 characters.",
    )
    surname: str = Field(
        max_length=20,
        description="The user's last name. Must be a string of maximum 20 characters.",
    )
    email: EmailStr = Field(
        description="The user's email address. Must be a valid email format."
    )


class UserIn(UserBase):
    password: str = Field(
        min_length=6,
        description="The user's password. Must be at least 6 characters long.",
    )

class UserUpdate(BaseModel):
    name: str | None = Field(None,
        max_length=20,
        description="The user's first name. Must be a string of maximum 20 characters.",
    )
    surname: str | None = Field(None,
        max_length=20,
        description="The user's last name. Must be a string of maximum 20 characters.",
    )
    password: str | None = Field(None,
        min_length=6,
        description="The user's password. Must be at least 6 characters long.",
    )
    
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if value is None or not value.strip():
            return None
        return value

class UserOut(UserBase):
    id: int = Field(
        description="ID of a new registered user in database.",
    )
