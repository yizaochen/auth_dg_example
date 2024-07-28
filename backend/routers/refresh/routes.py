from datetime import timedelta

from fastapi import APIRouter, Request, HTTPException, Depends
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from routers.users.models import Users
from routers.auth.schemas import TokenResponse
from core.database import get_db
from core.security import create_access_token, get_decode_jwt


router = APIRouter(
    prefix="/refresh",
    tags=["refresh"],
)


@router.get("/", response_model=TokenResponse)
def handle_refresh_token(request: Request, db: Session = Depends(get_db)):
    cookies = request.cookies
    refresh_token = cookies.get("jwt")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    found_user = db.query(Users).filter(Users.refreshToken == refresh_token).first()
    if not found_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        decoded_jwt = get_decode_jwt(refresh_token, "refresh")
        if found_user.username != decoded_jwt.get("sub"):
            raise HTTPException(status_code=403, detail="Forbidden")

        roles = found_user.roles.split(",")
        roles = [int(role) for role in roles]
        access_token = create_access_token(
            data={"sub": found_user.username, "roles": roles},
            expires_delta=timedelta(seconds=30),
        )

        return TokenResponse(accessToken=access_token, roles=roles)
    except JWTError:
        raise HTTPException(status_code=403, detail="Forbidden")
