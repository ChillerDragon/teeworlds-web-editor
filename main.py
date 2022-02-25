#!/usr/bin/env python3

from flask import Flask
from flask import render_template, url_for

import numpy
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

@app.route('/api/v1/game')
def api_game():
    m = twmap.Map('/usr/share/teeworlds/data/maps/dm1.map')
    game_layer = {
        'tiles': [],
        'width': m.game_layer().width(),
        'height': m.game_layer().height()
    }
    for (y, x, flags), tile in numpy.ndenumerate(m.game_layer().tiles):
        if flags != 0:
            continue
        game_layer['tiles'].append((int)(tile))
    return game_layer
