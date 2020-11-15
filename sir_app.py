#!/usr/bin/env python3
# coding: utf-8

import json, os, random, string
from collections import OrderedDict
from datetime import datetime, timedelta

from flask import Flask, abort, jsonify, render_template, request
from jsonschema import validate


with open('scene-definition-schema.json') as schema_file:
    SCENE_DEF_SCHEMA = json.load(schema_file)
SCENE_DEFS = (
    {'name': 'Hallways of Thime', 'img': {
        'url': 'https://chezsoi.org/lucas/jdr/shared-img-reveal/hallways_of_thime_by_djekspek_HD_no_comments.jpg',
        'width': 1158, 'height': 818,
        }, 'clips': [
            {'type': 'rect', 'x': 190, 'y': 0, 'width': 780, 'height': 36},  # Title
            {'type': 'ellipse', 'cx': 220, 'cy': 130, 'rx': 170, 'ry': 80},  # Entrance
            {'type': 'ellipse', 'cx': 260, 'cy': 270, 'rx': 110, 'ry': 120}, # Pitfall & tomb
            {'type': 'ellipse', 'cx': 380, 'cy': 210, 'rx': 90, 'ry': 70},   # Pitfall, stairs & arch
            {'type': 'ellipse', 'cx': 490, 'cy': 185, 'rx': 90, 'ry': 50},   # Transporter room
            {'type': 'ellipse', 'cx': 480, 'cy': 270, 'rx': 130, 'ry': 50},  # Arch & more hallways
            {'type': 'ellipse', 'cx': 670, 'cy': 240, 'rx': 110, 'ry': 60},  # 2 Coves
            {'type': 'ellipse', 'cx': 785, 'cy': 310, 'rx': 130, 'ry': 70},  # Columns
            {'type': 'ellipse', 'cx': 890, 'cy': 250, 'rx': 110, 'ry': 80},  # Temple
            {'type': 'ellipse', 'cx': 570, 'cy': 340, 'rx': 90, 'ry': 50},   # Tomb
            {'type': 'ellipse', 'cx': 470, 'cy': 400, 'rx': 60, 'ry': 60},   # Ladder
            {'type': 'ellipse', 'cx': 510, 'cy': 440, 'rx': 60, 'ry': 60},   # Crossroads
            {'type': 'ellipse', 'cx': 440, 'cy': 540, 'rx': 70, 'ry': 70},   # 2nd crossroads
            {'type': 'ellipse', 'cx': 570, 'cy': 400, 'rx': 60, 'ry': 40},   # Long corridor #1
            {'type': 'ellipse', 'cx': 690, 'cy': 380, 'rx': 80, 'ry': 30},   # Long corridor #2
            {'type': 'ellipse', 'cx': 780, 'cy': 420, 'rx': 50, 'ry': 30},   # Long corridor #3
            {'type': 'ellipse', 'cx': 915, 'cy': 465, 'rx': 110, 'ry': 80},  # Cellblock
            {'type': 'ellipse', 'cx': 620, 'cy': 480, 'rx': 100, 'ry': 80},  # Abandoned mine
            {'type': 'ellipse', 'cx': 750, 'cy': 530, 'rx': 60, 'ry': 35},   # Tunnels
            {'type': 'ellipse', 'cx': 835, 'cy': 560, 'rx': 70, 'ry': 60},   # Lost City stairs & tunnel entrance
            {'type': 'ellipse', 'cx': 750, 'cy': 650, 'rx': 150, 'ry': 110}, # Lost City
            {'type': 'ellipse', 'cx': 565, 'cy': 590, 'rx': 80, 'ry': 45},   # Water Basin
            {'type': 'ellipse', 'cx': 300, 'cy': 460, 'rx': 110, 'ry': 80},  # Machine Room
            {'type': 'ellipse', 'cx': 300, 'cy': 610, 'rx': 100, 'ry': 70},  # Treasure Cave
    ], 'images': [
        {'url': 'https://chezsoi.org/lucas/jdr/shared-img-reveal/rocks.png', 'x': 360, 'y': 210, 'width': 80, 'height': 80},
    ],'duration_in_min': 45},
    {'name': 'Adventure Time: Dungeon Crystal', 'img': {
        'url': 'https://chezsoi.org/lucas/jdr/shared-img-reveal/AdventureTimeDungeonCrystal.png',
        'width': 2043, 'height': 1150,
        }, 'clips': [
            {'type': 'ellipse', 'cx': 1200, 'cy': 1050, 'rx': 700, 'ry': 90}, # BOTTOM
            {'type': 'ellipse', 'cx': 1200, 'cy': 700, 'rx': 300, 'ry': 300}, # TOWER
            {'type': 'ellipse', 'cx': 1750, 'cy': 800, 'rx': 280, 'ry': 300}, # RIGHT
            {'type': 'ellipse', 'cx': 1700, 'cy': 290, 'rx': 350, 'ry': 280}, # TOP-RIGHT
            {'type': 'ellipse', 'cx': 400, 'cy': 830, 'rx':400, 'ry': 300},   # LEFT
            {'type': 'ellipse', 'cx': 580, 'cy': 290, 'rx': 580, 'ry': 280},  # TOP-LEFT
            {'type': 'ellipse', 'cx': 1250, 'cy': 300, 'rx': 200, 'ry': 150}, # DIAMOND
    ], 'duration_in_min': 20},
    {'name': 'Adventure Time: Dragon Carcass', 'img': {
        'url': 'https://chezsoi.org/lucas/jdr/shared-img-reveal/AdventureTimeDragonCarcass.png',
        'width': 2032, 'height': 1143,
        }, 'clips': [
            {'type': 'ellipse', 'cx': 1500, 'cy': 900, 'rx': 500, 'ry': 250}, # BOTTOM-RIGHT
            {'type': 'ellipse', 'cx': 700, 'cy': 800, 'rx': 400, 'ry': 350},  # BOTTOM-LEFT
            {'type': 'ellipse', 'cx': 300, 'cy': 400, 'rx': 400, 'ry': 400},  # TOP-LEFT
            {'type': 'ellipse', 'cx': 1000, 'cy': 350, 'rx': 400, 'ry': 300}, # TOP-MIDDLE
            {'type': 'ellipse', 'cx': 1600, 'cy': 350, 'rx': 400, 'ry': 300}, # TOP-RIGHT
    ], 'duration_in_min': 20},
)
APP = Flask(__name__, static_folder='.', static_url_path='')
TABLES = OrderedDict()  # in-memory data state
MAX_TABLES_COUNT = 50

