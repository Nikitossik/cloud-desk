from fastapi import APIRouter, Depends, status
from typing import Annotated
from pathlib import Path
from sqlalchemy.orm import Session

from ..models import User, Device
from ..dependencies import get_db, get_current_user, get_current_device
from ..schemas.user import UserIn, UserUpdate, UserOut
from ..schemas.sidebar import UserSidebarOut
from ..services.user import UserService

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


@user_route.patch("/me", summary="Updates the currently authenticated user's profile.", response_model=UserOut)
async def update_me(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return UserService(db).update(current_user.id, user_update)

@user_route.get("/me/sidebar", summary="Retrieves the data needed to populate the user's sidebar.", response_model=UserSidebarOut)
async def get_sidebar_data(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    current_device: Annotated[Device, Depends(get_current_device)],
):
    return UserService(db).get_sidebar_data(current_user, current_device)