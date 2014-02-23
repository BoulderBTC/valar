from flask import render_template, Response

import json
from valar import app
from valar.utils import get_summaries, get_devices

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
            if k in devs:
                data['devices'] = devs[k]

            results.append(data)

    return Response(json.dumps(results), mimetype='application/json')
