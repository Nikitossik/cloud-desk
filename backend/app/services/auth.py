from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Any

from ..repositories import UserRepository
from ..schemas.user import UserIn
from ..schemas.token import TokenPayload
from ..models import User
import jwt
import app.utils.security as us
from ..config import setting
from .device import DeviceService


class AuthService:
    def __init__(self, db: Session):
        self.user_repo: UserRepository = UserRepository(db)
        self.device_service: DeviceService = DeviceService(db)

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

    def create_token_pair(
        self,
        user_email: str | None = None,
        user_password: str | None = None,
        user: User | None = None,
    ) -> dict[str, Any]:
        if user is None:
            if user_email is None or user_password is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User credentials are required",
                )
            user = self.authenticate_user(user_email, user_password)

        token_data = {"sub": str(user.id)}

        access_token = us.create_access_token(token_data)
        refresh_token = us.create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def login_with_device_resolution(
        self,
        user_email: str,
        user_password: str,
        fingerprint: str | None,
    ) -> dict[str, Any]:
        user = self.authenticate_user(user_email, user_password)

        if not fingerprint:
            return {
                "status": "device_resolution_required",
                "resolution_token": us.create_resolution_token({"sub": str(user.id)}),
            }

        found_device = self.device_service.device_repo.get_by_user_and_fingerprint(user.id, fingerprint)

        if not found_device:
            return {
                "status": "device_resolution_required",
                "resolution_token": us.create_resolution_token({"sub": str(user.id)}),
            }

        self.device_service.create_or_get_device(user.id, fingerprint)

        token_pair = self.create_token_pair(user=user)

        return {
            "status": "ok",
            "token": token_pair,
        }

    def get_devices_for_resolution(self, user_id: int):
        return self.device_service.device_repo.get_by_user_id(user_id)

    def resolve_device_rebind(
        self,
        user_id: int,
        target_device_id: str,
        new_fingerprint: str,
    ) -> dict[str, Any]:
        user = self.user_repo.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User for resolution token was not found",
            )

        self.device_service.bind_device_fingerprint(user_id, target_device_id, new_fingerprint)
        return self.create_token_pair(user=user)

    def resolve_device_create(
        self,
        user_id: int,
        new_fingerprint: str,
        display_name: str | None = None,
    ) -> dict[str, Any]:
        user = self.user_repo.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User for resolution token was not found",
            )

        self.device_service.create_device_with_fingerprint(
            user_id=user_id,
            new_fingerprint=new_fingerprint,
            display_name=display_name,
        )

        return self.create_token_pair(user=user)

    def cancel_device_resolution(self, user_id: int, remove_user: bool = False) -> None:
        if not remove_user:
            return

        found_user = self.user_repo.get(user_id)
        if not found_user:
            return

        self.user_repo.delete(user_id)

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                refresh_token, setting.REFRESH_SECRET_KEY, setting.ALGORITHM
            )

            token_data = TokenPayload(**payload)
            new_access_token = us.create_access_token({"sub": str(token_data.sub)})

            return {
                "access_token": new_access_token,
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
