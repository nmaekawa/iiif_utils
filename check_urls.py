#!/usr/bin/env python

import contextlib
import json
from urllib.parse import urljoin
import sys

import requests


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



def returned_image(url):
    iiif_url = urljoin(url, '/full/32/0/default.jpg')
    r = requests.get(iiif_url)
    if r.status_code == requests.codes.ok:
        if r.headers['content-type'].lower().startswith('image'):
            if r.headers['content-length'] > 0:
                return True
    return False



if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        print('missing filename')
        exit(1)

    with open(args, 'r') as handle:
        for line in handle:
            iiif_url = line.strip() + '/full/32,/0/default.jpg'
            r = requests.get(iiif_url)

            if r.status_code == requests.codes.ok:
                if r.headers['content-type'].lower().startswith('image'):
                    if int(r.headers['content-length']) > 0:
                        msg = '   {} - {} - {} - [{}]'.format(
                            r.status_code, r.headers['content-type'],
                            r.headers['content-length'], iiif_url)

                        print(msg)
                        continue

            msg = '** {} - {} - {} - [{}]'.format(
                r.status_code, r.headers.get('content-type','none'),
                r.headers.get('content-length', 'none'), iiif_url)
            print(msg)

        handle.close()



