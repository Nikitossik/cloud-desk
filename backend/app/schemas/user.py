from pydantic import BaseModel, Field, EmailStr, ConfigDict


class Token(BaseModel):
    access_token: str = Field(
        description="Access token used to authenticate API requests."
    )
    refresh_token: str = Field(
        description="Refresh token used to obtain a new access token."
    )
    token_type: str = Field(description="Type of the token. Usually 'bearer'.")


class TokenPayload(BaseModel):
    sub: int = Field(description="Subject identifier. Represents the user's ID.")
    exp: int = Field(
        description="Expiration time of the token in Unix timestamp format."
    )


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


class UserOut(UserBase):
    id: int = Field(
        description="ID of a new registered user in database.",
    )
