from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime, timezone
from typing import Any
import uuid

from ..config import setting


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict, expiry_minutes: int = int(setting.ACCESS_TOKEN_EXPIRE_MINUTES)
):
    data_to_encode = data.copy()

    expiration_datetime = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)

    data_to_encode.update({"exp": expiration_datetime})
    return jwt.encode(
        payload=data_to_encode,
        key=setting.ACCESS_SECRET_KEY,
        algorithm=setting.ALGORITHM,
    )


def create_refresh_token(
    data: dict, expiry_days: int = int(setting.REFRESH_TOKEN_EXPIRE_DAYS)
):
    data_to_encode = data.copy()

    expiration_datetime = datetime.now(timezone.utc) + timedelta(days=expiry_days)

    data_to_encode.update({"exp": expiration_datetime})
    return jwt.encode(
        payload=data_to_encode,
        key=setting.REFRESH_SECRET_KEY,
        algorithm=setting.ALGORITHM,
    )


def create_resolution_token(data: dict, expiry_minutes: int = int(setting.RESOLUTION_TOKEN_EXPIRE_MINUTES)):
    data_to_encode = data.copy()

    expiration_datetime = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)

    data_to_encode.update(
        {
            "exp": expiration_datetime,
            "token_type": "resolution",
            "jti": str(uuid.uuid4()),
        }
    )

    return jwt.encode(
        payload=data_to_encode,
        key=setting.RESOLUTION_SECRET_KEY,
        algorithm=setting.ALGORITHM,
    )
