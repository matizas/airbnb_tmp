#!/usr/bin/python3
'''
This Module creates the Review Class
'''

from .base_model import BaseModel


class Review(BaseModel):
    '''
    A class to represent the Review model
    from which review instances will be created.

    ...
    Public Attributes
    ----------------
    place_id : str - The Place id
    user_id : str - The User id
    text : str
    '''
    place_id = ""
    user_id = ""
    text = ""
