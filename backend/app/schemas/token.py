from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str = Field(
        description="Access token used to authenticate API requests."
    )
    token_type: str = Field(description="Type of the token. Usually 'bearer'.")


class TokenPayload(BaseModel):
    sub: int = Field(description="Subject identifier. Represents the user's ID.")
    exp: int = Field(
        description="Expiration time of the token in Unix timestamp format."
    )