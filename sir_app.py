#!/usr/bin/env python3
# coding: utf-8

import copy, json, os, random, string, time
from collections import OrderedDict
from datetime import datetime, timedelta
from urllib.parse import unquote_plus
from urllib.request import urlopen

from flask import Flask, abort, jsonify, render_template, request
from jsonschema import validate
from PIL import Image


with open('scene-definition-schema.json', encoding='utf8') as schema_file:
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
    ], 'add': [
        {'type': 'image', 'xlink:href': 'https://chezsoi.org/lucas/jdr/shared-img-reveal/rocks.png', 'x': 360, 'y': 210, 'width': 80, 'height': 80},
    ], 'duration_in_min': 45},
    {'name': 'Enquête sous pression à ValTordu', 'img': {
        'url': 'https://chezsoi.org/lucas/jdr/shared-img-reveal/EnqueteAuVillage.jpg',
        'width': 1575, 'height': 881,
        }, 'clips': [
            # North-West
            {'type': 'ellipse', 'cx': 170, 'cy': 80, 'rx': 150, 'ry': 120},  # North-West exit
            {'type': 'ellipse', 'cx': 350, 'cy': 360, 'rx': 240, 'ry': 200},  # Market place
            {'type': 'ellipse', 'cx': 80, 'cy': 270, 'rx': 90, 'ry': 120},  # Court on the West
            {'type': 'ellipse', 'cx': 110, 'cy': 470, 'rx': 110, 'ry': 120},  # Enclosure on the West
            {'type': 'ellipse', 'cx': 550, 'cy': 200, 'rx': 70, 'ry': 80},  # Passage north
            {'type': 'ellipse', 'cx': 490, 'cy': 70, 'rx': 200, 'ry': 110},  # North area
            {'type': 'ellipse', 'cx': 700, 'cy': 170, 'rx': 120, 'ry': 120},  # Church
            {'type': 'ellipse', 'cx': 620, 'cy': 500, 'rx': 150, 'ry': 100},  # Mill
            {'type': 'ellipse', 'cx': 650, 'cy': 340, 'rx': 120, 'ry': 100},  # Main street
            # South-East
            {'type': 'ellipse', 'cx': 830, 'cy': 410, 'rx': 130, 'ry': 110},  # Main street
            {'type': 'ellipse', 'cx': 1100, 'cy': 470, 'rx': 220, 'ry': 190},  # Well place
            {'type': 'ellipse', 'cx': 1430, 'cy': 490, 'rx': 170, 'ry': 170},  # Forge & East exit
            {'type': 'ellipse', 'cx': 930, 'cy': 680, 'rx': 160, 'ry': 170},  # The fields
            {'type': 'ellipse', 'cx': 1210, 'cy': 720, 'rx': 220, 'ry': 120},  # The farm, south
            # Portraits
            {'type': 'ellipse', 'cx': 930, 'cy': 140, 'rx': 110, 'ry': 140},  # Priest
            {'type': 'ellipse', 'cx': 1184, 'cy': 140, 'rx': 110, 'ry': 140},  # Scholar
            {'type': 'ellipse', 'cx': 1442, 'cy': 140, 'rx': 110, 'ry': 140},  # Crook
            {'type': 'ellipse', 'cx': 120, 'cy': 740, 'rx': 110, 'ry': 140},  # Wizard
            {'type': 'ellipse', 'cx': 378, 'cy': 740, 'rx': 110, 'ry': 140},  # Mayor
            {'type': 'ellipse', 'cx': 635, 'cy': 740, 'rx': 110, 'ry': 140},  # Clockmaker
    ], 'add': [
        {'type': 'text', 'content': 'Faraday', 'x': 32, 'y': 825,
                         'font-family': 'Arial Black', 'font-size': 40, 'fill': 'white'},
        {'type': 'text', 'content': 'Douglas', 'x': 290, 'y': 825,
                         'font-family': 'Arial Black', 'font-size': 40, 'fill': 'white'},
        {'type': 'text', 'content': 'Erneste', 'x': 550, 'y': 825,
                         'font-family': 'Arial Black', 'font-size': 40, 'fill': 'white'},
        {'type': 'text', 'content': 'Sirius', 'x': 870, 'y': 220,
                         'font-family': 'Arial Black', 'font-size': 40, 'fill': 'white'},
        {'type': 'text', 'content': 'Marko', 'x': 1110, 'y': 220,
                         'font-family': 'Arial Black', 'font-size': 40, 'fill': 'white'},
        {'type': 'text', 'content': 'Jacques', 'x': 1350, 'y': 220,
                         'font-family': 'Arial Black', 'font-size': 40, 'fill': 'white'},
    ], 'duration_in_min': 45},
)
APP = Flask(__name__, static_folder='.', static_url_path='')
TABLES = OrderedDict()  # in-memory data state
MAX_TABLES_COUNT = int(os.environ.get('MAX_TABLES_COUNT', '50'))
PORT = int(os.environ.get('PORT', '8086'))
MODULE_LOAD_START_TIME = time.time()

