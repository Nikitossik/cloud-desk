from fastapi import Cookie, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Session as UserSession

from .schemas import UserInDB

from typing import Annotated


def get_current_user(
    *, db: Session = Depends(get_db), session_id: Annotated[str | None, Cookie()] = None
):
    if not session_id:
        return None

    user_session = db.query(UserSession).where(UserSession.id == session_id).first()

    return UserInDB.model_validate(user_session.user)
