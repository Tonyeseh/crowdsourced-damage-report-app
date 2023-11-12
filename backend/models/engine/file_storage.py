#!/usr/bin/python3
"""file_storage module"""


class FileStorage:
    """File Storage for db"""
    __file_path = "db.json"
    __objects = {}

    def all(self, cls=None):
        """returns all objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                pass


    def reload(self):
        """loads all objects stored in file.json"""
        pass


    def save(self):
        """saves the objects to the file.json"""
        pass
