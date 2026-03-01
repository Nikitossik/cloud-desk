from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Any
from ..repositories import UserRepository
from ..schemas.user import UserIn, UserUpdate
from ..models import User
import jwt
import app.utils.security as us
from ..config import setting


class UserService:
    def __init__(self, db: Session):
        self.user_repo: UserRepository = UserRepository(db)
        
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