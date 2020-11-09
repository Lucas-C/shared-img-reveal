#!/usr/bin/env python3
# coding: utf-8

import json, os, random, string
from collections import OrderedDict

from flask import Flask, abort, jsonify, render_template, request


SCENE_DEFS = (
    {'name': 'Adventure Time: Dungeon Crystal', 'img': {
        'url': 'https://chezsoi.org/lucas/shared-img-reveal/AdventureTimeDungeonCrystal.png',
        'width': 2043, 'height': 1150,
        }, 'clips': (
            {'type': 'ellipse', 'cx': 1200, 'cy': 1050, 'rx': 700, 'ry': 90}, # BOTTOM
            {'type': 'ellipse', 'cx': 1200, 'cy': 700, 'rx': 300, 'ry': 300}, # TOWER
            {'type': 'ellipse', 'cx': 1750, 'cy': 800, 'rx': 280, 'ry': 300}, # RIGHT
            {'type': 'ellipse', 'cx': 1700, 'cy': 290, 'rx': 350, 'ry': 280}, # TOP-RIGHT
            {'type': 'ellipse', 'cx': 400, 'cy': 830, 'rx':400, 'ry': 300},   # LEFT
            {'type': 'ellipse', 'cx': 580, 'cy': 290, 'rx': 580, 'ry': 280},  # TOP-LEFT
            {'type': 'ellipse', 'cx': 1250, 'cy': 300, 'rx': 200, 'ry': 150}, # DIAMOND
    )},
    {'name': 'Adventure Time: Dragon Carcass', 'img': {
        'url': 'https://chezsoi.org/lucas/shared-img-reveal/AdventureTimeDragonCarcass.png',
        'width': 2032, 'height': 1143,
        }, 'clips': (
            {'type': 'ellipse', 'cx': 1500, 'cy': 900, 'rx': 500, 'ry': 250}, # BOTTOM-RIGHT
            {'type': 'ellipse', 'cx': 700, 'cy': 800, 'rx': 400, 'ry': 350},  # BOTTOM-LEFT
            {'type': 'ellipse', 'cx': 300, 'cy': 400, 'rx': 400, 'ry': 400},  # TOP-LEFT
            {'type': 'ellipse', 'cx': 1000, 'cy': 350, 'rx': 400, 'ry': 300}, # TOP-MIDDLE
            {'type': 'ellipse', 'cx': 1600, 'cy': 350, 'rx': 400, 'ry': 300}, # TOP-RIGHT
    )},
)
APP = Flask(__name__, static_folder='.', static_url_path='')
TABLES = OrderedDict()  # in-memory data state
MAX_TABLES_COUNT = 50


@APP.route('/')
def index():
    return render_template('index.html', scene_defs=SCENE_DEFS)

@APP.route('/admin/<admin_id>', methods=('GET', 'POST'))
def admin(admin_id):
    # TABLES[admin_id] = {'scene_def': SCENE_DEFS[0], 'public_id': 'ABCDEF', 'visible_clips': [], 'display_all': False}
    if request.method == 'POST':
        if admin_id not in TABLES:  # => table creation
            autocleanup()
            scene_def_id = request.form.get('scene_def_id') and int(request.form.get('scene_def_id'))
            if scene_def_id:
                scene_def = SCENE_DEFS[scene_def_id - 1]
            elif request.form.get('scene_def'):
                scene_def = json.loads(request.form['scene_def'])
            else:
                abort(422, 'Invalid input: missing "scene_def_id" or "scene_def"')
            TABLES[admin_id] = {
                'scene_def': scene_def,
                'public_id': ''.join(random.choices(string.ascii_uppercase, k=6)),
                'visible_clips': [],
                'display_all': False,
            }
        else:  # => table update
            table = TABLES[admin_id]
            print(f'Table admin={admin_id}/public={table["public_id"]} update: {request.form}')
            table['display_all'] = request.form.get('display_all') == 'on'
            table['visible_clips'] = [int(key.split('enable_clip_')[1]) for key, value in request.form.items()
                                      if key.startswith('enable_clip_') and value == 'on']
            TABLES.move_to_end(admin_id)  # move on top of OrderedDict (must be done manually on updates)
    return render_template('admin.html', table=TABLES[admin_id])

@APP.route('/table/<public_id>')
def table(public_id):
    table = next(t for t in TABLES.values() if t['public_id'] == public_id)
    return render_template('table.html', table=table)

@APP.route('/table/<public_id>/json')
def table_json(public_id):
    table = next(t for t in TABLES.values() if t['public_id'] == public_id)
    return jsonify(table)

@APP.route('/json')
def root_json():
    return jsonify({'tables_count': len(TABLES)})

def autocleanup():
    while len(TABLES) > MAX_TABLES_COUNT:
        table = TABLES.popitem(last=True)
        print('Removed:', table)


if __name__ == '__main__':
    APP.run(port=int(os.environ.get('PORT', '8086')))
