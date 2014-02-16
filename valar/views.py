from flask import render_template, Response
import requests
import json
from valar import app
from valar.utils import hosts, get_summaries, get_devices, send_mail
import pprint

@app.route('/')
def index():
    return render_template("index.html", 
        title = 'Valar', 
    )

@app.route('/miner')
def get_miners():
    results = []
    sums = get_summaries()
    devs = get_devices()

    for k, v in sums.iteritems():
        if k != "err":
            data = dict(
              [('name', k)] + \
              v['STATUS'][0].items() + \
              v['SUMMARY'][0].items()
            )
            data['devices'] = devs[k]

            results.append(data)
    if sums["err"]:
        subject = "Valar ERROR"
        message = "Error\n\n{0}".format(sums["err"])
        send_mail(subject, message)
    return Response(json.dumps(results), mimetype='application/json')
