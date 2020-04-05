from flask import Blueprint, current_app, jsonify, make_response
from corona_map.data import region_loader
from corona_map.data.tools import geolocation_calculator
import json

mod = Blueprint('/data/<string:region>/daily', __name__)

def getDataForRegion(region):
    values = region_loader.getDataFrameFromRegion(region)

    data = values.groupby(['date', 'Region']).sum()
    data = data.reset_index()
    data = data.sort_values(by=['date', 'Region'])
    return data

@mod.route('/data/<string:region_URL>/daily')
def getCommunityData(region_URL):
    region = region_loader.getMyRegion(region_URL)
    data = getDataForRegion(region)

    lats = data['lat'].unique()
    lons = data['lon'].unique()

    center_lat, center_lon = geolocation_calculator.getCenter(lats, lons)

    data_json = json.loads(data.to_json(orient='records'))

    r = make_response(json.dumps({'data': data_json, 'map': {'lat': center_lat, 'lon': center_lon}}))
    r.mimetype = 'application/json'
    return r

