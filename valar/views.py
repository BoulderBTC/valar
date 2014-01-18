import os
from flask import render_template
from valar import app
from valar.pycgm import CgminerAPI

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


@app.route('/')
def index():
    hosts = get_hosts()
    sums = get_summaries(hosts)
    return render_template("index.html", title = 'Valar', sums = sums, hosts = hosts)

