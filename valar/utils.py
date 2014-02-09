import os
import logging
import socket
import requests
import json
from valar.pycgm import CgminerAPI
from valar import valar_settings as settings
from valar_settings import valar_api


url = valar_api + "miner/"
r = requests.get(url)
if r.ok and len(r.json()['_items']) > 0:
    hosts = r.json()['_items']
else:
    payload = settings.hosts
    headers = {"content-type": "application/json"}
    r = requests.post(url, headers = headers, data = json.dumps(payload))
    r = requests.get(url)
    hosts = r.json()['_items']



def get_summaries():
    results = {}
    for h in hosts:
        cgm = CgminerAPI(host=h['hostname'])
        try:
            results[h['name']] = cgm.summary()
        except Exception, errno:
            logging.error("Timeout: " + str(Exception))
    return results

def get_devices():
    results = {}
    for h in hosts:
        cgm = CgminerAPI(host=h['hostname'])
        try:
            data = cgm.devs()
            results[h['name']] = data['DEVS']
        except Exception, errno:
            logging.error("timeout")
            
    return results

def check_workers():
    for h in hosts:
        if not check_worker(h['hostname']):
            return False
    return True

def check_worker(h):
    try:
        cgm = CgminerAPI(host=h)
        result = cgm.summary()
    except socket.error as e:
        subject = "{0} - ERROR".format(h)
        message = "{0} - Error\n\n{1}".format(h, e)
        send_mail(subject, message)
        return False
    return True



