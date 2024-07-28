from typing import List
from fastapi import APIRouter, Depends

from core.security import verify_jwt


router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


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
