#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the list of objects of one type of class"""
        if cls:
            return {key: value for key, value in self.__objects.items() if isinstance(value, cls)}
        return self.__objects

    def new(self, obj):
        """Adds new object to __objects dictionary"""
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        """Saves __objects to the JSON file"""
        json_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Loads storage dictionary from the JSON file"""
        try:
            with open(self.__file_path, 'r') as f:
                json_objects = json.load(f)
                for key, value in json_objects.items():
                    cls_name = value["__class__"]
                    self.__objects[key] = classes[cls_name](**value)
        except FileNotFoundError:
            pass

    def get(self, cls, id):
        """Retrieve one object based on class and id"""
        if cls and id:
            key = f"{cls.__name__}.{id}"
            return self.__objects.get(key)
        return None

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class"""
        return len(self.all(cls))
