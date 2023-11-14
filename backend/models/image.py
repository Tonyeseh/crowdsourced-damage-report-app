#!/usr/bin/python3
"""image model"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String


class Image(BaseModel, Base):
    """Representation of an Image"""
    __tablename__ = "images"
    name = Column(String(128), nullable=False)
    damage_id = Column(String(60), ForeignKey('damages.id'), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initialises Image object"""
        super().__init__(*args, **kwargs)
