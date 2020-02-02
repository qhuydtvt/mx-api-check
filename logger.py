import logging
from datetime import datetime
import sys
import os

def setup_log(logger_name='api-check'):
  if not os.path.isdir('./logs'):
    os.mkdir('./logs')

  filename = f"./logs/{logger_name}-{datetime.now().strftime('%y-%m-%d')}.log"
  file_handler = logging.FileHandler(filename, mode='w')
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)
  l = logging.getLogger(logger_name)
  l.addHandler(file_handler)
  l.setLevel(logging.DEBUG)

def get_logger(name='api-check'):
  logger = logging.getLogger(name)
  def log(msg):
    nonlocal logger
    logger.info(msg)
    print(msg)
  return log
