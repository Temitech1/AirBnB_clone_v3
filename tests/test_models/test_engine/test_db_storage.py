#!/usr/bin/python3
"""
Contains the DBStorage class
"""

from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB')))
        if os.getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects of a given class"""
        new_dict = {}
        for cls_name in classes.values():
            if not cls or cls == cls_name:
                objs = self.__session.query(cls_name).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Adds new object to the database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from database if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get(self, cls, id):
        """Retrieve one object based on class and id"""
        if cls and id:
            key = f"{cls.__name__}.{id}"
            return self.__session.query(cls).get(id)
        return None

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class"""
        if cls:
            return self.__session.query(cls).count()
        return sum(self.__session.query(cls).count() for cls in classes.values())
