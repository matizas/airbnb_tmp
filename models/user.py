#!/usr/bin/python3
'''
This Module creates the User Class
'''

from .base_model import BaseModel


class User(BaseModel):
    '''
    A class to represent the User model
    from which user instances will be created.

    ...
    Public Attributes
    ----------------
    email : str
    password : str
    first_name : str
    last_name : str
    '''
    email = ""
    password = ""
    first_name = ""
    last_name = ""
