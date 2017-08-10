# -*- coding: utf-8 -*-
#!/usr/bin/python
import os, sys
import requests

KEY = os.getenv('KEY')
	
def user_location(location=raw_input('Enter your location: \n')):
	
	"""This function returns the lattitude and longtitude of user's location.
	Param:
		location(string): User's location.
		
	Return:
		:rtype tuple: (lat, lng)
	"""
	
	payload = {
			'query': location, 
			'key': KEY
	}
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
	r = requests.get(url, params=payload)
	output = r.json()
	
	for item in output['results']:
		lat = item['geometry']['location']['lat']
		lng = item['geometry']['location']['lng']	
		
	return lat, lng
	
def store_location(search_type = 'electronics_store', keyword = 'sieu thi dien may'):
	
	"""This function returns a list of nearest electronic stores around given places.
	
	Params:
		search_type(string): Value of 'type' in "payload" dictionary.
		keyword(string): Value of 'keyword' in "payload" dictionary.
	Return:
		:rtype tuple: (name, address)
	"""
	
	keyword.replace("", "+")
	lat, lng = user_location()
	payload = { 
			'radius': 4000, 
			'type': search_type, 
			'keyword': keyword, 
			'key': KEY
	}
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}'.format(lat, lng)
	r = requests.get(url, params=payload)
	output = r.json()
	
	for item in output['results']:
		name = item['name']
		address = item['vicinity']
		yield name, address
