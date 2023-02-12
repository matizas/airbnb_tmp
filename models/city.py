#!/usr/bin/python3
'''
This Module creates the City Class
'''

from .base_model import BaseModel


class City(BaseModel):
    '''
    A class to represent the City model
    from which city instances will be created.

    ...
    Public Attributes
    ----------------
    state_id : str - The State id
    name : str - City name
    '''
    state_id = ""
    name = ""
