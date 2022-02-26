class AccessType(BaseModel):
    id:int
    type:str
    description:str

    class Config:
        orm_mode = True