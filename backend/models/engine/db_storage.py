#!/bin/python3
"""db_storage module"""

import models
from models.base_model import Base
from models.damage import Damages
from models.damage_category import DamageCategory
from models.facility import Facility
from models.infrastructure import Infrastructure
from models.location import Location
from models.user import User
from models.working_on import WorkingOn
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {"Damages": Damages, "DamageCategory": DamageCategory, "Facility": Facility, "Infrastructure": Infrastructure, "Location": Location, "User": User, "WorkingOn": WorkingOn}

class DBStorage:
    """DB Storage class"""
    __session = None
    __engine = None
    __db_string = ""
    __objects = {}

    def __init__(self) -> None:
        """Instantiate a DBStorage object"""
        DB_USER = None
        DB_PWD = None
        DB_HOST = None
        DB_NAME = None
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_NAME))
        if False:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns all objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.objects.items():
                if cls in key:
                    new_dict[key] = value
            return new_dict
        
        return self.__objects
    
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes in current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current db session obj"""
        if obj is not None:
            self.__session.delete(obj)
    
    def reload(self):
        """loads all objects stored in db"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """calls remove() method of the Session attribute"""
        self.__session.remove()
        
    def get(self, cls, id):
        """Returns an object based on the class name and its ID or None if not found"""
        if cls not in classes.values():
            return None
        
        all_cls_obj = models.storage.all(cls)
        for value in all_cls_obj.value():
            if value.id == id:
                return value
        
        return None
    
    def count(self, cls=None):
        """count number of objects in storage"""
        all_class = classes.values()
        if not cls:
            count = len(models.storage.all().values())
        else:
            count = len(models.storage.all(cls).values())

        return count
