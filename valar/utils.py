import os
import smtplib
from email.mime.text import MIMEText
from valar.pycgm import CgminerAPI
from valar import settings

root_dir = os.path.dirname(os.path.abspath(__file__))

def get_hosts():
    return settings.hosts

def get_summaries(hosts):
    results = {}
    for h in hosts:
        cgm = CgminerAPI(host=h)
        results[h] = cgm.summary()
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

