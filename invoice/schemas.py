from pydantic import BaseModel
from datetime import datetime


class Invoice(BaseModel):
    id: int
    number: int
    date: datetime
    employee: int
    status: str
    type: str
    description: str
    item: str
    count: int

    class Config:
        orm_mode = True