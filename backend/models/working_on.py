#!/usr/bin/python3
"""holds working_on class"""

from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, DateTime


class WorkingOn(BaseModel, Base):
    """Representation of WorkingOn"""
    __tablename__ = "working_on"
    damage_id: str = Column(String(60), ForeignKey('damages.id'), nullable=False)
    # worker_id: str = Column(String(60), ForeignKey('user.id'), nullable=True)
    status: str = Column(String(128), default="In Progress")
    date_assigned = Column(DateTime, default=datetime.utcnow)
    date_completed = Column(DateTime, nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
