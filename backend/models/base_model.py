#!/usr/bin/env python3
"""Base model"""

from datetime import datetime
import models
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from typing import Mapping

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """BaseModel from which all other models inherit"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs) -> None:
        """Initialisation to the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get(
                    'created_at',
                    None) and isinstance(
                    self.created_at,
                    str):
                self.created_at = datetime.strptime(kwargs['created_at', time])
            else:
                self.created_at = datetime.utcnow()

            if kwargs.get(
                    'updated_at',
                    None) and isinstance(
                    self.updated_at,
                    str):
                self.updated_at = datetime.strptime(kwargs['updated_at'], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get('id', None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self) -> str:
        """String representation of the Class"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self, save_fs=None) -> Mapping:
        """returns a dictionary containing all key/values of the instance"""
        new_dict = self.__dict__.copy()
        if not new_dict.get('created_at', None):
            new_dict['created_at'] = new_dict['created_at'].strftime(time)
        if not new_dict.get('updated_at', None):
            new_dict['updated_at'] = new_dict['updated_at'].strftime(time)

        new_dict['__class__'] = self.__class__.__name__
        if new_dict.get('_sa_instance_state', None):
            del new_dict['_sa_instance_state']
        if save_fs is None:
            if new_dict.get('password', None):
                del new_dict['password']
        return new_dict

    def save(self) -> None:
        """updates the update_at with the current time"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
