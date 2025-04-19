from fastapi import HTTPException, status

from ..repositories import UserRepository
from ..schemas import UserIn, UserBase, Token
from ..models import User
from sqlalchemy.orm import Session

import app.utils.security as us


class UserService:
    def __init__(self, db: Session):
        self.user_repo: UserRepository = UserRepository(db)

    def get_user_by_id(self, user_id) -> User:
        return self.user_repo.get(user_id)

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

    def create_access_token(self, user_email: str, user_password: str) -> Token:
        user = self.authenticate_user(user_email, user_password)

        access_token = us.create_access_token(data={"sub": str(user.id)})

        return Token(access_token=access_token, token_type="bearer")
