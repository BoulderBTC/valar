from flask import render_template
from valar import app
from valar.utils import hosts, get_summaries, get_devices

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

