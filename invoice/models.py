from sqlalchemy import Column,String,Integer,DateTime, ForeignKey
from database import Base


class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, unique=True)
    number = Column(Integer, unique=True)
    date = Column(DateTime)
    employee = Column(Integer, ForeignKey('employee.id'), onupdate=CASCADE)
    status = Column(String)
    type = Column(String)
    description = Column(String)
    item = Column(String, ForeignKey('items.id'), onupdate = CASCADE)
    count = Column(Integer)