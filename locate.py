# -*- coding: utf-8 -*-
import os
import requests


API_KEY = os.environ['GG_MAP']
RADIUS = 1000
URL_GEO = ("https://maps.googleapis.com/maps/"
           "api/geocode/json?address={0}&key={1}")
URL_PLACE = ("https://maps.googleapis.com/maps/api/place/nearbysearch/"
             "json?location={0},{1}&radius={2}&"
             "type={3}&keyword={4}&key={5}")


def get_locations(address, type_, keyword,
                  url_geo=URL_GEO, url_place=URL_PLACE):
    """ Return lists of places of 'type' located nearby 'address'

    :param address:
    :param type:
    :param keyword:
    :rtype generator:
    """
    req = requests.get(url_geo.format(address.replace(' ', '+'), API_KEY))
    resp = req.json()
    location = resp['results'][0].get('geometry').get('location')

    req = requests.get(url_place.format(
                                        location['lat'],
                                        location['lng'],
                                        RADIUS,
                                        type_,
                                        keyword.replace(' ', '+'),
                                        API_KEY
        ))
    resp = req.json()
    for store in resp['results']:
        yield store['name'], store['vicinity']
