import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pyproj

import mplleaflet

# Load up the geojson data
filename = os.path.join(os.path.dirname(__file__), 'data', 'track.geojson')
with open(filename) as f:
    gj = json.load(f)
features = [feat for feat in gj['features'][::10]]

xy = np.array([feat['geometry']['coordinates'] for feat in features])

# Transform the data to EPSG:26986 (Mass. state plane)
proj_in = pyproj.Proj(preserve_units=True, init='epsg:4326', no_defs=True)
crs_out = {'init': 'epsg:26986', 'no_defs': True}
proj_out = pyproj.Proj(preserve_units=True, **crs_out)
xy = np.array([pyproj.transform(proj_in, proj_out, c[0], c[1]) for c in xy])

# Grab the speed (m/s)
speed = np.array([feat['properties']['speed'] for feat in features])

# Grab the course. Course is 0 degrees due North, increasing clockwise
course = np.array([feat['properties']['course'] for feat in features])
angle = np.deg2rad(-course + 90)  # Convert to angle in xy plane

# Normalize the speed to use as the length of the arrows
r = speed / max(speed)
uv = r[:, np.newaxis] * np.column_stack([np.cos(angle), np.sin(angle)])

# For each point, plot an arrow pointing in the direction of the iPhone's
# course estimate. The arrow length is proportional to the phone's speed
# estimate. For a bigger effect, color each other based on its speed
plt.quiver(xy[:,0], xy[:,1], uv[:,0], uv[:,1], speed)

root, ext = os.path.splitext(__file__)
mapfile = root  + '.html'
# Create the map
mplleaflet.show(path=mapfile, crs=crs_out, tiles=mplleaflet.maptiles.mapbox('jwass.gnj4hje6'))
