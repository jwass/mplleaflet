mplleaflet
==========
mplleaflet turns [matplotlib](http://matplotlib.org) plots into a webpage
containing a [Leaflet](http://leafletjs.com) map that can be zoomed and
panned. mplleaflet can also embed the Leaflet map in an IPython notebook.

The goal of mplleaflet is to allow all matplotlib plotting commands to be
converted to Leaflet. You can use plot() with normal styling options,
contour(), quiver(), etc.

Internally mplleaflet uses [mplexporter](https://github.com/mpld3/mplexporter)
to walk matplotlib figures.

Why mplleaflet?
---------------
Other Python libraries, [basemap](http://matplotlib.org/basemap/) and
[folium](https://github.com/wrobstory/folium), exist to create maps with
either matplotlib or Leaflet. However these generally require learning a new
API for plotting data or the user is required to set up and generate all the
background data plotted on the map.

Examples
--------
The examples

* [Plot New York City boroughs in IPython
  notebook](http://nbviewer.ipython.org/github/jwass/mplleaflet/blob/master/examples/NYC%20Boroughs.ipynb)

Dependencies
------------
Required
* [mplexporter](https://github.com/mpld3/mplexporter)
* [jinja2](http://jinja.pocoo.org/)

Optional: Used by a few examples
* [GeoPandas](https://github.com/kjordahl/geopandas)
