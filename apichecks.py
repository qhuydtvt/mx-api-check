import requests
from exceptions.apichecks import ApiException
from logger import get_logger

def create_check(request_config_obj):
  log = get_logger()
  url = request_config_obj.url
  seconds_to_check = request_config_obj.get('checkEvery', 30)
  timeout = request_config_obj.get('timeOut', 10)
  seconds = 0
  def tick():
    nonlocal seconds
    nonlocal log
    nonlocal timeout
    seconds += 1
    print(f'{seconds_to_check - seconds} seconds to check {url}')
    if seconds >= seconds_to_check:
      seconds = 0
      try:
        log(f'Checking {url}')
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
          raise ApiException(url, 'API response with code >= 400')
      except Exception as e:
        log(f'{url} is NOT OK {str(e)}')
        raise ApiException(url, message=str(e))
      log(f'{url} is OK')
  
  return tick
