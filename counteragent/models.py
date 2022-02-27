from database import Base
from sqlalchemy import Column,Integer,String


class CounterAgent(Base):
    __tablename__ = 'counter_agent'
    id = Column(Integer, unique=True)
    type = Column(String)
    name = Column(String, primary_key=True,unique=True)
    address = Column(String)