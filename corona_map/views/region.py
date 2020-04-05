from flask import Blueprint, render_template, current_app
import json
import csv
import pandas
import os
from corona_map.data import region_total, region_loader

mod = Blueprint('/view/<string:region>', __name__)

def getMyRegion(url):
    regions = current_app.config['REGIONS']
    value = next((x for x in regions if x['URL'] == url), None)
    return value


@mod.route('/view/<string:region_URL>')
def getRegion(region_URL):
    title = current_app.config['TITLE']
    region = getMyRegion(region_URL)
    data = region_total.getDataForRegion(region)
    return render_template('regions/ShowMap.html', TITLE=title, REGION=region['TITLE'], DATA_TOTAL=data)

