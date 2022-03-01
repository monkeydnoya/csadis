from sqlalchemy import Column,String,Integer,DateTime, ForeignKey
from database import Base


class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, unique=True,autoincrement=True)
    number = Column(Integer, unique=True)
    date = Column(DateTime)
    employee = Column(Integer, ForeignKey('employee.id'), onupdate='cascade',primary_key=True)
    status = Column(String)
    type = Column(String)
    description = Column(String)
    item = Column(Integer, ForeignKey('items.id'), onupdate = 'cascade', primary_key=True)
    count = Column(Integer)