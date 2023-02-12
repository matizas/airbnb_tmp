#!/usr/bin/python3
'''
This Module creates the Place Class
'''

from .base_model import BaseModel


class Place(BaseModel):
    '''
    A class to represent the Place model
    from which place instances will be created.

    ...
    Public Attributes
    ----------------
    city_id: str - the City.id
    user_id: str - the User.id
    name: str - Place name
    description: str - Place description
    number_rooms: int
    number_bathrooms: int
    max_guest: int
    price_by_night: int
    latitude: float
    longitude: float
    amenity_ids: list of str - the list of Amenity.id
    '''
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
