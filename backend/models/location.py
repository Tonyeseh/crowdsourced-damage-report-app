#!/usr/bin/python3
"""holds location City"""
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Location(BaseModel):
    """Representation of a Location"""
    __tablename__ = "locations"
    name: str = Column(String(128), nullable=False)
    infrastructures = relationship("Infrastructure", backref="location", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
