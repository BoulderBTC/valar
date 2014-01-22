from celery import Celery
from datetime import timedelta
from valar import app, settings
from valar.utils import get_summaries, get_devices
import logging

hosts = settings.hosts

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def save_miner_stats():
  sums = get_summaries()
  devs = get_devices()
  for s in hosts:
    logging.info(s + ': ' + str(sums[s]['SUMMARY'][0]['MHS 5s']) + ' MH/s')
  return 'Success'
