import json
import os

import matplotlib.pyplot as plt
from mplexporter.exporter import Exporter
from jinja2 import Environment, PackageLoader

from leaflet_renderer import LeafletRenderer
import maptiles

env = Environment(loader=PackageLoader('mplleaflet', 'templates'),
                  trim_blocks=True, lstrip_blocks=True)

def fig_to_html(fig=None, template='base.html', tiles=None, crs=None, 
                epsg=None):
    if tiles is None:
        tiles = maptiles.osm
    elif isinstance(tiles, basestring):
        if tiles not in maptiles.tiles:
            raise ValueError('Unknown tile source "{}"'.format(tiles))
        else:
            tiles = maptiles.tiles[tiles]

    template = env.get_template(template) 

    if fig is None:
        fig = plt.gcf()
    dpi = fig.get_dpi()

    renderer = LeafletRenderer(crs=crs, epsg=epsg)
    exporter = Exporter(renderer)
    exporter.run(fig)

    gjdata = json.dumps(renderer.geojson())
    params = {
        'geojson': gjdata,
        'width': fig.get_figwidth()*dpi,
        'height': fig.get_figheight()*dpi,
        'mapid': '0',
        'tile_url': tiles[0],
        'attribution': tiles[1],
    }
    html = template.render(params)

    return html


def fig_to_geojson(fig=None, **kwargs):
    """
    Returns a figure's GeoJSON representation as a dictionary

    """
    renderer = LeafletRenderer(**kwargs)
    exporter = Exporter(renderer)
    exporter.run(fig)

    return renderer.geojson()


def save_html(fig=None, fileobj='map.html', **kwargs):
    if isinstance(fileobj, str):
        fileobj = open(fileobj, 'w')
    if not hasattr(fileobj, 'write'):
        raise ValueError("fileobj should be a filename or a writable file")
    html = fig_to_html(fig, **kwargs)
    fileobj.write(html)
    fileobj.close()


def display(fig=None, closefig=True, **kwargs):
    from IPython.display import HTML
    if fig is None:
        fig = plt.gcf()
    if closefig:
        plt.close(fig)

    html = fig_to_html(fig, template="ipynb.html", **kwargs)
    return HTML(html)


def show(fig=None, path='_map.html', **kwargs):
    import webbrowser
    fullpath = os.path.abspath(path)
    with open(fullpath, 'w') as f:
        save_html(fig, fileobj=f, **kwargs)
    webbrowser.open('file://' + fullpath)
