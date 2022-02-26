#!/usr/bin/env python3

from crypt import methods
from flask import Flask
from flask import render_template, send_from_directory, request

import os
from PIL import Image
from itertools import product

import numpy
import twmap
from pathlib import Path

app = Flask(__name__)

map_path = '/usr/share/teeworlds/data/maps/dm1.map'

# function by Ivan
# https://stackoverflow.com/a/65698752
def generate_tiles(filename, dir_in, dir_out, d):
    if not os.path.exists(f"{dir_in}/{filename}"):
        app.logger.info(f"not generating '{filename}' tiles due to missing data ...")
        return
    app.logger.info(f"generating '{filename}' tiles ...")
    Path(dir_in).mkdir(parents=True, exist_ok=True)
    Path(dir_out).mkdir(parents=True, exist_ok=True)
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        x = (int)(j / d)
        y = (int)(i / d)
        out = os.path.join(dir_out, f'{x}_{y}{ext}')
        img.crop(box).save(out)

@app.route('/tile/<tileset>/<int:x>/<int:y>')
def tile(tileset, x, y):
    """
    The /tile route serves tileset images as individual tiles
    """
    img_path = f"./data/{tileset}/{x}_{y}.png"
    if not os.path.exists(img_path):
        generate_tiles(f"{tileset}.png", './static/mapres', f"./data/{tileset}", 64)
    return send_from_directory(f"./data/{tileset}", f"{x}_{y}.png")

@app.route('/entities/<tileset>/<int:x>/<int:y>')
def entities(tileset, x, y):
    """
    The /entities route serves entity images as individual tiles
    """
    img_path = f"./data/entities/{tileset}/{x}_{y}.png"
    if not os.path.exists(img_path):
        generate_tiles(f"{tileset}.png", './static/entities', f"./data/entities/{tileset}", 64)
    return send_from_directory(f"./data/entities/{tileset}", f"{x}_{y}.png")

@app.route('/')
def index():
    app.logger.info('ellox')
    return 'return statement'

@app.route('/map')
def map():
    m = twmap.Map(map_path)
    return render_template('map.html.j2', twmap = m, enumerate=enumerate)

@app.route('/api/v1/game')
def api_game():
    m = twmap.Map(map_path)
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

@app.route('/api/v1/game/<int:tile>/<int:x>/<int:y>', methods=["POST"])
def api_set_gametile(tile, x, y):
    m = twmap.Map(map_path)
    tiles = m.game_layer().tiles
    tiles[y][x][0] = tile
    m.game_layer().tiles = tiles
    m.save(map_path)
    app.logger.info(f"set {tile} at {x}/{y}")
    return {'status': 'ok'}
