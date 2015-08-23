import os

import matplotlib.pyplot as plt
import geopandas as gpd

import mplleaflet

# Download a file from: http://water.weather.gov/precip/download.php
# and change the path below
filename = os.path.join(os.path.dirname(__file__),
                        'data',
                        'nws_precip_year2date_observed_shape_20140406',
                        'nws_precip_year2date_observed_20140406.shp')
df = gpd.read_file(filename)

# Negative values are missing data so just drop them
df.rename(columns=lambda x: x.lower(), inplace=True)
df = df[df['globvalue'] > 0]

# Setting the index, then calling unstack() creates the matrix of values 
# indexed by Hrapx in the columns, Hrapy in the rows. Try to do that in
# MATLAB!
df.set_index(['hrapy', 'hrapx'], inplace=True)
df = df.unstack()

# Sorting the values here is unnecessary, but do it just in case
df.sort_index(axis=0, inplace=True)
df.sort_index(axis=1, inplace=True)

g = df['globvalue']
plt.contour(4762.5 * (g.columns.values - 401), 
            4762.5 * (g.index.values - 1601), g)

# See http://www.nws.noaa.gov/oh/hrl/distmodel/hrap.htm
# Note: The Proj.4 CRS definition below is gleaned from reading the NWS and
# Proj.4 docs. Reach out if it's not correct although the resulting map looks
# right.
crs = {'lon_0': -105.0,
       'lat_ts': 60.0,
       'R': 6371200,
       'proj': 'stere',
       'units': 'm',
       'lat_0': 90.0}

root, ext = os.path.splitext(__file__)
mapfile = root  + '.html'
mplleaflet.show(crs=crs, path=mapfile, tiles='mapbox bright')
