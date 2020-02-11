import requests
from logger import get_logger
import json
from exceptions.apichecks import ApiException
from logger import get_logger

def authenticate(auth_config_obj):
  log = get_logger()
  seconds_to_check = 30
  firebase_url = auth_config_obj.firebaseAPI
  auth_url = auth_config_obj.crmAuthAPI
  crm_cred = json.dumps(auth_config_obj.credential)
  try:
    firebase_response = requests.post(firebase_url, crm_cred)
    token_obj = {'idToken': firebase_response.json()['idToken']}
    token_obj = json.dumps(token_obj)
    log(f'Checking {auth_url}')
    response = requests.post(auth_url, token_obj, headers={'Content-Type': 'application/json; charset=utf-8'})
    if response.status_code >= 400:
      raise ApiException(auth_url, f'API response with code {response.status_code}')
    seconds_to_last_errors = 0
    log(f'{auth_url} is OK')
  except Exception as e:
    log(f'{auth_url} is NOT OK {str(e)}')
    log(f'Seconds to last errors: {seconds_to_last_errors}')
    should_raise_exception = False
    if seconds_to_last_errors == 0:
      should_raise_exception = True
    seconds_to_last_errors += seconds_to_check
    if seconds_to_last_errors >= 60:
      seconds_to_last_errors = 0
    if should_raise_exception:
      log('Raising exception')
      raise ApiException(auth_url, message=str(e))
  return firebase_response.json()
