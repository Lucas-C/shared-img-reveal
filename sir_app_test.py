#!/usr/bin/env python3
# coding: utf-8

from jsonschema import validate

from sir_app import SCENE_DEF_SCHEMA, SCENE_DEFS


def test_predefined_scenes_match_json_schema():
    for scene_def in SCENE_DEFS:
        validate(instance=scene_def, schema=SCENE_DEF_SCHEMA)
