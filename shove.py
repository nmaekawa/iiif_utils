#!/usr/bin/env python

import contextlib
import json
import sys

from elasticsearch5 import Elasticsearch

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

    es = Elasticsearch(
        ['localhost'],
        http_auth=('elastic', 'changeme'))
    all_manifests = json.loads(content)
    print('---- starting! ----')

    for mani in all_manifests['hits']['hits']:
        es.index(
            index='manifests',
            doc_type=mani['_type'],
            id=mani['_id'],
            body=mani['_source'])
        print('{} : {}'.format(mani['_type'], mani['_id']))

    print('---- finished! ----')
