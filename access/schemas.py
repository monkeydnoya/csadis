from pydantic import BaseModel


class Access(BaseModel):
    warehouse:str
    access_type:int
    employee:str

    class Config:
        orm_mode = True
    