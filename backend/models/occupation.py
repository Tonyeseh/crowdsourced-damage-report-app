#!/usr/bin/python3
""" occupation class """

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String


class Occupation(BaseModel, Base):
    """ worker occupation class """
    __tablename__ = "occupations"
    name = Column(String(60), nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
