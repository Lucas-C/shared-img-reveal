#!/usr/bin/env python3
# coding: utf-8
# TODO: allow to provide a custom table_definition.json file

import os, random, string
from collections import OrderedDict

from flask import Flask, abort, jsonify, render_template, request


TABLE_DEFS = (
    {'name': 'Adventure Time Dungeon Crystal', 'img': {
        'url': 'https://chezsoi.org/lucas/shared-img-reveal/AdventureTimeDungeonCrystal.png',
        'width': 2048, 'height': 1157,
        }, 'clips': (
            {'type': 'ellipse', 'cx': 1200, 'cy': 1050, 'rx': 700, 'ry': 90}, # START
            {'type': 'ellipse', 'cx': 1200, 'cy': 700, 'rx': 300, 'ry': 300}, # TOWER
            {'type': 'ellipse', 'cx': 1750, 'cy': 800, 'rx': 280, 'ry': 300}, # RIGHT
            {'type': 'ellipse', 'cx': 1700, 'cy': 290, 'rx': 350, 'ry': 280}, # TOP-RIGHT
            {'type': 'ellipse', 'cx': 400, 'cy': 830, 'rx':400, 'ry': 300}, # LEFT
            {'type': 'ellipse', 'cx': 580, 'cy': 290, 'rx': 580, 'ry': 280}, # TOP-LEFT
            {'type': 'ellipse', 'cx': 1250, 'cy': 300, 'rx': 200, 'ry': 150}, # DIAMOND
    )},
)
APP = Flask(__name__, static_folder='.', static_url_path='')
TABLES = OrderedDict()  # in-memory data state
MAX_TABLES_COUNT = 50


@APP.route('/')
def index():
    return render_template('index.html', table_defs=TABLE_DEFS)

@APP.route('/admin/<admin_id>', methods=('GET', 'POST'))
def admin(admin_id):
    # TABLES[admin_id] = {'table_def': TABLE_DEFS[0], 'public_id': 'ABCDEF', 'visible_clips': [], 'display_all': False}
    if request.method == 'POST':
        if admin_id not in TABLES:  # => table creation
            if not request.form.get('table_def'):
                abort(422, 'Invalid form input: missing "table_def"')
            autocleanup()
            TABLES[admin_id] = {
                'table_def': TABLE_DEFS[int(request.form['table_def'])],
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
