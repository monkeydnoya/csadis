from pydantic import BaseModel


class WareHouse(BaseModel):
    id:int
    number:int
    address:str

    class Config:
        orm_mode = True