import requests

def create_notification(notification_type, notification_config):
  if notification_type == 'httpEndpoint':
    url = notification_config.url
    def notify(json):
      nonlocal url
      response = requests.post(url, json=json)
      if response.status_code >= 400:
        print(response)
        raise Exception('Notication failed')
    return notify
  else:
    raise Exception('Notification type NOT supported')