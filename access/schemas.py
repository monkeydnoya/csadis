from pydantic import BaseModel


class Access(BaseModel):
    employee:int
    warehouse:str
    access_type:int

    class Config:
        orm_mode = True
    