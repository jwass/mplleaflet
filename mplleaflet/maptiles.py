osm = (
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'Map data (c) <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
)

mapquest_open = (
    'http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://open.mapquest.com/">MapQuest</a> Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'
)

mapbox_bright = (
    'http://{s}.tiles.mapbox.com/v3/mapbox.world-bright/{z}/{x}/{y}.png',
    'Map tiles by <a href="http://www.mapbox.com/m">Mapbox</a> Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'
)

tiles = {
    'osm': osm,
    'mapquest open': mapquest_open,
    'mapbox_bright': mapbox_bright,
}

_mb_url = 'http://{{s}}.tiles.mapbox.com/v3/{mapid}/{{z}}/{{x}}/{{y}}.png'
_mb_attribution = '<a href="https://www.mapbox.com/about/maps/">Terms & Feedback</a>'
def mapbox(mapid):
    url = _mb_url.format(mapid=mapid)
    return (url, _mb_attribution)

