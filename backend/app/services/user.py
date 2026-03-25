from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Any
from ..repositories import UserRepository, DeviceRepository
from ..schemas.user import UserIn, UserUpdate
from ..schemas.sidebar import UserSidebarOut
from ..models import User, Device
import jwt
import app.utils.security as us
from ..config import setting


class UserService:
    def __init__(self, db: Session):
        self.user_repo: UserRepository = UserRepository(db)
        self.device_repo: DeviceRepository = DeviceRepository(db)
        
    def get(self, user_id: int) -> User:
        user = self.user_repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def update(self, user_id: int, user_update: UserUpdate) -> User:
        found_user = self.get(user_id)
        
        user_data = user_update.model_dump(exclude_none=True)
        
        if user_data.get('password'):
            user_data['password_hash'] = us.get_password_hash(user_data.pop('password'))
        
        updated_user = self.user_repo.update(found_user, user_data)
        return updated_user
    
    def get_sidebar_data(self, current_user: User, current_device: Device) -> UserSidebarOut:
        user_devices = current_user.devices
        existing_sessions = [session for session in current_device.sessions if session.last_deleted_at is None]
        deleted_sessions = [session for session in current_device.sessions if session.last_deleted_at is not None]
        
        for device in user_devices:
            device.is_current = (device.id == current_device.id)
        
        return UserSidebarOut(
            devices=user_devices,
            sessions=existing_sessions,
            deleted_sessions_count=len(deleted_sessions)
        )