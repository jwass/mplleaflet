osm = (
    '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'Map data (c) <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
)

mapquest_open = (
    '//otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://open.mapquest.com/">MapQuest</a> Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'
)

mapbox_bright = (
    '//{s}.tiles.mapbox.com/v3/mapbox.world-bright/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://www.mapbox.com/m">Mapbox</a> Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'
)

thunderforest_landscape = (
    '//{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
     '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
)


esri_aerial = (
    '//server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png',
    'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
)

esri_natgeo = (
    '//server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}.png',
    'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC'
)
stamen_wc = (
    '//{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
)

tiles = {
    'osm': osm,
    'mapquest open': mapquest_open,
    'mapbox bright': mapbox_bright,
    'thunderforest_landscape': thunderforest_landscape,
    'esri_aerial': esri_aerial,
    'stamen_wc': stamen_wc,
    'esri_natgeo': esri_natgeo,

}

_mb_url = '//{{s}}.tiles.mapbox.com/v3/{mapid}/{{z}}/{{x}}/{{y}}.png'
_mb_attribution = '<a href="https://www.mapbox.com/about/maps/">Terms & Feedback</a>'
def mapbox(mapid):
    url = _mb_url.format(mapid=mapid)
    return (url, _mb_attribution)

