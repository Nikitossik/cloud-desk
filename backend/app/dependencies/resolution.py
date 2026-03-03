from fastapi import Header, HTTPException, status
from typing import Annotated
from pydantic import ValidationError
import jwt

from ..config import setting
from ..schemas.token import TokenPayload


def get_resolution_user_id(
    x_resolution_token: Annotated[str | None, Header(alias="X-Resolution-Token")] = None,
) -> int:
    if not x_resolution_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Resolution-Token header",
        )

    try:
        payload = jwt.decode(
            jwt=x_resolution_token,
            key=setting.RESOLUTION_SECRET_KEY,
            algorithms=[setting.ALGORITHM],
        )

        if payload.get("token_type") != "resolution":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid resolution token type",
            )

        token_data = TokenPayload(**payload)
        return token_data.sub
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired resolution token",
        )
    except (jwt.exceptions.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid resolution token",
        )
