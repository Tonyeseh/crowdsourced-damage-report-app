#!/usr/bin/python3
"""damages class"""
from models.base_model import BaseModel


class Damages(BaseModel):
    """Representation of Damages"""
    reporter_id: str = ""
    facility_id: str = ""
    state: str = ""  # completed|assigned|not assigned|awaiting verification
    description: str = ""
    category: str = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
