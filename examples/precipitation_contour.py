import matplotlib.pyplot as plt
import geopandas as gpd

import mplleaflet

# http://water.weather.gov/precip/download.php
df = gpd.read_file('/Users/jwass/Downloads/nws_precip_year2date_observed_shape_20140406/nws_precip_year2date_observed_20140406.shp')

# Negative values are missing data so just drop them
df = df[df['Globvalue'] > 0]

# See http://www.nws.noaa.gov/oh/hrl/distmodel/hrap.htm
# I'd love to hear from properly trained GIS professionals whether the
# following CRS is correct for the NWS data.
crs = {'lon_0': -105.0,
       'lat_ts': 60.0,
       'R': 6371200,
       'proj': 'stere',
       'units': 'm',
       'lat_0': 90.0}

# Setting the index, then calling unstack() creates the matrix of values 
# indexed by Hrapx in the columns, Hrapy in the rows.
df.set_index(['Hrapy', 'Hrapx'], inplace=True)
df = df.unstack()

# Sorting the values here is unnecessary, but do it just in case
df.sort_index(axis=0, inplace=True)
df.sort_index(axis=1, inplace=True)

g = df['Globvalue']
plt.contour(4762.5 * (g.columns.values - 401), 
            4762.5 * (g.index.values - 1601), g)

mplleaflet.save_html(plt.gcf(), '_map.html', crs=crs)
