from flask import current_app
import os
import pandas
import requests
import json

def getPath():
    return os.path.join(os.path.abspath(current_app.root_path), 'database', 'geolocation.csv')

def getLocationsDataframe():
    try:
        data = pandas.read_csv(getPath(), header=0, encoding='utf-8')
        data.drop_duplicates(inplace=True, keep='first')
        return data
    except:
        return pandas.DataFrame({'region': [], 'country': [], 'lat': [], 'lon': []})

def searchForGeolocation(miunicipality, district):
    url = 'https://nominatim.openstreetmap.org/search.php?q=' + miunicipality + ',' + district + '&format=json&type=administrative&polygon_geojson=1'
    response = json.loads(requests.get(url).text)

    if (len(response) > 0):
        lat = response[0]['lat']
        lon = response[0]['lon']
        polygon = response[0]['geojson']['coordinates']
        if len(polygon) == 1:
            polygon = polygon[0]


        reverted = []
        if len(polygon) >= 2 * 4:
            for rev_long, rev_lat in polygon:
                reverted.append([rev_lat, rev_long])
            polygon = json.dumps(reverted)
    else:
        lat = None
        lon = None
        polygon = None
    return lat, lon, polygon

def saveGeoLoactionForRegion(municipality, district, lat, lon, polygon):
    dataFrame = pandas.DataFrame({'region': [municipality], 'country': [district], 'lat': [lat], 'lon': [lon], 'Polygon': [polygon]})
    default = getLocationsDataframe()

    default = default.append(dataFrame, ignore_index=True, sort=False)

    default.to_csv(getPath(), index=False)


