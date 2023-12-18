#!/usr/bin/python3
"""holds Damage category class"""

from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class DamageCategory(BaseModel, Base):
    """Representation of DamageCategory"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False, unique=True)
    workers = relationship('Worker', backref="categories")

    def __init__(self, *args, **kwargs) -> None:
        """Initialises DamageCategory"""
        super().__init__(*args, **kwargs)
