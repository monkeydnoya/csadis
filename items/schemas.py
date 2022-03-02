from pydantic import BaseModel


class Items(BaseModel):
    id: int
    name: str
    type: str
    price: int
    currency: str


    class Config:
        orm_mode = True