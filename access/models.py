from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer
# from sqlalchemy.orm import relationship
from employee.models import *


class Access(Base):
    __tablename__ = 'accesstable' # mb foreign key
    warehouse = Column(Integer, ForeignKey('counter_agent.id', onupdate='cascade', ondelete='cascade'),primary_key=True)
    access_type = Column(Integer, ForeignKey('access_type.id'))
    employee = Column(String, ForeignKey('employee.name', onupdate='cascade', ondelete='cascade'))
