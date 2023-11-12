#!/usr/bin/python3
"""holds infrastructure class"""
from models.base_model import BaseModel


class Infrastructure(BaseModel):
    """Representation of an Infrastructure"""
    name: str = ""
    location_id = ""
    description: str = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
