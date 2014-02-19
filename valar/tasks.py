from celery import Celery
from datetime import timedelta
import datetime
import json
import requests
import logging
import time
from pymongo import MongoClient
#from valar import app
from valar import valar_settings as settings
from valar.utils import hosts, get_summaries, get_devices, hosts, send_mail
from valar_settings import valar_api
from valar.fabfile import restart

#hosts = settings.hosts

app = Celery('tasks')
from valar import celeryconfig
app.config_from_object(celeryconfig)

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.valar

@app.task
def save_miner_stats():
  sums = get_summaries()
  devs = get_devices()
  payload = []
  
  for s in hosts:
      
      if s["name"] not in sums:
          sums[s["name"]] = {"SUMMARY": [{'MHS 5s': 0}]}
        
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
      message = "Error\n\n{0}".format(", ".join([x["name"] for x in sums["err"]]))
      #send_mail(subject, message)
      for h in sums["err"]:
          #db.restarts.insert({"name": h, "when": time.time()})
          restarted = db.restarts.find_one({"hostname": h["hostname"]})
          if restarted:
              if (time.time() - restarted["when"]) / 60 > 10:
                  
                  restarted["when"] = time.time()
                  db.restarts.save(restarted)
                  print (time.time() - restarted["when"]) / 60
                  send_mail(subject, message)
                  restart(h["hostname"])
          elif not restarted:
              db.restarts.insert({"hostname": h["hostname"], "when": time.time()})
              restart(h["hostname"])
              #send_mail(subject, message)
  
  return 'Success' if r.ok else 'failure'
