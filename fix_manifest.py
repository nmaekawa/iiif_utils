#!/usr/bin/env python

from iiif_prezi.loader import ManifestReader

import contextlib
import json
import sys

VERBOSE = True
VERSION = '2.0'
LOGO_URI = 'https://devo.images.harvardx.harvard.edu/iiif/harvard_logo.tif/full/full/0/default.jpg'
MANIFEST_CONTEXT = {
    '1.0': 'http://www.shared-canvas.org/ns/context.json',
    '2.0': 'http://iiif.io/api/presentation/2/context.json',
    '2.1': 'http://iiif.io/api/presentation/2/context.json',
}

# from http://stackoverflow.com/a/29824059
@contextlib.contextmanager
def _smart_open(filename, mode='Ur'):
    if filename == '-':
        if mode is None or mode == '' or 'r' in mode:
            fh = sys.stdin
        else:
            fh = sys.stdout
    else:
        fh = open(filename, mode)

    try:
        yield fh
    finally:
        if filename is not '-':
            fh.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '-'

    with _smart_open(args) as handle:
        content = handle.read()

    # shoving these to fix stuff
    json_manifest = json.loads(content)
    json_manifest['logo'] = LOGO_URI
    json_manifest.update({'@context': MANIFEST_CONTEXT[VERSION]})
    print(json.dumps(json_manifest))

