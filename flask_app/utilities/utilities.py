import requests
from flask_app import API_KEY

#checks if a string has an uppercase character or not
def has_uppercase(string):
    for char in string:
        if char.isupper():
            return True
    return False


#checks if a string has one number or not
def has_number(string):
    for char in string:
        if char.isnumeric():
            return True
    return False


#translates location into lattitude and longitude
def convert_address(location):
    """
    :params: location
    :returns: object lat and lng
    """
    params = {
        'key': API_KEY,
        'address': location
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params).json()

    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        lat = geometry['location']['lat']
        lng = geometry['location']['lng']
    else:
        return
    
    translated_location = {
        'lat': lat,
        'lng': lng
    }

    return translated_location

