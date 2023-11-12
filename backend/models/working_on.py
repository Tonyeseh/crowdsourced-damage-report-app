#!/usr/bin/python3
"""holds working_on class"""
from models.base_model import BaseModel


class WorkingOn(BaseModel):
    """Representation of WorkingOn"""
    damage_id: str = ""
    worker_id: str = ""
    status: str = ""
    date_assigned = ""
    date_completed = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
