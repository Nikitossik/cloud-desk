from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..models import User
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from ..schemas.user import UserIn, UserUpdate, UserOut
from ..schemas.device import DeviceOut
from ..services.user import UserService
from pathlib import Path

user_route = APIRouter(prefix="/user", tags=["user"])

@user_route.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(
    db: Annotated[Session, Depends(get_db)],
):
    db.query(User).delete()
    db.commit()
    return None

@user_route.get(
    "/me",
    summary="Retrieves the currently authenticated user's profile.",
    response_model=UserOut,
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@user_route.get(
    "/me/devices",
    summary="Retrieves the currently authenticated user's devices.",
    response_model=list[DeviceOut],
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user.devices



@user_route.patch("/me", summary="Updates the currently authenticated user's profile.", response_model=UserOut)
async def update_me(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return UserService(db).update(current_user.id, user_update)