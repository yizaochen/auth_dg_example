from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .auth import verify_jwt


router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


class Employee(BaseModel):
    id: int
    firstname: str
    lastname: str


@router.get("/", response_model=List[Employee])
def get_all_employees(username: str = Depends(verify_jwt)):
    print(username)
    data = [
        {"id": 1, "firstname": "Dave", "lastname": "Gray"},
        {"id": 2, "firstname": "John", "lastname": "Smith"},
    ]
    response_data = []
    for employee in data:
        response_data.append(Employee(**employee))
    return response_data
