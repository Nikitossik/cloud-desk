from fastapi import APIRouter, Depends, Header, Response, Cookie, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..models import User
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from ..schemas.user import Token, UserIn, UserOut
from ..services import AuthService
from pathlib import Path

auth_route = APIRouter(prefix="/auth", tags=["auth"])
DOCS_PATH = Path(__file__).parent.parent.parent / "api_docs" / "auth"


@auth_route.post(
    "/signup",
    description=(DOCS_PATH / "post_signup.md").read_text(),
    summary="Register a new user",
    response_model=UserOut,
)
def sign_up_user(*, db: Annotated[Session, Depends(get_db)], user_in: UserIn):
    return AuthService(db).signup_user(user_in)


@auth_route.post(
    "/token",
    description=(DOCS_PATH / "post_token.md").read_text(),
    summary="Authenticates the user and returns an access and refresh token.",
    response_model=Token,
)
def login_for_token_pair(
    *,
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response
):
    token_pair = AuthService(db).create_token_pair(form_data.username, form_data.password)
    
    response.set_cookie(key="refresh_token", 
        value=token_pair["refresh_token"], 
        httponly=True, 
        samesite="lax",
        secure=False,
        path="/auth")
    return token_pair


@auth_route.post(
    "/refresh",
    description=(DOCS_PATH / "post_refresh.md").read_text(),
    summary="Refreshes the access token by providing a valid refresh token.",
    response_model=Token,
)
def refresh_access_token(
    *,
    db: Annotated[Session, Depends(get_db)],
    refresh_token: Annotated[str | None, Cookie()],
):
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")
    
    return AuthService(db).refresh_access_token(refresh_token)


