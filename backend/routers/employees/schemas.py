from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    firstname: str
    lastname: str
