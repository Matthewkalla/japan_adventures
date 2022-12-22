from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import API_KEY

def get_place_details(place_id):
#set up the API client
    credentials = Credentials.from_api_key(API_KEY)
    service = build('maps', 'v3', credentials=credentials)

#get the details of the place
    response = service.places().get(placeId=place_id).execute()
    return response


#setting up the API client
def search_places(query):

    credentials = Credentials.from_api_key(API_KEY)
    service = build('maps', 'v3', credentials=credentials)


    #Search for places
    response = service.places().textSearch(query=query).execute()
    return response['results']