#!/usr/bin/python3
"""holds Facility class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Facility(BaseModel):
    """Representation of a Facility"""
    __tablename__ = "facilities"
    name: str = Column(String(128), nullable=False)
    infrastructure_id: str = Column(String(60), ForeignKey('infrastructures.id'), nullable=False)
    description: str = Column(String(1024), nullable=False)
    # category_id: str = Column(String(60), ForeignKey('categories.id'), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """initiliases a facility"""
        super().__init__(*args, **kwargs)
