from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer,primary_key=True,unique=True)
    name = Column(String(255), nullable=False,unique=True)
    # warehouse = Column(Integer, ForeignKey('counter_agent.id'),unique=True)
    iin = Column(Integer)
    post = Column(String)

    def __str__(self):
        return f'<Employee name: {self.name}, Post: {self.post}>'