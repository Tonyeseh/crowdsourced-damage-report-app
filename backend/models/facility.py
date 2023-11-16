#!/usr/bin/python3
"""holds Facility class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Facility(BaseModel, Base):
    """Representation of a Facility"""
    __tablename__ = "facilities"
    name = Column(String(128), nullable=False)
    infrastructure_id = Column(String(60), ForeignKey('infrastructures.id'), nullable=False)
    description = Column(String(1024), nullable=False)
    damages = relationship("Damage", backref="facilities", cascade="all, delete, delete-orphan")
    # category_id: str = Column(String(60), ForeignKey('categories.id'), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """initiliases a facility"""
        super().__init__(*args, **kwargs)
