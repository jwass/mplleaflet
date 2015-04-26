import matplotlib.pyplot as plt
import mplleaflet

def test_basic():
    plt.plot([0, 0], [1, 1])
    mplleaflet.fig_to_geojson()


def test_scatter():
    plt.scatter([0, 10, 0, 10], [0, 0, 10, 10], c=[1, 2, 3, 4])
    mplleaflet.fig_to_geojson()
