import os
import smtplib
from email.mime.text import MIMEText
from flask import render_template
from valar import app
from valar.pycgm import CgminerAPI  
from valar import settings

root_dir = os.path.dirname(os.path.abspath(__file__))

def get_hosts():
    hosts = []
    with open(root_dir + '/hosts.txt') as ifile:
        for l in ifile.readlines():
            hosts.append(l.strip())
            
    return hosts

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

@app.route('/')
def index():
    hosts = get_hosts()
    sums = get_summaries(hosts)
    return render_template("index.html", title = 'Valar', sums = sums, hosts = hosts)

