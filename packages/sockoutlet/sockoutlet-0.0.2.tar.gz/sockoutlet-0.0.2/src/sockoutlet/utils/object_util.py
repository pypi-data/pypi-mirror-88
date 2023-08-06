#!/usr/bin/env python3

import datetime
import json

def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    return o

def json_dumps(obj, indent=None):
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, default = json_converter, ensure_ascii=False, indent=indent)

def json_loads(data):
    if not isinstance(data, str):
        return data, None
    try:
        json_dict = json.loads(data)
        return json_dict, None
    except Exception as exception:
        return None, exception
