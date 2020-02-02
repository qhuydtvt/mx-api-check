import requests
from exceptions.apichecks import ApiException

def create_check(request_config_obj):
  url = request_config_obj.url
  seconds_to_check = request_config_obj.checkEvery
  seconds = 0
  def tick():
    nonlocal seconds
    seconds += 1
    print(f'{seconds} to check ${url}')
    if seconds >= seconds_to_check:
      seconds = 0
      try:
        response = requests.get(url)
        if response.status_code >= 400:
          raise ApiException(url)
      except:
        raise ApiException(url)
  
  return tick
