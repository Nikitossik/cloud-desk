from .base import BaseRepository
from ..models import User


class UserRepository(BaseRepository):
    model = User

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
