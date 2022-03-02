from pydantic import BaseModel, Field


class Employee(BaseModel):
    id:int
    name:str
    email: str
    password: str
    # warehouse:int
    iin:int 
    post:int = Field(...,ge = 0, le = 2)

     
    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = '0fb3ad8cd86e8605f4e04b20baed2b30'
    

class LoginModel(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True