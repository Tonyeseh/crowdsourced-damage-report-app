#!/usr/bin/python3
"""holds location City"""
from models.base_model import BaseModel


class Location(BaseModel):
    """Representation of a Location"""
    name: str = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
