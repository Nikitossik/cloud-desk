from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..models import User
import app.utils.security as us
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from ..schemas import Token, UserBase, UserIn
from ..services import AuthService

auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.post("/signup", response_model=UserBase)
def sign_up_user(*, db: Session = Depends(get_db), user_in: UserIn):
    return AuthService(db).signup_user(user_in)


@auth_route.post("/token", response_model=Token)
def login_for_token_pair(
    *,
    db: Session = Depends(get_db),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return AuthService(db).create_token_pair(form_data.username, form_data.password)


@auth_route.post("/refresh", response_model=Token)
def refresh_access_token(
    *,
    db: Session = Depends(get_db),
    refresh_token: Annotated[str, Header(alias="X-Refresh-Token")],
):
    return AuthService(db).refresh_access_token(refresh_token)


@auth_route.get("/me", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
