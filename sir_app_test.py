#!/usr/bin/env python3
# coding: utf-8

import os
from jsonschema import validate

from sir_app import scene_def_from_image, SCENE_DEF_SCHEMA, SCENE_DEFS


def test_predefined_scenes_match_json_schema():
    for scene_def in SCENE_DEFS:
        validate(instance=scene_def, schema=SCENE_DEF_SCHEMA)

def test_scene_def_from_image():
    image_url = 'file://' + os.path.abspath('EnqueteAuVillage.jpg')
    scene_def = scene_def_from_image(image_url, clip_width=525, clip_height=441)
    assert scene_def == {
        'name': 'EnqueteAuVillage',
        'img': { 'url': image_url, 'width': 1575, 'height': 881 },
        'clips': [
            {'type': 'rect', 'x': 0, 'y': 0, 'width': 525, 'height': 441},
            {'type': 'rect', 'x': 0, 'y': 441, 'width': 525, 'height': 440},
            {'type': 'rect', 'x': 525, 'y': 0, 'width': 525, 'height': 441},
            {'type': 'rect', 'x': 525, 'y': 441, 'width': 525, 'height': 440},
            {'type': 'rect', 'x': 1050, 'y': 0, 'width': 525, 'height': 441},
            {'type': 'rect', 'x': 1050, 'y': 441, 'width': 525, 'height': 440}
    ]}
    validate(instance=scene_def, schema=SCENE_DEF_SCHEMA)
