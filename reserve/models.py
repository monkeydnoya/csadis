from ast import For
from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class Reserve(Base):
    __tablename__ = 'reserve'
    id = Column(Integer,unique=True,autoincrement=True,primary_key=True)
    item = Column(Integer, ForeignKey('items.id', ondelete='cascade', onupdate='cascade'))
    warehouse = Column(Integer, ForeignKey('warehouse.id', ondelete='cascade', onupdate='cascade'))
    count = Column(Integer)