@APP.route('/')
def index_as_html():
    return render_template('index.html', scene_defs=SCENE_DEFS)

@APP.route('/json')
def index_as_json():
    table_last_update_times = [table['last_update_time'] for table in TABLES.values()]
    return jsonify({
        'last_table_update_time': max(table_last_update_times) if table_last_update_times else None,
        'tables': TABLES,
        'MAX_TABLES_COUNT': MAX_TABLES_COUNT,
        'uptime_in_hours': int(time.time() - MODULE_LOAD_START_TIME) / 3600,
    })

@APP.route('/admin/<admin_id>', methods=('GET', 'POST'))
def admin_as_html(admin_id):
    # Uncomment this while working on a scene, to help iterating on SVGs positions:
    # TABLES[admin_id] = {'scene_def': SCENE_DEFS[0], 'public_id': 'ABCDEF', 'visible_clips': [], 'display_all': False}
    if request.method == 'POST':
        if admin_id not in TABLES:  # => table creation
            autocleanup()
            scene_def_id = request.form.get('scene_def_id') and int(request.form.get('scene_def_id'))
            image_url = request.form.get('image_url')
            if scene_def_id:
                scene_def = copy.deepcopy(SCENE_DEFS[scene_def_id - 1])
            elif image_url:
                if not image_url.startswith('http'):
                    abort(422, 'Invalid input: "image_url" must be an HTTP URL')
                clip_width = int(request.form.get('clip_width', '50'))
                clip_height = int(request.form.get('clip_height', '50'))
                offset_x = int(request.form.get('offset_x', '0'))
                offset_y = int(request.form.get('offset_y', '0'))
                scene_def = scene_def_from_image(image_url, clip_width, clip_height, offset_x, offset_y)
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
            if 'add' not in scene_def:
                scene_def['add'] = []
            table = {
                'scene_def': scene_def,
                'public_id': ''.join(random.choices(string.ascii_uppercase, k=6)),
                'visible_clips': [],
                'added_elems': [],
                'display_all': False,
                'timer_end': None,
            }
            TABLES[admin_id] = table
        else:  # => table update
            table = TABLES[admin_id]
            table['display_all'] = request.form.get('display_all') == 'on'
            if request.form.get('reset_timer') == 'on':
                countdown_minutes = int(request.form['countdown_minutes'])
                table['timer_end'] = (datetime.now() + timedelta(minutes=countdown_minutes)).timestamp()
            table['visible_clips'] = [int(key.split('enable_clip_')[1]) for key, value in request.form.items()
                                      if key.startswith('enable_clip_') and value == 'on']
            table['added_elems'] = [int(key.split('enable_elem_')[1]) for key, value in request.form.items()
                                    if key.startswith('enable_elem_') and value == 'on']
            TABLES.move_to_end(admin_id)  # move on top of OrderedDict (must be done manually on updates)
        table['last_update_time'] = datetime.now()
    return render_template('admin.html', table=TABLES[admin_id])

@APP.route('/table/<public_id>')
def table_as_html(public_id):
    table = next(t for t in TABLES.values() if t['public_id'] == public_id)
    return render_template('table.html', table=table)

@APP.route('/table/<public_id>/json')
def table_as_json(public_id):
    table = next(t for t in TABLES.values() if t['public_id'] == public_id)
    return jsonify(table)

def scene_def_from_image(image_url, clip_width, clip_height, offset_x=0, offset_y=0):
    name = os.path.splitext(unquote_plus(os.path.basename(image_url)))[0]
    with Image.open(urlopen(image_url)) as img:
        width, height = img.size  # nosec: URL scheme is checked by calling function
    x, clips = offset_x, []
    while x < width:
        y = offset_y
        while y < height:
            clips.append({'type': 'rect', 'x': x, 'y': y,
                          'width': min(clip_width, width - x),
                          'height': min(clip_height, height - y)})
            y += clip_height
        x += clip_width
    return {
        'name': name,
        'img': {
            'url': image_url,
            'width': width, 'height': height,
        }, 'clips': clips}

def autocleanup():
    while len(TABLES) > MAX_TABLES_COUNT:
        admin_id, table = TABLES.popitem(last=True)
        print('autocleanup removed table:', table['scene_def']['name'], 'admin_id=', admin_id, 'public_id=', table['public_id'])


if __name__ == '__main__':
    APP.run(port=PORT)
