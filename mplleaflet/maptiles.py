osm = (
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'Map data (c) <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
)

mapquest_open = (
    'https://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://open.mapquest.com/">MapQuest</a> Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'
)

mapbox_bright = (
    'https://{s}.tiles.mapbox.com/v3/mapbox.world-bright/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://www.mapbox.com/m">Mapbox</a> Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'
)

thunderforest_landscape = (
    'https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
     '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
)


esri_aerial = (
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png',
    'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
)

esri_natgeo = (
    'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}.png',
    'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC'
)

esri_worldtopo = (
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}.png',
    'Tiles &copy; Esri &mdash; Esri, HERE, DeLorme, Intermap, increment P Corp., GEBCO, USGS, FAO, NPS, NRCAN, GeoBase, IGN, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), swisstopo, MapmyIndia, &copy; OpenStreetMap contributors, GIS User Community'
)

stamen_wc = (
    'https://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
)

stamen_toner = (
    'https://a.tile.stamen.com/toner/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
)


cartodb_positron = (
    'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
)


tiles = {
    'osm': osm,
    'mapquest open': mapquest_open,
    'mapbox bright': mapbox_bright,
    'thunderforest_landscape': thunderforest_landscape,
    'esri_aerial': esri_aerial,
    'stamen_wc': stamen_wc,
    'stamen_toner': stamen_toner,
    'esri_natgeo': esri_natgeo,
    'cartodb_positron': cartodb_positron,
    'esri_worldtopo': esri_worldtopo
}

_mb_url = 'https://{{s}}.tiles.mapbox.com/v3/{mapid}/{{z}}/{{x}}/{{y}}.png'
_mb_attribution = '<a href="https://www.mapbox.com/about/maps/">Terms & Feedback</a>'
def mapbox(mapid):
    url = _mb_url.format(mapid=mapid)
    return (url, _mb_attribution)

