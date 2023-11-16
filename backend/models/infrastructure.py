#!/usr/bin/python3
"""holds infrastructure class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Infrastructure(BaseModel, Base):
    """Representation of an Infrastructure"""
    __tablename__ = "infrastructures"
    name: str = Column(String(128), nullable=False)
    location_id = Column(String(60), ForeignKey('locations.id'), nullable=False)
    description: str = Column(String(1024), nullable=False)
    facilities = relationship("Facility", backref="infrastructures", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
