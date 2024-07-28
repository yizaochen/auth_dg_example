from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from routers.users.models import Users
from routers.users.schemas import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    # print(request)
    users = db.query(Users).all()
    return [{"username": user.username} for user in users]
