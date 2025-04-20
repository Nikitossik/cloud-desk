from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime, timezone
from ..config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
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
    data: dict, expiry_minutes: int = int(setting.REFRESH_TOKEN_EXPIRE_MINUTES)
):
    data_to_encode = data.copy()

    expiration_datetime = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)

    data_to_encode.update({"exp": expiration_datetime})
    return jwt.encode(
        payload=data_to_encode,
        key=setting.REFRESH_SECRET_KEY,
        algorithm=setting.ALGORITHM,
    )
