#!/usr/bin/python3
'''
This Module creates the Amenity Class
'''

from .base_model import BaseModel


class Amenity(BaseModel):
    '''
    A class to represent the Amenity model
    from which amenity instances will be created.

    ...
    Public Attributes
    ----------------
    name : str - Amenity name
    '''
    name = ""
