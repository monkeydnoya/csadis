from database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True,unique=True,autoincrement=True)
    name = Column(String, unique=True)
    address = Column(String, unique=True)

    invoice = relationship('Invoice')