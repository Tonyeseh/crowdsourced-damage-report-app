#!/usr/bin/python3
"""holds Facility class"""
from models.base_model import BaseModel


class Facility(BaseModel):
    """Representation of a Facility"""
    name: str = ""
    building_id: str = ""
    description: str = ""
    category: str

    def __init__(self, *args, **kwargs) -> None:
        """initiliases a facility"""
        super().__init__(*args, **kwargs)
