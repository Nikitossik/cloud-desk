from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..models import User
from ..schemas import UserBase, UserIn

user_route = APIRouter(prefix="/user", tags=["users"])


@user_route.get("/", response_model=list[UserBase])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@user_route.get("/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).where(User.id == user_id).scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@user_route.post("/", status_code=201, response_model=UserBase)
def add_user(user: UserIn, db: Session = Depends(get_db)):
    user_data = user.model_dump()

    # mocking password hashing
    password_hash = "hashed:" + user_data["password"]

    new_user: User = User(**user_data, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return user
