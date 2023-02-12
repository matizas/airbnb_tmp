#!/usr/bin/python3
'''
This Module creates the State Class
'''

from .base_model import BaseModel


class State(BaseModel):
    '''
    A class to represent the State model
    from which state instances will be created.

    ...
    Public Attributes
    ----------------
    name : str - State name
    '''
    name = ""
