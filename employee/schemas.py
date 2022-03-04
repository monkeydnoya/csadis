from pydantic import BaseModel, Field


class Employee(BaseModel):
    id:int
    name:str
    email: str
    password: str
    # warehouse:int
    iin:int 
    post:int = Field(...,ge = 0, le = 3)

     
    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'
    

class LoginModel(BaseModel):
    email: str
    password: str

    # class Config:
    #     orm_mode = True