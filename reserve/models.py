from ast import For
from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class Reserve(Base):
    __tablename__ = 'reserve'
    item = Column(Integer, ForeignKey('items.id'),primary_key=True, onupdate=CASCADE)
    warehouse = Column(Integer, ForeignKey('counter_agent.id'), primary_key=True, onupdate=CASCADE)
    count = Column(Integer)

