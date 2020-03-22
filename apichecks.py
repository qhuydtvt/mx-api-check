import requests
from exceptions.apichecks import ApiException
from logger import get_logger
from authentication import create_authentication

def create_check(request_config_obj):
  log = get_logger()
  url = request_config_obj.url
  get_auth = create_authentication(request_config_obj.authentication)
  seconds_to_check = request_config_obj.get('checkEvery', 30)
  timeout = request_config_obj.get('timeOut', 10)
  seconds = 0
  seconds_to_last_errors = 0
  def closure_tick():
    nonlocal seconds
    nonlocal log
    nonlocal timeout
    nonlocal seconds_to_last_errors
    seconds += 1
    print(f'{seconds_to_check - seconds} seconds to check {url}')
    if seconds >= seconds_to_check:
      seconds = 0
      try:
        log(f'Checking {url}')
        response = None
        if get_auth:
          response = requests.get(url, timeout=timeout, auth=get_auth())
        else:
          response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
          raise ApiException(url, f'API response with code {response.status_code}')
        seconds_to_last_errors = 0
        response_text = response.text.encode('utf-8')
        log(f'{url} response: {response_text}')
        log(f'{url} is OK')
      except Exception as e:
        log(f'{url} is NOT OK {str(e)}')
        log(f'Seconds to last errors: {seconds_to_last_errors}')
        should_raise_exception = False
        if seconds_to_last_errors == 0:
          should_raise_exception = True
        seconds_to_last_errors += seconds_to_check
        if seconds_to_last_errors >= 60:
          seconds_to_last_errors = 0
        if should_raise_exception:
          log('Raising exception')
          raise ApiException(url, message=str(e))
  
  return closure_tick
