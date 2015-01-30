import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Catador(Base):
    __tablename__ = 'catador'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    phone = Column(String(20), unique=False)
    address = Column(String(120), unique=False)
    latitude = Column(Float(), unique=False)
    longitude = Column(Float(), unique=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Catador %r>' % (self.name)

    def to_JSON(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            }, indent=4)
