from pydantic import BaseModel


class Access(BaseModel):
    warehouse:int
    access_type:int
    employee:str

    class Config:
        orm_mode = True
    