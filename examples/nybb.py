import geopandas as gpd
import matplotlib.pyplot as plt
import mplleaflet

def main():
    df = gpd.read_file('/nybb_13a/nybb.shp',
            vfs='zip:///Users/jwass/projects/geopandas/examples/nybb_13a.zip')
    df.plot()
    mplleaflet.show(crs=df.crs)


if __name__ == '__main__':
    main()
