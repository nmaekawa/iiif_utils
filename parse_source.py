#!/usr/bin/env python

import contextlib
import json
import os
import sys


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


output_dir = './manifest'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '-'

    with _smart_open(args) as handle:
        content = handle.read()

    all_manifests = json.loads(content)
    for mani in all_manifests['hits']['hits']:
        try:
            os.makedirs('{}/{}'.format(output_dir, mani['_type']))
        except OSError as e:
            if ('File exists' in str(e)):
                pass
            else:
                raise

        manifest_id = '{}/{}/{}.json'.format(output_dir, mani['_type'], mani['_id'])
        with open(manifest_id, 'w+') as f:
            f.write(json.dumps(mani['_source'], indent=4))

        print('{}'.format(manifest_id))

