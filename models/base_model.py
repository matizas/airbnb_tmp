#!/usr/bin/python3
'''
This Module creates the BaseModel Class as a template
for other models created
'''

from uuid import uuid4
from datetime import datetime
import models as m


class BaseModel:
    '''
    A class to represent the base model.

    ...
    Attributes
    ----------
    id : str - uuid(uuid4)
    created_at : datetime - current datetime
    when a new instance is created
    updated_at : datetime - current datetime
    when a new instance is created and it
    will be updated every time an instance of the base model changes
    Public Instance Methods
    -------
    save():
        updates the public instance attribute
        updated_at with the current datetime
    to_dict():
        returns a dictionary containing all keys/
        values of __dict__ of the instance
    Public Class Methods
    --------------------
    all() :
        get all records of a Model's class
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructs all the neccesary attributes for the BaseModel
        Object
        Parameters
        ----------
        args : not used
        kwargs : dictionary of keyword arguments
        '''
        if len(kwargs):
            for key in kwargs:
                value = kwargs[key]
                if key != "__class__":
                    self.__setattr__(key, value)
                if key in ["created_at", "updated_at"]:
                    self.__setattr__(key, datetime.fromisoformat(value))
        else:
            self.id = uuid4().__str__()
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            m.storage.new(self)

    def __str__(self):
        " Returns the string representation of
        an instance of the Base Model class "
        return("[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        '''
        Updates the public instance attribute
        updated_at with the current datetime
        and persists instance to file storage
        '''
        self.updated_at = datetime.now()
        m.storage.save()

    def to_dict(self):
        " returns a dictionary containing all keys/
        values of __dict__ of the instance "
        dict_copy = {**self.__dict__}
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy["created_at"] = datetime.isoformat(self.created_at)
        dict_copy["updated_at"] = datetime.isoformat(self.updated_at)
        return dict_copy

    @classmethod
    def all(cls):
        " Returns a list of all instances of selected class model "
        all = m.storage.all()
        data_list = []
        cls_name = cls.__name__

        for cls_name_id_key in all:

            if cls_name_id_key.startswith(cls_name):
                data_list.append(all[cls_name_id_key].__str__())

        return data_list

    @classmethod
    def count(cls):
        " Returns number of instances of selected class model "
        return len(cls.all())

    @classmethod
    def show(cls, id):
        '''
        Returns a single instance retrived by id of selected class model
        Returns
        -------
            int(1) : Error(** instance id missing **)
            int(2) : Error(** no instance found **)
            object : Success (selected instance)
        '''

        if not id:
            return (1)

        cls_name_id_key = cls.__name__+"."+id
        all = m.storage.all()

        if cls_name_id_key in all:
            return all[cls_name_id_key]
        else:
            return(2)

    @classmethod
    def destroy(cls, id):
        '''
        Destroys a single instance retrived from the selected class model by id
        Returns
        -------
            int(1) : Error(** instance id missing **)
            int(2) : Error(** no instance found **)
            None : Success
        '''

        if not id:
            return (1)

        key_to_del = cls.__name__+"."+id
        all = m.storage.all()

        if key_to_del in all:
            all.pop(key_to_del)
            m.storage.save()
        else:
            return(2)

    @classmethod
    def update(cls, id, attr_name, attr_value):
        cls_name_id_key = cls.__name__+"."+id
        all = m.storage.all()
        selected_record = all[cls_name_id_key]
        setattr(selected_record, attr_name, eval(attr_value))
        m.storage.save()
