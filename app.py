from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import argparse
import json
from addict import Dict
from utils import de_empty, read_json
from crm_auth import authenticate
from apichecks import create_check
from queuecheck import create_queue_check
from notifications import create_notification
from exceptions.apichecks import ApiException
from logger import setup_log, get_logger

sched = BlockingScheduler(timezone='Asia/Ho_Chi_Minh')
api_by_sec_checks = []
queue_by_sec_checks = []
notifications = None
log = None

@sched.scheduled_job('interval', seconds=1)
def check_job():
  print('Check job running...')
  for api_by_sec_check in api_by_sec_checks + queue_by_sec_checks:
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
  global queue_by_sec_checks
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
  queue_by_sec_checks = [
    create_queue_check(request_config)
    for request_config in config_obj.get('queueUrls', [])
  ]
  notifications = [
    create_notification(noti_config[0], noti_config[1])
    for noti_config in list(config_obj.get('notifications').items())
  ]

  init_log(config_obj.log)

def init_log(log_obj):
  global log
  setup_log(log_obj)
  log = get_logger()

if __name__ == "__main__":
  init_log()
  parse_arguments()
  sched.start()
