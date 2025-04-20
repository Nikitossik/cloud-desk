from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from ..repositories import UserRepository
from ..schemas import UserIn, TokenPayload
from ..models import User
import jwt
import app.utils.security as us
from ..config import setting


class AuthService:
    def __init__(self, db: Session):
        self.user_repo: UserRepository = UserRepository(db)

    def signup_user(self, user: UserIn) -> User:
        user_data = user.model_dump()

        found_user = self.user_repo.get_by_email(user_data["email"])

        if found_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )

        user_data.update({"password_hash": us.get_password_hash(user_data["password"])})

        user = self.user_repo.create(user_data)
        return user

    def authenticate_user(self, user_email: str, user_password: str) -> User:
        user = self.user_repo.get_by_email(email=user_email)

        if not user or not us.verify_password(user_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_token_pair(self, user_email: str, user_password: str):
        user = self.authenticate_user(user_email, user_password)

        token_data = {"sub": str(user.id)}

        access_token = us.create_access_token(token_data)
        refresh_token = us.create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_access_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, setting.REFRESH_SECRET_KEY, setting.ALGORITHM
            )

            token_data = TokenPayload(**payload)
            new_access_token = us.create_access_token({"sub": token_data.sub})

            return {
                "access_token": new_access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired refresh token"
            )
        except (jwt.exceptions.InvalidTokenError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
