import os
import smtplib
import logging
from email.mime.text import MIMEText
from valar.pycgm import CgminerAPI
from valar import settings

root_dir = os.path.dirname(os.path.abspath(__file__))

hosts = settings.hosts

def get_summaries():
    results = {}
    for h in hosts:
        cgm = CgminerAPI(host=h)
        try:
            results[h] = cgm.summary()
        except Exception, errno:
            logging.error("Timeout: " + str(Exception))
    return results

def get_devices():
    results = {}
    for h in hosts:
        cgm = CgminerAPI(host=h)
        try:
            data = cgm.devs()
            results[h] = data['DEVS']
        except Exception, errno:
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

