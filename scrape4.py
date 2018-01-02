#!/usr/bin/env python
from __future__ import print_function
from math import log, tan, pi
from itertools import product
from argparse import ArgumentParser
from os.path import join, splitext

import tempfile, shutil, urllib, io, sys, os, subprocess
import unittest

# four formats are available, let's use GeoTIFF
tile_url = 'https://tile.mapzen.com/mapzen/terrain/v1/516/terrarium/{z}/{x}/{y}.png?api_key={k}'

# default API key, please set your own
default_api_key = 'mapzen-SPsSJJY'

def mercator(lat, lon, zoom):
    ''' Convert latitude, longitude to z/x/y tile coordinate at given zoom.
    '''
    # convert to radians
    x1, y1 = lon * pi/180, lat * pi/180

    # project to mercator
    x2, y2 = x1, log(tan(0.25 * pi + 0.5 * y1))

    # transform to tile space
    tiles, diameter = 2 ** zoom, 2 * pi
    x3, y3 = int(tiles * (x2 + pi) / diameter), int(tiles * (pi - y2) / diameter)

    return zoom, x3, y3

def tiles(zoom):
    ''' Convert geographic bounds into a list of tile coordinates at given zoom.
    '''
    # generate a list of tiles
    xs, ys = range(0, pow(2, zoom)), range(0, pow(2, zoom))
    tiles = [(zoom, x, y) for (y, x) in product(ys, xs)]

    return tiles

def download(output_path, tiles, api_key, verbose=True):
    ''' Download list of tiles to a temporary directory and return its name.
    '''
    dir = tempfile.mkdtemp(prefix='collected-')
    _, ext = splitext(output_path)


    try:
        files = []

        for (z, x, y) in tiles:
            response = urllib.urlopen(tile_url.format(z=z, x=x, y=y, k=api_key))
            if response.getcode() != 200:
                raise RuntimeError('No such tile: {}'.format((z, x, y)))
            if verbose:
                print('Downloaded', response.url, file=sys.stderr)

            with io.open(join(dir, '{}-{}-{}.png'.format(z, x, y)), 'wb') as file:
                file.write(response.read())
                files.append(file.name)

        if merge_geotiff:
            if verbose:
                print('Combining', len(files), 'into', output_path, '...', file=sys.stderr)
            temp_png = join(dir, 'temp.png')
            subprocess.check_call(['gdal_merge.py', '-o', temp_png] + files)
            shutil.move(temp_png, output_path)
        else:
            if verbose:
                print('Moving files in', dir, 'to', output_path, '...', file=sys.stderr)
            # shutil.move(dir, output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            files = os.listdir(dir)
            for f in files:
                try:
                    shutil.move(dir+'/'+f, output_path)
                except:
                    pass


    finally:
        if merge_geotiff:
            shutil.rmtree(dir)


parser = ArgumentParser(description='''Collect Mapzen elevation tiles into a
single GeoTIFF or directory. If output_path ends in ".tif", ".tiff", or
".geotiff", gdal_merge.py will be called to merge all downloaded tiles into a
single image. Otherwise, they are collected into the named directory.''')

parser.add_argument('--zoom', type=int, default=12,
                    help='Map zoom level given as integer. Defaults to 12.')

parser.add_argument('--mapzen_api_key', default=None, required=True,
                    help='Mapzen API key required to use the terrain tile service. See: https://mapzen.com/documentation/overview/#developer-accounts-and-api-keys.')

parser.add_argument('output_path', help='Output GeoTIFF filename or local directory name.')

if __name__ == '__main__':
    args = parser.parse_args()

    if args.testing:
        import mock # To run tests, `pip install mock==2.0.0`
        suite = unittest.defaultTestLoader.loadTestsFromName(__name__)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        exit(0 if result.wasSuccessful() else 1)

    download(args.output_path, tiles(args.zoom, *args.bounds), args.mapzen_api_key)