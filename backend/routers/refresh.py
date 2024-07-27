import sys

sys.path.append("..")
from datetime import timedelta

from fastapi import APIRouter, Request, HTTPException, Depends
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from models import Users
from database import get_db
from .auth import REFRESH_SECRET_KEY, ALGORITHM, create_access_token, Token


router = APIRouter(
    prefix="/refresh",
    tags=["refresh"],
)


@router.get("/", response_model=Token)
def handle_refresh_token(request: Request, db: Session = Depends(get_db)):
    cookies = request.cookies
    refresh_token = cookies.get("jwt")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    found_user = db.query(Users).filter(Users.refreshToken == refresh_token).first()
    if not found_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        decoded_jwt = jwt.decode(
            refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if found_user.username != decoded_jwt.get("sub"):
            raise HTTPException(status_code=403, detail="Forbidden")

        roles = found_user.roles.split(",")
        roles = [int(role) for role in roles]
        access_token_expires = timedelta(seconds=30)
        access_token = create_access_token(
            data={"sub": found_user.username, "roles": roles},
            expires_delta=access_token_expires,
        )

        return Token(accessToken=access_token, roles=roles)
    except JWTError:
        raise HTTPException(status_code=403, detail="Forbidden")
