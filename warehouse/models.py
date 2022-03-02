from database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship


class WareHouse(Base):
    __tablename__ = 'warehouse'
    id = Column(Integer, primary_key=True,unique=True,autoincrement=True)
    number = Column(Integer, unique=True)
    address = Column(String, unique=True)

    invoice = relationship('Invoice')
    item = relationship('Items', secondary='reserve', back_populates='wh')