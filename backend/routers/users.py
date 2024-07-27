import sys

sys.path.append("..")

from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


from database import get_db
from models import Users


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


class UserResponse(BaseModel):
    username: str


@router.get("/", response_model=List[UserResponse])
def get_all_users(request: Request, db: Session = Depends(get_db)):
    print(request)
    users = db.query(Users).all()
    return [{"username": user.username} for user in users]
