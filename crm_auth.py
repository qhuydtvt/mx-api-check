import requests
import json
from exceptions.apichecks import ApiException
from logger import get_logger

def authenticate(auth_config_obj):
  firebase_url = auth_config_obj.firebaseAPI
  auth_url = auth_config_obj.crmAuthAPI
  crm_cred = json.dumps(auth_config_obj.credential)
  firebase_response = requests.post(firebase_url, crm_cred)
  if firebase_response.status_code < 400:
    token_obj = {'idToken': firebase_response.json()['idToken']}
    token_obj = json.dumps(token_obj)
    response = requests.post(auth_url, token_obj, headers={'Content-Type': 'application/json; charset=utf-8'})
    if response.status_code < 400:
      return firebase_response.json()
