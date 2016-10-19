# https://github.com/yelp/yelp-python

import io, json, requests
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from collections import Counter

def get_search_parameters(lat,lon):
  #See the Yelp API for more details
  params = {}
  params["term"] = "tech"
  params["ll"] = "{},{}".format(str(lat),str(lon))
  params["radius_filter"] = "2000"
  params["limit"] = "10"
  print params
  return params


def get_results(client, params):
  response = client.search('New York, NY',**params)
  #Transforms the JSON API response into a Python dictionary
  return response

def main():
# read API keys
  with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    session = Oauth1Authenticator(**creds)
    client = Client(session)

  locations = [(40.744, -73.985)]
  api_calls = []

  neighborhood_counter = Counter()
  for lat,lon in locations:
    params = get_search_parameters(lat,lon)
    results = client.search_by_coordinates(lat, lon, **params)

    #Be a good internet citizen and rate-limit yourself
    for b in results.businesses:
      # business fields: 'categories', 'deals', 'display_phone', 'distance', 'eat24_url', 'gift_certificates', 'id', 'image_url', 'is_claimed', 'is_closed', 'location', 'menu_date_updated', 'menu_provider', 'mobile_url', 'name', 'phone', 'rating', 'rating_img_url', 'rating_img_url_large', 'rating_img_url_small', 'reservation_url', 'review_count', 'reviews', 'snippet_image_url', 'snippet_text', 'url'
      print b.name
      print "Street address: %s"%b.location.cross_streets
      print "Neighborhoods: %s"%b.location.neighborhoods
      print b.location.coordinate.latitude, b.location.coordinate.longitude
      neighborhood_counter.update(b.location.neighborhoods)
      # 'address', 'city', 'coordinate', 'country_code', 'cross_streets', 'display_address', 'geo_accuracy', 'neighborhoods', 'postal_code', 'state_code'

    print neighborhood_counter




       
  ##Do other processing

if __name__=="__main__":
	main()