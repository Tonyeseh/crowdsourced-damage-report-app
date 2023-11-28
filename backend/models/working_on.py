#!/usr/bin/python3
"""holds working_on class"""

from datetime import datetime
import enum
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, Float, ForeignKey, String, DateTime

class WorkState(enum.Enum):
    in_progress = "in_progress"
    done = "done"
    failed = "failed"

work_state = ("In Progress", "Done", "Failed")


class WorkingOn(BaseModel, Base):
    """Representation of WorkingOn"""
    __tablename__ = "working_on"
    damage_id = Column(String(60), ForeignKey('damages.id'), nullable=False)
    worker_id = Column(String(60), ForeignKey('workers.id'), nullable=True)
    status = Column(Enum(*work_state), default="In Progress")
    date_assigned = Column(DateTime, default=datetime.utcnow)
    date_completed = Column(DateTime, nullable=True)
    proposed_cost = Column(Float(2), default=0.00)
    actual_cost = Column(Float(2), default=0.0)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
