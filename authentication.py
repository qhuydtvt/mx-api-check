import requests

class BearerAuth(requests.auth.AuthBase):
  def __init__(self, token):
    self.token = token
  
  def __call__(self, r):
    r.headers['Authorization'] = 'Bearer ' + self.token
    return r

def get_firebase_token(firebase_url, credentials):
  try:
    firebase_response = requests.post(firebase_url, json=credentials)
    return firebase_response.json()['idToken']
  except:
    raise Exception('Logging in to firebase failed')

def create_authentication(authentication_obj):
  auth_type = authentication_obj.type
  if auth_type == 'firebase':
    firebase_url = authentication_obj.firebase.url
    credentials = authentication_obj.firebase.credentials
    def closure_firebase_token_auth():
      token = get_firebase_token(firebase_url, credentials)
      print(token)
      return BearerAuth(token)
    return closure_firebase_token_auth