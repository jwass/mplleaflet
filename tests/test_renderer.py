# Compatibility for 2.6
import sys
if sys.version_info[:2] == (2, 6):
    try:
        import unittest2 as unittest
    except ImportError:
        import unittest
else:
    import unittest

import matplotlib
# So testing can work on Travis too
matplotlib.use('agg', warn=False)

import matplotlib.pyplot as plt
import numpy as np

import mplleaflet

class BaseTestCase(unittest.TestCase):
    def assertFeaturesEqual(self, expected, msg=None, fig=None, **kwargs):
        if fig is None:
            fig = plt.gcf()
        result = mplleaflet.fig_to_geojson(fig, **kwargs)

        self.assertEqual(result['type'], 'FeatureCollection')
        self.assertEqual(len(result['features']), len(expected['features']))

        # Match expected features to output. Order doesn't matter
        # so we have to search the output for matching features
        for i, ef in enumerate(expected['features']):
            egeom = ef['geometry']
            for j, rf in enumerate(result['features']):
                rgeom = rf['geometry']
                if (self.geom_equal(egeom, rgeom) and
                   self.props_equal(ef['properties'], rf['properties'])):
                        break
            else:
                # Get here if we never break
                self.fail("Feature at index not found: {} {}\nin {}".format(
                    i, ef, rf))

            # Once we find a match in the result features, remove it from
            # the list so it can't be matched to another expected feature
            # Also makes the double-for loop a little faster
            del result['features'][j]

    def geom_equal(self, first, second):
        # mplleaflet won't output Mult* geom types
        eq = ((first['type'] == second['type']) and
              np.allclose(first['coordinates'], second['coordinates']))

        return eq

    def props_equal(self, first, second):
        return first == second

    def setUp(self):
        self.coords = np.array([[1, 4], [2, 5], [3, 2]], dtype='float')

    def tearDown(self):
        plt.close()

    def test_one_line(self):
        color = '#123ABC'
        plt.plot(self.coords[:, 0], self.coords[:, 1], color=color)
        expected = fc([
            feat('LineString', self.coords.tolist(),
                 {'color': color, 'opacity': 1, 'weight': 1.0}),
        ])
        self.assertFeaturesEqual(expected)

    def test_multiple_lines(self):
        color1 = '#123ABC'
        color2 = '#456DEF'

        coords1 = self.coords
        coords2 = self.coords + [100, 5]

        plt.hold(True)
        plt.plot(coords1[:, 0], coords1[:, 1], color=color1, alpha=0.6)
        plt.plot(coords2[:, 0], coords2[:, 1], color=color2, linewidth=4.5)
        expected = fc([
            feat('LineString', coords1.tolist(),
                 {'color': color1, 'opacity': 0.6, 'weight': 1.0}),
            feat('LineString', coords2.tolist(),
                 {'color': color2, 'opacity': 1, 'weight': 4.5})
        ])
        self.assertFeaturesEqual(expected)

    def test_line_dash(self):
        color = '#123ABC'
        dashes = [10, 5, 3, 8]
        plt.plot(self.coords[:, 0], self.coords[:, 1],
                 color=color, dashes=dashes)
        expected = fc([
            feat('LineString', self.coords.tolist(),
                {'color': color, 'opacity': 1, 'weight': 1.0,
                 'dashArray': ','.join(str(int(v)) for v in dashes)}),
        ])
        self.assertFeaturesEqual(expected)

    def test_text(self):
        # Test that text doesn't crash
        color = '#0000FF'

        plt.hold(True)
        plt.plot(self.coords[:, 0], self.coords[:, 1], color=color)
        plt.text(4, 4, 'mplleaflet')
        expected = fc([
            feat('LineString', self.coords.tolist(),
                 {'color': color, 'opacity': 1, 'weight': 1.0}),
        ])
        self.assertFeaturesEqual(expected)


def feat(gtype, coordinates, properties=None):
    if properties is None:
        properties = {}

    return {
        'type': 'Feature',
        'geometry': {
            'type': gtype,
            'coordinates': coordinates,
        },
        'properties': properties,
    }


def fc(features):
    return {
        'type': 'FeatureCollection',
        'features': features,
    }
