from celery import Celery
from datetime import timedelta
import datetime
import json
import requests
import logging
#from valar import app
from valar import valar_settings as settings
from valar.utils import get_summaries, get_devices, hosts, send_mail
from valar_settings import valar_api


#hosts = settings.hosts

app = Celery('tasks')
from valar import celeryconfig
app.config_from_object(celeryconfig)

@app.task
def save_miner_stats():
  sums = get_summaries()
  devs = get_devices()
  payload = []
  for s in hosts:
    if s["name"] in sums:
        logging.info(s['name'] + ': ' + str(sums[s['name']]['SUMMARY'][0]['MHS 5s']) + ' MH/s')
        now = datetime.datetime.now()
        payload.append({ 
            'hashrate': int(sums[s['name']]['SUMMARY'][0]['MHS 5s'] * 1000), 
            'miner': s['_id'], 
            'when': now.strftime('%a, %d %b %Y %X GMT'),
        })
  headers = {"content-type": "application/json"}
  url = valar_api + "stat/"
  r = requests.post(url, headers = headers, data = json.dumps(payload))
  if sums["err"]:
        subject = "Valar ERROR"
        message = "Error\n\n{0}".format(sums["err"])
        send_mail(subject, message)
  return 'Success' if r.ok else 'failure'
