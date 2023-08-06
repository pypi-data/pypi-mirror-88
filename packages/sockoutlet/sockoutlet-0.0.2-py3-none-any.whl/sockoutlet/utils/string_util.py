#!/usr/bin/env python3

import re

def stringToArray(labels):
    if isinstance(labels, str):
        return filter(lambda s: len(s) > 0, map(lambda s: s.strip(), re.split(r',', labels)))
    return []
