from __future__ import absolute_import

from functools import partial

from jinja2 import Template
from .mplexporter.renderers.base import Renderer
import numpy as np

from .utils import iter_rings


svg_template = Template("""<svg width="{{ width|int }}px" height="{{ height|int }}px" viewBox="{{ minx }} {{ miny }} {{ width }} {{ height }}" xmlns="http://www.w3.org/2000/svg" version="1.1">  <path d="{{ path }}" {% for k, v in style.items() %}{{ k }}="{{ v }}" {% endfor %}/></svg>""")

_marker_inflation = 1.25

class LeafletRenderer(Renderer):
    def __init__(self, crs=None, epsg=None):
        if crs is not None and epsg is not None:
            raise ValueError('crs and epsg cannot both be specified')

        if epsg is not None:
            crs = _crs_from_epsg(epsg)
        if crs is not None:
            import pyproj
            crs_out = _crs_from_epsg(4326)
            proj_in = pyproj.Proj(preserve_units=True, **crs)
            proj_out = pyproj.Proj(preserve_units=True, **crs_out)
            self.transformfunc = partial(pyproj.transform, proj_in, proj_out)
        else:
            self.transformfunc = None

        self._features = []


    def geojson(self):
        fc = {
            "type": "FeatureCollection",
            "features": self._features,
        }
        return fc


    def _convert_style(self, style):
        leaflet_style = {
            'color': style['edgecolor'],
            'weight': style['edgewidth'],
            'opacity': style['alpha'],
        }
        if style['facecolor'] != 'none':
            leaflet_style['fillColor'] = style['facecolor']
        if style['dasharray'] != 'none':
            leaflet_style['dashArray'] = style['dasharray']

        return leaflet_style

    def _convert_style_svg(self, style):
        svg_style = {
            'stroke': style['edgecolor'],
            'stroke-width': style['edgewidth'],
            'stroke-opacity': style['alpha'],
        }
        if style['facecolor'] != 'none':
            svg_style['fill'] = style['facecolor']
            svg_style['fill-opacity'] = style['alpha']

        return svg_style

    def _svg_path(self, pathcodes, data):
        """ 
        Return the SVG path's 'd' element.
    
        """
        def gen_path_elements(pathcodes, data):
            counts = {'M': 1, 'L': 1, 'C': 3, 'Z': 0}
            it = iter(data)
            for code in pathcodes:
                yield code
                for _ in range(counts[code]):
                    p = next(it)
                    yield str(p[0])
                    yield str(p[1])

        return ' '.join(gen_path_elements(pathcodes, data))


    def draw_path(self, data, coordinates, pathcodes, style,
                  offset=None, offset_coordinates="data", mplobj=None):
        properties = self._convert_style(style)
        if coordinates == 'points' or coordinates == 'display':
            # Flip the points about y-axis to align with SVG coordinate
            # system.
            path_points = data.copy()
            path_points[:,1] *= -1
            if offset_coordinates != 'data':
                pass  # Don't know how to work with this yet
            if self.transformfunc:
                coords = self.transformfunc(*offset)
            else:
                coords = list(offset)
            geometry_type = 'Point'

            # Find the size of the path, and increase by inflation
            mx = np.max(path_points, axis=0)
            mn = np.min(path_points, axis=0)

            center = mn + (mx - mn) / 2.0
            size = np.ceil(_marker_inflation * (mx - mn))
            corner = center - size / 2.0
            svg = svg_template.render(
                path=self._svg_path(pathcodes, path_points),
                style=self._convert_style_svg(style),
                width=size[0],
                height=size[1],
                minx=corner[0],
                miny=corner[1],
            )
            properties = {'html': svg,
                          'anchor_x': -corner[0],
                          'anchor_y': -corner[1]}
        else:
            if self.transformfunc:
                data = [self.transformfunc(*c) for c in data]
            else:
                data = [c.tolist() for c in data]
            rings = list(iter_rings(data, pathcodes))

            if style['facecolor'] != 'none':
                # It's a polygon
                geometry_type = 'Polygon'
                coords = rings
            else:
                geometry_type = 'LineString'
                coords = rings[0]

        feature = {
            "type": "Feature",
            "geometry": {
                "type": geometry_type,
                "coordinates": coords,
            },
            "properties": properties
        }

        self._features.append(feature)

    def draw_text(self, *args, **kwargs):
        """ Don't draw the text for now, but don't crash """
        pass


def _crs_from_epsg(epsg):
    epsgstr = 'epsg:{}'.format(epsg)
    crs = {'init': epsgstr, 'no_defs': True}
    return crs
