import sys
sys.path.append("..")

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt

from database import get_db
from models import Users

router = APIRouter(
    prefix="/register",
    tags=["register"],
)


class NewUserRequest(BaseModel):
    user: str
    pwd: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def handle_new_user(new_user: NewUserRequest, db: Session = Depends(get_db)):
    user = new_user.user
    pwd = new_user.pwd

    if not user or not pwd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required.",
        )

    # Check for duplicate usernames in the db
    duplicate = db.query(Users).filter(Users.username == user).first()
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists."
        )

    try:
        # Encrypt the password
        hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        # Store the new user
        new_user_data = Users(username=user, password=hashed_pwd)

        # new_user_data = {
        #     "username": user,
        #     "roles": {"User": 2001},
        #     "password": hashed_pwd,
        # }
        # usersDB["users"].append(new_user_data)
        # save_users(usersDB["users"])

        return JSONResponse(content={"success": f"New user {user} created!"})

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
