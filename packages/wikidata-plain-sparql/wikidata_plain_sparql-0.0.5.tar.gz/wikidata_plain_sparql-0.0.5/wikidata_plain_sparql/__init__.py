import pandas as pd
import requests
import json
import re
import math

from bokeh.plotting import figure, ColumnDataSource, show, output_notebook
from bokeh.models import HoverTool, BoxZoomTool, WheelZoomTool
from bokeh.tile_providers import CARTODBPOSITRON, get_provider

def query(query, view=None):
    data = __load_from_api(query)
    if view == 'map':
        return __render_map(data)
    return __json_to_df(data)

def __render_map(data):
    columns = data['head']['vars']

    lat = []
    lon = []
    info = {}

    for column in columns:
        info['info_' + column] = []

    k = 6378137
    lon_ratio = k * math.pi / 180.0
    lat_ratio = math.pi / 360.0

    for result in data['results']['bindings']:
        for column in columns:
            popupText = ''
            if column in result:
                if 'datatype' in result[column] and result[column]['datatype'] == 'http://www.opengis.net/ont/geosparql#wktLiteral':
                    pointStr = result[column]['value']
                    coordStr = re.search('^Point\((.*)\)$', pointStr)
                    if coordStr:
                        coordsLatLong = coordStr[1].split(' ')
                        latWebMercator = math.log(math.tan((90 + float(coordsLatLong[1])) * lat_ratio)) * k
                        lonWebMercator = float(coordsLatLong[0]) * lon_ratio
                        lon.append(lonWebMercator)
                        lat.append(latWebMercator)
                    if ('info_' + column) in info:
                        info.pop('info_' + column, None)
                else:
                    if result[column]['type'] == 'uri':
                        popupText = result[column]['value'].replace('http://www.wikidata.org/entity/', '')
                    else:
                        popupText = result[column]['value']
            if 'info_' + column in info and isinstance(info['info_' + column], list):
                info['info_' + column].append(popupText)

    if len(lat) == 0 or len(lon) == 0:
        print('Unable to render map: no results.')
        return None

    info['lat'] = lat
    info['lon'] = lon

    source = ColumnDataSource(data=info)

    maxLat = max(lat)
    minLat = min(lat)

    rangeLat = maxLat - minLat
    marginLat = rangeLat / 5

    maxLon = max(lon)
    minLon = min(lon)

    rangeLon = maxLon - minLon
    marginLon = rangeLon / 5

    output_notebook()

    tile_provider = get_provider(CARTODBPOSITRON)
    p = figure(
        x_range=(minLon - marginLon, maxLon + marginLon),
        y_range=(minLat - marginLat, maxLat + marginLat),
        x_axis_type='mercator',
        y_axis_type='mercator',
        match_aspect=True,
        tools='pan,reset'
    )


    p.add_tile(tile_provider)

    p.circle(x='lon', y='lat', size=10, fill_color='blue', fill_alpha=0.8, source=source)

    tooltips = []

    for column in columns:
        if 'info_' + column in info:
            tooltips.append((column, '@info_' + column))

    # keep aspect ratio while zooming
    p.add_tools(BoxZoomTool(match_aspect=True))
    wheel_zoom = WheelZoomTool(zoom_on_axis=False)
    p.add_tools(wheel_zoom)
    p.toolbar.active_scroll = wheel_zoom

    p.add_tools(HoverTool(tooltips=tooltips))

    return show(p)

def __json_to_df(data):
    # create empty data frame
    df = pd.DataFrame(columns = data['head']['vars'])
    # iterate through all results
    for result in data['results']['bindings']:
        # flatten result objects (result <- result.value)
        mappedResult = {}
        for column in result:
            mappedResult[column] = result[column]['value']
        # append result to data frame
        df = df.append(mappedResult, ignore_index = True)
    return df


def __load_from_api(query):
    url = 'https://query.wikidata.org/sparql'
    payload = {
        'query': query
    }
    # add header to receive result as json
    headers = {
        'Accept': 'application/sparql-results+json'
    }
    while True:
        response = requests.get(url, params = payload, headers = headers)
        # check if request was successful
        if response.ok:
            # convert json to dict
            return json.loads(response.content)
        else:
            # raise exception in case of http error
            response.raise_for_status()
            break
    raise Exception