#!/usr/bin/python3
""" damage module """

from models.base_model import BaseModel, Base
from sqlalchemy import Enum, Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Damage(BaseModel, Base):
    """Representation of Damages"""
    __tablename__ = "damages"
    reporter_id = Column(String(60), ForeignKey('student_users.id'), nullable=False)
    facility_id = Column(String(60), ForeignKey('facilities.id'), nullable=False)
    state = Column(String(60), default="Not Assigned")  # completed|assigned|not assigned|awaiting verification
    description = Column(String(1024), nullable=False)
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    priority = Column(String(60), default="Not serious")
    working_on = relationship("WorkingOn", backref="damages", cascade="all, delete, delete-orphan")
    # images = relationship("Image", backref="damages", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
