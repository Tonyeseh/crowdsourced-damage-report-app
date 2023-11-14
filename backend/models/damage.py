#!/usr/bin/python3
"""damages class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Enum, Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Damages(BaseModel, Base):
    """Representation of Damages"""
    __tablename__ = "damages"
    reporter_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    facility_id = Column(String(60), ForeignKey('facilities.id'), nullable=False)
    state = Column(String(60), default="Not Assigned")  # completed|assigned|not assigned|awaiting verification
    description = Column(String(1024), nullable=False)
    category_id = Column(String(60), ForeignKey('damagescategories.id'), nullable=False)
    priority = Column(String(60), default="Not serious")
    images = relationship("Images", backref="damage", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
