#!/usr/bin/python3
""" worker class """

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.base_user import BaseUser


class Worker(BaseUser, Base):
    """ defines the worker class """
    __tablename__ = "workers"
    job_type = Column(String(128), ForeignKey('categories.id'))
    jobs = relationship("WorkingOn", backref="workers")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
