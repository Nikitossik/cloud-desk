from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from typing import Annotated
import jwt
from ..schemas.user import TokenPayload
from ..repositories import UserRepository
from ..config import setting
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

expired_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    *, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = jwt.decode(
            jwt=token, key=setting.ACCESS_SECRET_KEY, algorithms=[setting.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

    except jwt.exceptions.ExpiredSignatureError:
        raise expired_token_exception
    except (jwt.exceptions.InvalidTokenError, ValidationError):
        raise credentials_exception

    user = UserRepository(db).get(token_data.sub)

    if user is None:
        raise credentials_exception
    return user
