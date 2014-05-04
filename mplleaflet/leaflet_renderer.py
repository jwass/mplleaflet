from functools import partial

from jinja2 import Template
from mplexporter.renderers.base import Renderer
import numpy as np

from utils import iter_rings


svg_template = Template("""<svg width="{{ width }}px" height="{{ height }}px" viewBox="-{{ width / 2 }} -{{ height / 2 }} {{ width }} {{ height }}" xmlns="http://www.w3.org/2000/svg" version="1.1">  <path d="{{ path }}" {% for k, v in style.iteritems() %}{{ k }}="{{ v }}" {% endfor %}/></svg>""")

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
            'dashArray': style['dasharray'],
        }
        if style['facecolor'] != 'none':
            leaflet_style['fillColor'] = style['facecolor']

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
    
        Note that SVG's coordinate system is flipped about the 
        y-axis.
        """
        def gen_path_elements(pathcodes, data):
            counts = {'M': 1, 'L': 1, 'C': 3, 'Z': 0}
            it = iter(data)
            for code in pathcodes:
                yield code
                for _ in range(counts[code]):
                    p = it.next()
                    yield str(p[0])
                    yield str(-p[1])

        return ' '.join(gen_path_elements(pathcodes, data))


    def draw_path(self, data, coordinates, pathcodes, style,
                  offset=None, offset_coordinates="data", mplobj=None):
        properties = self._convert_style(style)
        if coordinates == 'points' or coordinates == 'display':
            path_points = data
            if offset_coordinates != 'data':
                pass  # Don't know how to work with this yet
            if self.transformfunc:
                coords = self.transformfunc(*offset)
            else:
                coords = list(offset)
            geometry_type = 'Point'

            # Find the size of the path, and increase 25%
            size = np.ceil(1.25 * np.ptp(path_points, axis=0))
            width = int(size[0])
            height = int(size[1])
            path = self._svg_path(pathcodes, path_points)
            svg_style = self._convert_style_svg(style)
            properties = {'html': svg_template.render(path=path, 
                                                      style=svg_style,
                                                      width=width,
                                                      height=height),
                          'width': width,
                          'height': height}
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


def _crs_from_epsg(epsg):
    epsgstr = 'epsg:{}'.format(epsg)
    crs = {'init': epsgstr, 'no_defs': True}
    return crs
