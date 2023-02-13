#!/usr/bin/python3
'''
This Module creates the FileStorage Class which handles instance storage
and retrivals
'''

import json
import os
import models.base_model as bm


class FileStorage:
    '''
        A class which serializes instances to JSON and persists
        to the file storage (file.json) as well as deserialize
        json from file storage
        Private Attributes
        ------------------
        __file_path : str - path to the JSON file (file.json)
        __objects : dict - stores all objects by <class name>.id
        Public Methods
        -----------------
        all() : returns the dictionary __objects
        new(obj) : sets in __objects the obj with key <obj class name>.id
        save() : serializes __objects to the JSON file (path: __file_path)
        reload(): deserializes the JSON file
        to __objects (only if the JSON file (__file_path)
        exists ; otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised)
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        "returns the dictionary __objects"
        return FileStorage.__objects

    def new(self, obj):
        '''
        sets in __objects the obj with key <obj class name>.id
        Paramater
        ---------
        obj : model.instance - an instance of a model
        '''
        if not obj:
            raise Exception("obj argument must be a valid instance")

        if not isinstance(obj, bm.BaseModel):
            raise Exception("Invalid Instance")

        cls_name_id_key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[cls_name_id_key] = obj

    def save(self):
        " serializes __objects to the JSON file (path: __file_path) "

        if len(FileStorage.__objects):
            with open(FileStorage.__file_path, "w") as fp:
                dict_data = {}

                for cls_name_id_key in FileStorage.__objects:
                    fl = FileStorage.__objects[cls_name_id_key].to_dict()
                    record_in_dict = fl
                    dict_data[cls_name_id_key] = record_in_dict

                json.dump(dict_data, fp, indent=4)

    def reload(self):
        '''
        deserializes the JSON file to __objects
        (only if the JSON file (__file_path)
        exists ; otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised)
        '''
        from ..base_model import BaseModel
        from ..user import User
        from ..amenity import Amenity
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..state import State

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as fp:
                dict_data = json.load(fp)
                FileStorage.__objects = {}

                for cls_name_id_key in dict_data:
                    record = dict_data[cls_name_id_key]
                    sout = locals()[record["__class__"]](**record)
                    FileStorage.__objects[cls_name_id_key] = sout
