from flask import Blueprint, jsonify
from corona_map.data import region_loader


mod = Blueprint('/data/<string:region>/history', __name__)

def getDataForRegion(region):
    values = region_loader.getDataFrameFromRegion(region)

    data = values.groupby(['Zeitpunkt']).sum()
    data = data.reset_index()
    return data

@mod.route('/data/<string:region_URL>/history')
def getHistoricalData(region_URL):
    region = region_loader.getMyRegion(region_URL)
    data = getDataForRegion(region)

    return jsonify(data.values.tolist())

