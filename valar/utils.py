import logging
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient

from valar.pycgm import CgminerAPI
from valar import valar_settings as settings


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.valar

hosts = [x for x in db.miner.find()]
if not hosts:
    hosts = settings.hosts
    db.miner.insert(hosts)

def get_summaries():
    results = {"err": []}
    for h in hosts:
        cgm = CgminerAPI(host=h['hostname'])
        try:
            results[h['name']] = cgm.summary()
        except Exception, errno:
            output = "Timeout: " + h['name'] + " " + str(Exception)
            results["err"].append(h) 
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
            results["err"].append(h)
            logging.error("timeout")
    return results


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
