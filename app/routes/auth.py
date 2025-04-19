from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..models import User
import app.utils.security as us
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from ..schemas import Token, UserBase, UserIn
from ..services import UserService

auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.post("/signup", response_model=UserBase)
def sign_up_user(*, db: Session = Depends(get_db), user_in: UserIn):
    return UserService(db).signup_user(user_in)


@auth_route.post("/token", response_model=Token)
def login_for_access_token(
    *,
    db: Session = Depends(get_db),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return UserService(db).create_access_token(form_data.username, form_data.password)


@auth_route.get("/me", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
