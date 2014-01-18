from flask import render_template
from valar import app

@app.route('/')
def index():
    return render_template("index.html", title = 'Valar')
