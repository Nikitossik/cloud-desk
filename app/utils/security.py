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
    data: dict, expires_in: int = setting.ACCESS_TOKEN_EXPIRE_MINUTES
):
    data_to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

    data_to_encode.update({"exp": expire})
    return jwt.encode(
        payload=data_to_encode, key=setting.SECRET_KEY, algorithm=setting.ALGORITHM
    )


def decode_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token, key=setting.SECRET_KEY, algorithms=[setting.ALGORITHM]
        )
        return payload
    except jwt.InvalidTokenError:
        return False
