from ast import For
from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class Reserve(Base):
    __tablename__ = 'reserve'
    id = Column(Integer,unique=True,autoincrement=True)
    item = Column(Integer, ForeignKey('items.id', ondelete='cascade', onupdate='cascade'),primary_key=True)
    warehouse = Column(Integer, ForeignKey('counter_agent.id', ondelete='cascade', onupdate='cascade'), primary_key=True)
    count = Column(Integer)

