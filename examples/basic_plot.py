import json
import os

import matplotlib.pyplot as plt
import numpy as np

import mplleaflet

# Load up the geojson data
filename = os.path.join(os.path.dirname(__file__), 'data', 'track.geojson')
with open(filename) as f:
    gj = json.load(f)

# Grab the coordinates (longitude, latitude) from the features, which we
# know are Points
xy = np.array([feat['geometry']['coordinates'] for feat in gj['features'][::10]])

# Plot the path as red dots connected by a blue line
plt.hold(True)
plt.plot(xy[:,0], xy[:,1], 'r.')
plt.plot(xy[:,0], xy[:,1], 'b')

root, ext = os.path.splitext(__file__)
mapfile = root  + '.html'
# Create the map. Save the file to basic_plot.html. _map.html is the default
# if 'path' is not specified
mplleaflet.show(path=mapfile)
