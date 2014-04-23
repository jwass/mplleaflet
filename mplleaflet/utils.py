"""Utility Routines"""
import warnings

import numpy as np
from matplotlib.path import Path

PATH_DICT = {Path.LINETO: 'L',
             Path.MOVETO: 'M',
             Path.STOP: 'STOP',
             Path.CURVE3: 'S',
             Path.CURVE4: 'C',
             Path.CLOSEPOLY: 'Z'}


def eval_bezier(p, n=5):
    # Get t as [n x 2] array
    t = np.tile(np.linspace(0, 1, n).reshape((n,1)), (1, 2))
    t2 = t*t
    mt = 1-t
    mt2 = mt*mt

    if len(p) == 3:  # Quadratic
        x = mt2*p[0,:] + 2*mt*t*p[1,:] + t2*p[2,:]
    elif len(p) == 4:  # Cubic
        mt3 = mt2*mt
        t3 = t2*t
        x = mt3*p[0,:] + 3*mt2*t*p[1,:] + 3*mt*t2*p[2,:] + t3*p[3,:]
    else:
        raise ValueError('Bezier curves can only be quadratic or cubic.')

    return x

def derive_coords(data, pathcodes):
    coords = list(iter_rings(path))

    if transform:
        coords = [transform(c) for c in coords]

    if len(coords) > 1:  # Definitely a polygon!
        geomtype = Polygon
    else:  # Try to figure out if LineString or Polygon
        pc = list(path.iter_segments(simplify=False))
        paths, codes = zip(*pc)

        # If there's a close polygon in the paths then it's definitely a 
        # polygon. If there are more than one moveto command, then it's also
        # a polygon (that's how descartes puts in interior polygons)
        if (any(c == Path.CLOSEPOLY for c in codes) or
            sum(int(c == Path.MOVETO) for c in codes) > 1):
            geomtype = Polygon
        else:
            geomtype = LineString
            coords = coords[0]

    geom = geomtype(coords)
    return geom

def iter_rings(data, pathcodes):
    ring = []
    # Do this smartly by finding when pathcodes changes value
    # and do smart indexing on data
    for point, code in zip(data, pathcodes):
        if code == 'M':
            # Emit the path and start a new one
            if len(ring):
                yield ring
            ring = [point]
        elif code == 'L':
            ring.append(point)
        elif code == Path.CURVE3 or code == Path.CURVE4:
            warnings.warn('Quadratic/Cubic beziers not implemented')
        else:
            raise ValueError('Unrecognized code: {}'.format(code))

    if len(ring):
        yield ring
