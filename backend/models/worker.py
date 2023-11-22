#!/usr/bin/python3
""" worker class """

import enum
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.base_user import BaseUser


class Worker(BaseUser, Base):
    """ defines the worker class """
    __tablename__ = "workers"
    # occupation = Column(String(60), ForeignKey("occupations.id"))
    jobs = relationship("WorkingOn", backref="workers")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    
