#!/usr/bin/env python

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

def get_images_list(jo):
    jo_images = []
    if isinstance(jo, dict):
        #print('************ keys is dict({})'.format(jo.keys()))
        for key in jo.keys():
            #print('************ key is({})'.format(key))
            if key == 'images':
                return jo[key]
            else:
                result =  get_images_list(jo[key])
                if result is not None:
                    jo_images += result

    elif isinstance(jo, list):
        for item in jo:
            result = get_images_list(item)
            if result is not None:
                jo_images += result

    if jo_images:
        return jo_images

    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '-'

    with _smart_open(args) as handle:
        content = handle.read()

    #print('------------------ 1')
    # load the json object
    json_manifest = json.loads(content)
    #print('------------------ 2')

    # visit nodes in json looking for "images" prop
    for key in json_manifest:
        jo_images = get_images_list(json_manifest[key])
        if jo_images is not None:
            #print("--------------- jo_images is not None: {}".format(json.dumps(jo_images)))
            for item in jo_images:  # images is a list
                if 'resource' in item:
                    if 'service' in item['resource']:
                        item['resource']['service']['@context'] = MANIFEST_CONTEXT['2.0']
                        continue

    print(json.dumps(json_manifest))








