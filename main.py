#!/usr/bin/env python3

from flask import Flask
from flask import render_template, url_for

import twmap

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info('ellox')
    return 'return statement'

@app.route('/map')
def map():
    m = twmap.Map('/usr/share/teeworlds/data/maps/dm1.map')
    return render_template('map.html.j2', twmap = m, enumerate=enumerate)
