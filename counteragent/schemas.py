from pydantic import BaseModel


class CounterAgent(BaseModel):
    id:int
    type:str
    name:str
    address:str

    class Config:
        orm_mode = True