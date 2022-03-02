from email.quoprimime import unquote
from sre_constants import OP_UNICODE_IGNORE
from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer,primary_key=True,unique=True,autoincrement=True)
    name = Column(String, nullable=False,unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    iin = Column(Integer, unique=True)
    post = Column(Integer, ForeignKey('access_type.id', ondelete='cascade', onupdate='cascade')) #Children for AccessType

    invoice = relationship('Invoice') # Parent in O2M

    def __str__(self):
        return f'<Employee name: {self.name}, Post: {self.post}>'