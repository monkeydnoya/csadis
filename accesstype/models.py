from database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class AccessType(Base):
    __tablename__ = 'access_type'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    description = Column(String)

    access = relationship('Access', back_populates='accesstype')