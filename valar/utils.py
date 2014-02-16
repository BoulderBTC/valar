import os
import logging
import socket
import requests
import json
import smtplib
from email.mime.text import MIMEText
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
    results = {"err": []}
    for h in hosts:
        cgm = CgminerAPI(host=h['hostname'])
        try:
            results[h['name']] = cgm.summary()
        except Exception, errno:
            output = "Timeout: " + h['name'] + " " + str(Exception)
            results["err"].append(h["name"] + " - " + output) 
            logging.error(output)
    return results

def get_devices():
    results = {"err": []}
    for h in hosts:
        cgm = CgminerAPI(host=h['hostname'])
        try:
            data = cgm.devs()
            results[h['name']] = data['DEVS']
        except Exception, errno:
            results["err"].append(h["name"] + " timeout!")
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


def send_mail(subject, message):
    username = settings.gmail_user
    password = settings.gmail_password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    msg = MIMEText(message)
    sender = settings.email_sender
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(settings.toaddrs)
    server.sendmail(sender, settings.toaddrs, msg.as_string())
