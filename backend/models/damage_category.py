#!/usr/bin/python3
"""holds Damage category class"""
from models.base_model import BaseModel


class DamageCategory(BaseModel):
    """Representation of DamageCategory"""
    name: str = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
