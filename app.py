from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import argparse
import json
from addict import Dict
from utils import de_empty, read_json
from crm_auth import authenticate
from apichecks import create_check
from notifications import create_notification
from exceptions.apichecks import ApiException
from logger import setup_log, get_logger

sched = BlockingScheduler()
api_by_sec_checks = None
notifications = None
log = None

@sched.scheduled_job('interval', seconds=1)
def check_job():
  print('Check job running...')
  for api_by_sec_check in api_by_sec_checks:
    try:
      api_by_sec_check()
    except ApiException as e:
      for notification in notifications:
        try:
          notification({
            'url': e.url,
            'error': str(e)
          })
        except Exception as ne:
          log(f'Notification failed: {str(ne)}')

def parse_arguments():
  global api_by_sec_checks
  global notifications
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', help='Config file')
  args = parser.parse_args()
  config_url = de_empty(args.config, 'config.json')
  config = read_json(config_url)
  config_obj = Dict(config)
  user = authenticate(config_obj.get('authentication'))
  user_obj = Dict(user)
  print(user)
  api_by_sec_checks = [
    # create_check(request_config)
    # for request_config in config_obj.get('requests', [])
  ]
  notifications = [
    # create_notification(noti_config[0], noti_config[1])
    # for noti_config in list(config_obj.get('notifications').items())
  ]

def init_log():
  global log
  setup_log()
  log = get_logger()

if __name__ == "__main__":
  init_log()
  parse_arguments()
  sched.start()
