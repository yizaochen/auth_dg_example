from typing import List
from pydantic import BaseModel


class TokenResponse(BaseModel):
    accessToken: str
    roles: List[int]


class LoginRequest(BaseModel):
    user: str
    pwd: str
