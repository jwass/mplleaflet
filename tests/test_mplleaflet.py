import matplotlib.pyplot as plt
import numpy as np
import mplleaflet

def test_contourf():
    x = np.linspace(-10,10,101)
    y = np.linspace(-10,10,101)
    xx, yy = np.meshgrid(x,y)
    grid = np.sin(xx) + np.sin(yy)
    plt.contourf(xx, yy, grid)
    mplleaflet.fig_to_html()
 

def test_basic():
    plt.plot([0, 1], [0, 1])
    mplleaflet.fig_to_html()


def test_basic_tiles():
    plt.plot([0, 1], [0, 1])
    mplleaflet.fig_to_html(tiles='osm')


def test_scatter():
    plt.scatter([0, 10, 0, 10], [0, 0, 10, 10], c=[1, 2, 3, 4])
    mplleaflet.fig_to_html()
