from pydantic import BaseModel


class Reserve(BaseModel):
    id: int
    item: int
    warehouse: int
    count: int


    class Config:
        orm_mode = True


