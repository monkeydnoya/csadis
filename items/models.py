from sqlalchemy import Column, Integer, ForeignKey, String, Float
from database import Base

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, unique=True)
    type = Column(String)
    price = Column(Float)
    currency = Column(String)

