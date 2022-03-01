from database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship


class CounterAgent(Base):
    __tablename__ = 'counter_agent'
    id = Column(Integer, unique=True,autoincrement=True)
    type = Column(String)
    name = Column(String, primary_key=True,unique=True)
    address = Column(String)

    invoice = relationship('Invoice')
    employee = relationship('Employee')
    item = relationship('Items', secondary='reserve', back_populates='counter_agent')
    employee_id = relationship('Employee', secondary='accesstable', back_populates='counter_agent')