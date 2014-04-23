from functools import partial

from utils import iter_rings

from mplexporter.renderers.base import Renderer

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


    def draw_path(self, data, coordinates, pathcodes, style,
                  offset=None, offset_coordinates="data", mplobj=None):
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
            "properties": self._convert_style(style)
        }

        self._features.append(feature)


def _crs_from_epsg(epsg):
    epsgstr = 'epsg:{}'.format(epsg)
    crs = {'init': epsgstr, 'no_defs': True}
    return crs
