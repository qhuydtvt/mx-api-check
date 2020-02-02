from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import argparse
import json
from addict import Dict
from utils import de_empty, read_json
from apichecks import create_check
from notifications import create_notification
from exceptions.apichecks import ApiException

sched = BlockingScheduler()
api_by_sec_checks = None
notifications = None

@sched.scheduled_job('interval', seconds=1)
def check_job():
  print('This job is run every one seconds.')
  for api_by_sec_check in api_by_sec_checks:
    try:
      api_by_sec_check()
    except ApiException:
      for notification in notifications:
        notification({
          'error': True
        })

def parse_arguments():
  global api_by_sec_checks
  global notifications
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', help='Config file')
  args = parser.parse_args()
  config_url = de_empty(args.config, 'config.json')
  config = read_json(config_url)
  config_obj = Dict(config)
  api_by_sec_checks = [
    create_check(request_config)
    for request_config in config_obj.get('requests', [])
  ]
  notifications = [
    create_notification(noti_config[0], noti_config[1])
    for noti_config in list(config_obj.get('notifications').items())
  ]

if __name__ == "__main__":
  parse_arguments()
  sched.start()