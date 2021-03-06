from flask import Blueprint, make_response
from corona_map.data import geolocation_mapper, region_loader
from corona_map.data.tools import geolocation_calculator
import json

mod = Blueprint('/data/<string:region>/total', __name__)


def getDataForRegion(region):
    group_by_list = ['Region', 'lat', 'lon', 'Polygon']
    values = region_loader.getDataFrameFromRegion(region)


    data = values[group_by_list].copy().drop_duplicates(keep='first')
    data['Anzahl'] = values.groupby(group_by_list)['Anzahl'].transform('sum')
    data['latest-record'] = values.groupby(group_by_list)['date'].transform('max')

    for index, row in data.iterrows():
        json_object = json.loads(row['Polygon'])
        data._set_value(index, 'Polygon', json_object)


    data = data.reset_index()


    return data


@mod.route('/data/<string:region_URL>/total')
def getRegion(region_URL):
    region = region_loader.getMyRegion(region_URL)
    dataFrame = getDataForRegion(region)

    lats = dataFrame['lat'].unique()
    lons = dataFrame['lon'].unique()

    center_lat, center_lon = geolocation_calculator.getCenter(lats, lons)
    data_json = json.loads(dataFrame.to_json(orient='records'))


    amounts = dataFrame['Anzahl']

    norminalized = amounts[~((amounts-amounts.mean()).abs() > 3*amounts.std())]
    min_value = norminalized.min()
    max_value = norminalized.max()

    r = make_response(json.dumps({'data': data_json, 'map': {'lat': center_lat, 'lon': center_lon}, 'range': {'min': int(min_value), 'max': int(max_value)}}))
    r.mimetype = 'application/json'
    return r




