#!/usr/bin/python3
"""holds User model"""

from hashlib import md5
from typing import Any
from models.base_model import BaseModel
from sqlalchemy import Column, String


class BaseUser(BaseModel):
    """Representation of a BaseUser"""
    email = Column(String(128), unique=True, nullable=False)
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
            __value = md5(__value.encode()).hexdigest()
        super().__setattr__(__name, __value)


    def validate_password(self, password):
        """validates the user password"""
        hashed_password = md5(password)
        if hashed_password == self.password:
            return True
        
        return False
