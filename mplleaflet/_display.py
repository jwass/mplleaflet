from __future__ import absolute_import

import json
import os
import uuid

import six

import matplotlib.pyplot as plt
from .mplexporter.exporter import Exporter
from jinja2 import Environment, PackageLoader

from .leaflet_renderer import LeafletRenderer
from .links import JavascriptLink, CssLink
from . import maptiles

# We download explicitely the CSS and the JS
_leaflet_js = JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js')
_leaflet_css = CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css')
_attribution = '<a href="https://github.com/jwass/mplleaflet">mplleaflet</a>'

env = Environment(loader=PackageLoader('mplleaflet', 'templates'),
                  trim_blocks=True, lstrip_blocks=True)

def fig_to_html(fig=None, template='base.html', tiles=None, crs=None,
                epsg=None, embed_links=False):
    """
    Convert a Matplotlib Figure to a Leaflet map

    Parameters
    ----------
    fig : figure, default gcf()
        Figure used to convert to map
    template : string, default 'base.html'
        The Jinja2 template to use
    tiles : string or tuple
        The tiles argument is used to control the map tile source in the
        Leaflet map. Several simple shortcuts exist: 'osm', 'mapquest open',
        and 'mapbox bright' may be specified to use those tiles.

        The argument may be a tuple of two elements. The first element is the
        tile URL to use in the map's TileLayer, the second argument is the
        attribution to display.  See
        http://leafletjs.com/reference.html#tilelayer for more information on
        formatting the URL.

        See also maptiles.mapbox() for specifying Mapbox tiles based on a
        Mapbox map ID.
    crs : dict, default assumes lon/lat
        pyproj definition of the current figure. If None, then it is assumed
        the plot is longitude, latitude in X, Y.
    epsg : int, default 4326
        The EPSG code of the current plot. This can be used in place of the
        'crs' parameter.
    embed_links : bool, default False
        Whether external links (except tiles) shall be explicitely embedded in the final html.

    Note: only one of 'crs' or 'epsg' may be specified. Both may be None, in
    which case the plot is assumed to be longitude / latitude.

    Returns
    -------
    String of html of the resulting webpage

    """
    if tiles is None:
        tiles = maptiles.osm
    elif isinstance(tiles, six.string_types):
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

    attribution = _attribution + ' | ' + tiles[1]

    mapid = str(uuid.uuid4()).replace('-', '')

    gjdata = json.dumps(renderer.geojson())
    params = {
        'geojson': gjdata,
        'width': fig.get_figwidth()*dpi,
        'height': fig.get_figheight()*dpi,
        'mapid': mapid,
        'tile_url': tiles[0],
        'attribution': attribution,
        'links': [_leaflet_js,_leaflet_css],
        'embed_links': embed_links,
    }
    html = template.render(params)

    return html


def fig_to_geojson(fig=None, **kwargs):
    """
    Returns a figure's GeoJSON representation as a dictionary

    All arguments passed to fig_to_html()

    Returns
    -------
    GeoJSON dictionary

    """
    if fig is None:
        fig = plt.gcf()
    renderer = LeafletRenderer(**kwargs)
    exporter = Exporter(renderer)
    exporter.run(fig)

    return renderer.geojson()


def save_html(fig=None, fileobj='_map.html', **kwargs):
    if isinstance(fileobj, str):
        fileobj = open(fileobj, 'w')
    if not hasattr(fileobj, 'write'):
        raise ValueError("fileobj should be a filename or a writable file")
    html = fig_to_html(fig, **kwargs)
    fileobj.write(html)
    fileobj.close()


def display(fig=None, figsize=None, closefig=True, **kwargs):
    """
    Convert a Matplotlib Figure to a Leaflet map. Embed in IPython notebook.

    Parameters
    ----------
    fig : figure, default gcf()
        Figure used to convert to map
    figsize : tuple of (width,height) or string, default (None,None)
        The width and height of the putput figure.
        * If string is provided, then (figsize,None) is used
        * If width is None, the figure size is used
        * If height is None, it is computed from width and the figure aspect ratio.
        Note that you can specify width and height in percent ("**%")
        in pixel ("**px") or in inches (int).
    closefig : boolean, default True
        Close the current Figure
    """
    from IPython.display import HTML

    if figsize is None:
        figsize=(None,None)
    elif not isinstance(figsize,tuple):
        figsize=(figsize,None)

    if fig is None:
        fig = plt.gcf()
    if closefig:
        plt.close(fig)

    if figsize[0]:
        if isinstance(figsize[0],int):
            width = figsize[0]*60
        else:
            width = figsize[0]
    else:
        width = int(60.*fig.get_figwidth())

    if figsize[1]:
        if isinstance(figsize[1],int):
            height = figsize[1]*60
        else:
            height = figsize[1]
    elif str(width).endswith('px'):
        height = int(float(str(width).replace('px',''))*fig.get_figheight()/fig.get_figwidth())
    elif str(width).endswith('%'):
        height = int(float(str(width).replace('%',''))*fig.get_figheight()/fig.get_figwidth()*0.01*17*60)
    else:
        try:
            height=int(float(str(width))*fig.get_figheight()/fig.get_figwidth())
        except:
            height=400

    html = fig_to_html(fig, **kwargs)

    # We embed everything in an iframe.
    iframe_html = '<iframe src="data:text/html;base64,{html}" width="{width}" height="{height}"></iframe>'\
    .format(html = html.encode('base64'),
            width = width,
            height= height,
           )
    return HTML(iframe_html)

def show(fig=None, path='_map.html', **kwargs):
    """
    Convert a Matplotlib Figure to a Leaflet map. Open in a browser

    Parameters
    ----------
    fig : figure, default gcf()
        Figure used to convert to map
    path : string, default '_map.html'
        Filename where output html will be saved

    See fig_to_html() for description of keyword args.

    """
    import webbrowser
    fullpath = os.path.abspath(path)
    with open(fullpath, 'w') as f:
        save_html(fig, fileobj=f, **kwargs)
    webbrowser.open('file://' + fullpath)