@APP.route('/')
def index_as_html():
    return render_template('index.html', scene_defs=SCENE_DEFS)

@APP.route('/json')
def index_as_json():
    return jsonify({'tables_count': len(TABLES)})

@APP.route('/admin/<admin_id>', methods=('GET', 'POST'))
def admin_as_html(admin_id):
    # TABLES[admin_id] = {'scene_def': SCENE_DEFS[0], 'public_id': 'ABCDEF', 'visible_clips': [], 'display_all': False}
    if request.method == 'POST':
        if admin_id not in TABLES:  # => table creation
            autocleanup()
            scene_def_id = request.form.get('scene_def_id') and int(request.form.get('scene_def_id'))
            if scene_def_id:
                scene_def = SCENE_DEFS[scene_def_id - 1].copy()
            elif request.form.get('scene_def'):
                scene_def = json.loads(request.form['scene_def'])
                validate(instance=scene_def, schema=SCENE_DEF_SCHEMA)  # avoids any HTML/SVG injection
                if not any(scene_def['name'] == sd['name'] for sd in SCENE_DEFS):
                    print('Creating table from custom scene definition!'
                          ' admin_id=', admin_id, 'name:', scene_def['name'])
            else:
                abort(422, 'Invalid input: missing "scene_def_id" or "scene_def"')
            if 'clips' not in scene_def:
                scene_def['clips'] = []
            if 'images' not in scene_def:
                scene_def['images'] = []
            TABLES[admin_id] = {
                'scene_def': scene_def,
                'public_id': ''.join(random.choices(string.ascii_uppercase, k=6)),
                'visible_clips': [],
                'visible_images': [],
                'display_all': False,
                'timer_end': None,
            }
        else:  # => table update
            table = TABLES[admin_id]
            table['display_all'] = request.form.get('display_all') == 'on'
            if request.form.get('reset_timer') == 'on':
                countdown_minutes = int(request.form['countdown_minutes'])
                table['timer_end'] = (datetime.now() + timedelta(minutes=countdown_minutes)).timestamp()
            table['visible_clips'] = [int(key.split('enable_clip_')[1]) for key, value in request.form.items()
                                      if key.startswith('enable_clip_') and value == 'on']
            table['visible_images'] = [int(key.split('enable_image_')[1]) for key, value in request.form.items()
                                      if key.startswith('enable_image_') and value == 'on']
            TABLES.move_to_end(admin_id)  # move on top of OrderedDict (must be done manually on updates)
    return render_template('admin.html', table=TABLES[admin_id])

@APP.route('/table/<public_id>')
def table_as_html(public_id):
    table = next(t for t in TABLES.values() if t['public_id'] == public_id)
    return render_template('table.html', table=table)

@APP.route('/table/<public_id>/json')
def table_as_json(public_id):
    table = next(t for t in TABLES.values() if t['public_id'] == public_id)
    return jsonify(table)

def autocleanup():
    while len(TABLES) > MAX_TABLES_COUNT:
        admin_id, table = TABLES.popitem(last=True)
        print('autocleanup removed table:', table['name'], 'admin_id=', admin_id, 'public_id=', table['public_id'])


if __name__ == '__main__':
    APP.run(port=int(os.environ.get('PORT', '8086')))
