from typing import List
import os

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
import bcrypt

from database import get_db
from models import Users

load_dotenv()
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET")
ALGORITHM = "HS256"


class Token(BaseModel):
    accessToken: str
    roles: List[int]


class LoginRequest(BaseModel):
    user: str
    pwd: str


# Define the HTTP Bearer scheme for token authentication
security = HTTPBearer()


def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Decode the JWT token using the secret key from environment variables
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded["sub"]
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/", response_model=Token)
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
    access_token_expires = timedelta(seconds=30)
    access_token = create_access_token(
        data={"sub": found_user.username, "roles": roles},
        expires_delta=access_token_expires,
    )
    roles = [int(role) for role in roles]

    refresh_token_expires = timedelta(days=1)
    refresh_token = create_refresh_token(
        data={"sub": found_user.username}, expires_delta=refresh_token_expires
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

    return Token(accessToken=access_token, roles=roles)
