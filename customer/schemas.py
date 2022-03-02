from pydantic import BaseModel


class Customer(BaseModel):
    id:int
    name:str
    address:str

    class Config:
        orm_mode = True