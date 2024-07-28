import os

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import timedelta
import bcrypt

from core.database import get_db
from core.security import create_access_token, create_refresh_token
from routers.users.models import Users
from routers.auth.schemas import TokenResponse, LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/", response_model=TokenResponse)
async def login(
    request: LoginRequest, response: Response, db: Session = Depends(get_db)
):
    user = request.user
    pwd = request.pwd
    if not user or not pwd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required.",
        )

    found_user = db.query(Users).filter(Users.username == user).first()
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    if not bcrypt.checkpw(pwd.encode("utf-8"), found_user.password.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    roles = found_user.roles.split(",")
    access_token = create_access_token(
        data={"sub": found_user.username, "roles": roles},
        expires_delta=timedelta(seconds=30),
    )
    roles = [int(role) for role in roles]

    refresh_token = create_refresh_token(
        data={"sub": found_user.username}, expires_delta=timedelta(days=1)
    )

    found_user.refreshToken = refresh_token
    db.add(found_user)
    db.commit()

    response.set_cookie(
        key="jwt",
        value=refresh_token,
        httponly=True,
        samesite="None",
        secure=True,
        max_age=24 * 60 * 60 * 1000,
    )

    return TokenResponse(accessToken=access_token, roles=roles)
