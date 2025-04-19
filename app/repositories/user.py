from ..utils.repositories import BaseRepository
from ..models import User
from typing import Any


class UserRepository(BaseRepository):
    model = User

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
