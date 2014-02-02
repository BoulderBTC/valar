from flask import render_template, Response
import requests
import json
from valar import app
from valar.utils import hosts, get_summaries, get_devices
import pprint

@app.route('/')
def index():
    sums = get_summaries()
    devs = get_devices()
    return render_template("index.html", 
        title = 'Valar', 
        hosts = hosts, 
        sums = sums, 
        devs = devs
    )

@app.route('/miner')
def get_miners():

    results = []
    sums = get_summaries()
    devs = get_devices()
    for k, v in sums.iteritems():
        data = dict(
          [('name', k)] + \
          v['STATUS'][0].items() + \
          v['SUMMARY'][0].items()
        )
        data['devices'] = devs[k]
        results.append(data)
        
    return Response(json.dumps(results), mimetype='application/json')
