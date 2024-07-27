import sys

sys.path.append("..")

from fastapi import APIRouter, Request, Depends, Response, status
from sqlalchemy.orm import Session

from models import Users
from database import get_db


router = APIRouter(
    prefix="/logout",
    tags=["logout"],
)


@router.get("/")
async def handle_logout(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    cookies = request.cookies
    if "jwt" not in cookies:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    refresh_token = cookies["jwt"]

    # Check if refresh token is in database
    found_user = db.query(Users).filter(Users.refreshToken == refresh_token).first()

    if not found_user:
        response.delete_cookie("jwt", httponly=True, samesite="none", secure=True)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Remove refresh token from user and update the database
    found_user.refreshToken = None
    db.add(found_user)
    db.commit()

    response.delete_cookie("jwt", httponly=True, samesite="none", secure=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
