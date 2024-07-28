from pydantic import BaseModel


class NewUserRequest(BaseModel):
    user: str
    pwd: str
    roles: str
