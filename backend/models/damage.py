#!/usr/bin/python3
""" damage module """

import enum
from models.base_model import BaseModel, Base
from sqlalchemy import Enum, Column, String, ForeignKey
from sqlalchemy.orm import relationship


class DamageState(enum.Enum):
    """ defines many damage states"""
    completed = "completed"
    assigned = "assigned"
    not_assigned = "not_assigned"
    awaiting_verification = "awaiting_verification"

damage_state = ("Completed",
"Assigned",
"Not Assigned",
"Awaiting Verification",
"Failed",
"Reassigned")

priority_lst = ("Not serious", "Serious", "Very serious")


class Damage(BaseModel, Base):
    """Representation of Damages"""
    __tablename__ = "damages"
    reporter_id = Column(String(60), ForeignKey('student_users.id'), nullable=False)
    facility_id = Column(String(60), ForeignKey('facilities.id'), nullable=False)
    state = Column(Enum(*damage_state), default="Not Assigned")  # completed|assigned|not assigned|awaiting verification| failed
    description = Column(String(1024), nullable=False)
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    priority = Column(Enum(*priority_lst), default="Not serious")
    working_on = relationship("WorkingOn", backref="damages", cascade="all, delete, delete-orphan")
    images = relationship("Image", backref="damages", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
