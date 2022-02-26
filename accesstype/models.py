class AccessType(Base):
    __tablename__ = 'access_type'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    description = Column(String)