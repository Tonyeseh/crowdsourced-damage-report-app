#!/usr/bin/python3
"""holds User model"""

from hashlib import md5
from typing import Any
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class BaseUser(BaseModel):
    """Representation of a BaseUser"""
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    # account_type = ""

    def __init__(self, *args, **kwargs) -> None:
        """initialises user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, __name: str, __value: Any) -> None:
        """sets a password with md5 encryption"""
        if __name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(__name, __value)
