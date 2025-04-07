from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse

from ..database import get_db

from ..schemas import UserIn, UserBase, UserCredentials, UserInDB
from ..models import User, Session as UserSession
from ..hasher import Hasher

from sqlalchemy.orm import Session

from ..dependencies import get_current_user

auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(*, db: Session = Depends(get_db), user: UserIn):
    user_data = user.model_dump()
    found_user = db.query(User).filter(User.email == user_data["email"]).first()

    if found_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    new_user = User(
        **user_data, password_hash=Hasher.get_password_hash(user_data["password"])
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@auth_route.get("/login")
def get_login_user():
    return {"message": "Login page"}


@auth_route.post("/login")
def login_user(
    *,
    db: Session = Depends(get_db),
    user_credentials: UserCredentials,
    response: Response,
):
    user_data = user_credentials.model_dump()
    found_user = db.query(User).filter(User.email == user_data["email"]).first()

    if not found_user or not Hasher.verify_password(
        user_data["password"], found_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user_session = UserSession(id=Hasher.get_random_uuid(), user_id=found_user.id)
    db.add(user_session)
    db.commit()
    db.refresh(user_session)

    response.set_cookie("session_id", user_session.id)

    return {"message": f"Welcome, {found_user.name} {found_user.surname}"}


@auth_route.get("/check")
def check_user(*, current_user: UserInDB = Depends(get_current_user), request: Request):
    if not current_user:
        redirect_url = request.url_for("login_user")

        return RedirectResponse(redirect_url)

    return current_user


@auth_route.get("/logout")
def logout_user(
    *,
    response: Response,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    db.delete(user)
    db.commit()

    response.delete_cookie("session_id")
    return {"message": f"Bye, {current_user.name} {current_user.surname}"}
