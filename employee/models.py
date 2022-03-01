from sre_constants import OP_UNICODE_IGNORE
from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer,primary_key=True,unique=True,autoincrement=True)
    name = Column(String(255), nullable=False,unique=True)
    warehouse = Column(Integer, ForeignKey('counter_agent.id', onupdate='cascade', ondelete='cascade'),unique=True)
    iin = Column(Integer)
    post = Column(String)

    def __str__(self):
        return f'<Employee name: {self.name}, Post: {self.post}>'