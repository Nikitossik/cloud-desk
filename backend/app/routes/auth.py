from fastapi import APIRouter, Depends, Header, Response, Cookie, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pathlib import Path
import uuid
from ..dependencies import get_db, get_resolution_user_id
from sqlalchemy.orm import Session
from ..schemas.user import UserIn, UserOut
from ..schemas.token import Token
from ..schemas.device import DeviceOut
from ..schemas.device_resolution import (
    ResolveDeviceRebindIn,
    ResolveDeviceCreateIn,
    ResolveDeviceCancelIn,
)
from ..services import AuthService
from ..config import setting

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
    response: Response,
    x_device_fingerprint: Annotated[str | None, Header(alias="X-Device-Fingerprint")] = None,
):
    
    if not x_device_fingerprint and setting.DEBUG:
        x_device_fingerprint = form_data.client_id
    elif setting.DEBUG:
        x_device_fingerprint = str(uuid.uuid4())
    
    result = AuthService(db).login_with_device_resolution(
        form_data.username,
        form_data.password,
        x_device_fingerprint,
    )

    if result["status"] != "ok":
        raise HTTPException(
            status_code=409,
            detail={
                "code": "device_resolution_required",
                "resolution_token": result["resolution_token"],
            },
        )

    token_pair = result["token"]
    
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


@auth_route.post(
    "/device/resolve/devices",
    summary="Returns user's devices for device-resolution flow.",
    response_model=list[DeviceOut],
)
def get_devices_for_resolution(
    *,
    db: Annotated[Session, Depends(get_db)],
    resolution_user_id: Annotated[int, Depends(get_resolution_user_id)],
):
    return AuthService(db).get_devices_for_resolution(resolution_user_id)


@auth_route.post(
    "/device/resolve/rebind",
    summary="Binds selected existing device to new fingerprint and returns auth tokens.",
    response_model=Token,
)
def resolve_device_rebind(
    *,
    db: Annotated[Session, Depends(get_db)],
    resolution_user_id: Annotated[int, Depends(get_resolution_user_id)],
    body: ResolveDeviceRebindIn,
    response: Response,
):
    token_pair = AuthService(db).resolve_device_rebind(
        user_id=resolution_user_id,
        target_device_id=str(body.target_device_id),
        new_fingerprint=body.new_fingerprint,
    )

    response.set_cookie(
        key="refresh_token",
        value=token_pair["refresh_token"],
        httponly=True,
        samesite="lax",
        secure=False,
        path="/auth",
    )

    return token_pair


@auth_route.post(
    "/device/resolve/create",
    summary="Creates/binds new device fingerprint and returns auth tokens.",
    response_model=Token,
)
def resolve_device_create(
    *,
    db: Annotated[Session, Depends(get_db)],
    resolution_user_id: Annotated[int, Depends(get_resolution_user_id)],
    body: ResolveDeviceCreateIn,
    response: Response,
):
    token_pair = AuthService(db).resolve_device_create(
        user_id=resolution_user_id,
        new_fingerprint=body.new_fingerprint,
        display_name=body.display_name,
    )

    response.set_cookie(
        key="refresh_token",
        value=token_pair["refresh_token"],
        httponly=True,
        samesite="lax",
        secure=False,
        path="/auth",
    )

    return token_pair


@auth_route.post(
    "/device/resolve/cancel",
    summary="Cancels device-resolution flow. Optionally removes user created during signup.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_device_resolution(
    *,
    db: Annotated[Session, Depends(get_db)],
    resolution_user_id: Annotated[int, Depends(get_resolution_user_id)],
    body: ResolveDeviceCancelIn,
):
    AuthService(db).cancel_device_resolution(
        user_id=resolution_user_id,
        remove_user=body.remove_user,
    )


