from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer


class Access(Base):
    __tablename__ = 'accesstable' # mb foreign key
    warehouse = Column(String, ForeignKey('employee.warehouse'), primary_key=True)
    access_type = Column(Integer, ForeignKey('access_type.id'))
    employee = Column(Integer, ForeignKey('employee.id'))
