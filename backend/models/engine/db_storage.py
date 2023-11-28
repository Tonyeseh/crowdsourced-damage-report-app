#!/bin/python3
"""db_storage module"""

import models
from models.base_model import Base
from models.admin_user import AdminUser
from models.damage import Damage
from models.damage_category import DamageCategory
from models.facility import Facility
from models.infrastructure import Infrastructure
from models.image import Image
from models.location import Location
from models.student_user import StudentUser
from models.working_on import WorkingOn
from models.worker import Worker
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {"AdminUser": AdminUser, "Damages": Damage, "DamageCategory": DamageCategory, "Facility": Facility, "Image": Image, "Infrastructure": Infrastructure, "Location": Location, "StudentUser": StudentUser, "WorkingOn": WorkingOn, "Worker": Worker}

class DBStorage:
    """DB Storage class"""
    __session = None
    __engine = None

    def __init__(self) -> None:
        """Instantiate a DBStorage object"""
        DB_USER = getenv('DB_USER')
        DB_PWD = getenv('DB_PWD')
        DB_HOST = 'localhost'
        DB_NAME = getenv('DB_NAME')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_NAME))
        if False:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
    
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
        for value in all_cls_obj.values():
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
