from ast import For
from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class Reserve(Base):
    __tablename__ = 'reserve'
    id = Column(Integer,unique=True,autoincrement=True)
    item = Column(Integer, ForeignKey('items.id'),primary_key=True, onupdate='cascade')
    warehouse = Column(Integer, ForeignKey('counter_agent.id'), primary_key=True, onupdate='cascade')
    count = Column(Integer)

