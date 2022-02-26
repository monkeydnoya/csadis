from pydantic import BaseModel, Field


class Employee(BaseModel):
    id:int
    name:str
    warehouse:str
    iin:int 
    post:str
    # access:int # = Field(..., lt = 5, ge = 0, description='Access level: 0 - 5')

     
    class Config:
        orm_mode = True


class Access(BaseModel):
    employee:int
    warehouse:str
    access_type:int

    class Config:
        orm_mode = True
    

class AccessType(BaseModel):
    id:int
    type:str
    description:str

    class Config:
        orm_mode = True


class CounterAgent(BaseModel):
    id:int
    type:str
    name:str
    address:str

    class Config:
        orm_mode = True