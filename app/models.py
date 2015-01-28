from sqlalchemy import Column, Integer, String, Float
from database import Base

class Catador(Base):
    __tablename__ = 'catador'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    address = Column(String(120), unique=False)
    latitude = Column(Float(), unique=False)
    longitude = Column(Float(), unique=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Catador %r>' % (self.name)
