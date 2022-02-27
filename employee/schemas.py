from pydantic import BaseModel


class Employee(BaseModel):
    id:int
    name:str
    # warehouse:int
    iin:int 
    post:str
    # access:int # = Field(..., lt = 5, ge = 0, description='Access level: 0 - 5')

     
    class Config:
        orm_mode = True