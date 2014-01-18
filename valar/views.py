from flask import render_template
from valar import app
from valar.utils import get_hosts, get_summaries

@app.route('/')
def index():
    hosts = get_hosts()
    sums = get_summaries(hosts)
    return render_template("index.html", title = 'Valar', sums = sums, hosts = hosts)

