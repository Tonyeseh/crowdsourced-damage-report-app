#!/usr/bin/python3
"""holds User model"""

from hashlib import md5
from typing import Any
import models
from models.base_model import BaseModel
from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash


class BaseUser(BaseModel):
    """Representation of a BaseUser"""
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    # account_type = ""

    def __init__(self, *args, **kwargs) -> None:
        """initialises user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, __name: str, __value: Any) -> None:
        """sets a password with md5 encryption"""
        if __name == "password":
            __value = generate_password_hash(__value)
        super().__setattr__(__name, __value)


    def check_password(self, password):
        """validates the user password"""
        hashed_password = md5(password)
        if hashed_password == self.password:
            return True
        
        return False

    @classmethod
    def get_by_email(cls, email):
        """ get user by email """
        users = models.storage.all(cls)
        for user in users.values():
            if user.email == email:
                return user
            
        return None
    
    @classmethod
    def login(cls, email, password):
        """ validates the user to ligin them in"""
        user = cls.get_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user
