import requests

def create_notification(notification_type, notification_config):
  if notification_type == 'httpEndpoint':
    url = notification_config.url
    def end_point_notify(json):
      nonlocal url
      response = requests.post(url, json=json)
      if response.status_code >= 400:
        print(response)
        raise Exception('Notication failed')
    return end_point_notify
  if notification_type == 'telegram':
    chat_id = notification_config.chatId
    bot_id = notification_config.botId
    bot_token = notification_config.botToken
    url = f'https://api.telegram.org/bot{bot_id}:{bot_token}/sendMessage'
    def telegram_notify(input_json):
      nonlocal url
      nonlocal chat_id
      json = {
        'chat_id': chat_id,
        'text': input_json['error'],
        'parse_mode': 'Markdown'
      }
      response = requests.post(url, json=json)
      if response.status_code >= 400:
        print(response)
        raise Exception('Notication failed')
    return telegram_notify
  else:
    raise Exception('Notification type NOT supported')