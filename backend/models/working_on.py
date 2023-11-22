#!/usr/bin/python3
"""holds working_on class"""

from datetime import datetime
import enum
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, ForeignKey, String, DateTime

class WorkState(enum.Enum):
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class WorkingOn(BaseModel, Base):
    """Representation of WorkingOn"""
    __tablename__ = "working_on"
    damage_id = Column(String(60), ForeignKey('damages.id'), nullable=False)
    worker_id = Column(String(60), ForeignKey('workers.id'), nullable=True)
    status = Column(Enum(WorkState), default=WorkState.in_progress)
    date_assigned = Column(DateTime, default=datetime.utcnow)
    date_completed = Column(DateTime, nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
