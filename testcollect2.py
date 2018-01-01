#!/usr/bin/env python
from __future__ import print_function
from math import log, tan, pi
from itertools import product
from argparse import ArgumentParser
from os.path import join, splitext
import ntpath
import tempfile, shutil, urllib, io, sys, os, subprocess
import unittest

import multiprocessing
import time

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

def tiles(zoom, lat1, lon1, lat2, lon2):
    ''' Convert geographic bounds into a list of tile coordinates at given zoom.
    '''
    # convert to geographic bounding box
    minlat, minlon = min(lat1, lat2), min(lon1, lon2)
    maxlat, maxlon = max(lat1, lat2), max(lon1, lon2)

    # convert to tile-space bounding box
    _, xmin, ymin = mercator(maxlat, minlon, zoom)
    _, xmax, ymax = mercator(minlat, maxlon, zoom)

    # generate a list of tiles
    xs, ys = range(xmin, xmax+1), range(ymin, ymax+1)
    tiles = [(zoom, x, y) for (y, x) in product(ys, xs)]

    return tiles

def getTile(tile):
    # print('gettile:', tile)
    z, x, y = tile
    # print('z, x, y:', z, x, y)
    output_path = args.output_path
    api_key = args.mapzen_api_key
    if os.path.isfile(join(output_path, '{}-{}-{}.png'.format(z, x, y))):
        print('exists, skipping:', join(output_path, '{}-{}-{}.png'.format(z, x, y)))
    else:
        response = urllib.urlopen(tile_url.format(z=z, x=x, y=y, k=api_key))
        if response.getcode() != 200:
            # raise RuntimeError('No such tile: {}'.format((z, x, y)))
            print('RuntimeError: {}'.format((z, x, y)))
            print(response.getcode())
            # print('RuntimeError: No such tile: {}'.format((z, x, y)))
        # if verbose:
            # print('Downloaded', response.url, file=sys.stderr)

        with io.open(join(tempdir, '{}-{}-{}.png'.format(z, x, y)), 'wb') as file:
            # print('file:', file)
            file.write(response.read())
            # files.append(file.name)
            print(ntpath.basename(file.name))
            return file.name


def download(output_path, tiles, api_key, verbose=True):
    # print(tiles)
    ''' Download list of tiles to a temporary directory and return its name.
    '''
    _, ext = splitext(output_path)

    # if the extension is one of these strings, merge_geotiff = true
    merge_geotiff = bool(ext.lower() in ('.tif', '.tiff', '.geotiff'))

    try:
        try:
            pool = multiprocessing.Pool(processes=10) # how much parallelism?
            pool.map(getTile, tiles)

        except RuntimeError as err:
            print("RuntimeError: "+str(err))
            sys.exit(0)

        if merge_geotiff:
            if verbose:
                print('Combining', len(files), 'into', output_path, '...', file=sys.stderr)
            temp_png = join(tempdir, 'temp.png')
            subprocess.check_call(['gdal_merge.py', '-o', temp_png] + files)
            shutil.move(temp_png, output_path)
        else:
            if verbose:
                print('Moving files in', tempdir, 'to', output_path, '...', file=sys.stderr)
            # shutil.move(dir, output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            files = os.listdir(tempdir)
            for f in files:
                try:
                    shutil.move(tempdir+'/'+f, output_path)
                except:
                    pass

    except IOError:
        raise IOError
    finally:
        if merge_geotiff:
            shutil.rmtree(dir)

def main(args):
    # four formats are available, let's use GeoTIFF
    tile_url = 'https://tile.mapzen.com/mapzen/terrain/v1/516/terrarium/{z}/{x}/{y}.png?api_key={k}'

    # default API key, please set your own
    # default_api_key = 'mapzen-SPsSJJY'
    tempdir = tempfile.mkdtemp(prefix='collected-')

    download(tile_url, args.output_path, tiles(args.zoom, *args.bounds), args.mapzen_api_key)

if __name__ == '__main__':

    args = parser.parse_args()

    if args.testing:
        import mock # To run tests, `pip install mock==2.0.0`
        suite = unittest.defaultTestLoader.loadTestsFromName(__name__)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        exit(0 if result.wasSuccessful() else 1)

    main(args)