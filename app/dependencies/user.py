from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from typing import Annotated
import jwt
import app.utils.security as us
from ..schemas import TokenData
from ..services import UserService

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
        payload = us.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)

    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    except jwt.exceptions.ExpiredSignatureError:
        raise expired_token_exception

    user = UserService(db).get_user_by_id(token_data.id)

    if user is None:
        raise credentials_exception
    return user
