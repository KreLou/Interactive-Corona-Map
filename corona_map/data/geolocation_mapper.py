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
    url = 'https://nominatim.openstreetmap.org/search.php?q=' + miunicipality + ',' + district + '&format=json'
    response = json.loads(requests.get(url).text)

    if (len(response) > 0):
        lat = response[0]['lat']
        lon = response[0]['lon']
    else:
        lat = None
        lon = None
    return lat, lon

def saveGeoLoactionForRegion(municipality, district, lat, lon):
    dataFrame = pandas.DataFrame({'region': [municipality], 'country': [district], 'lat': [lat], 'lon': [lon]})
    default = getLocationsDataframe()

    default = default.append(dataFrame, ignore_index=True, sort=False)

    default.to_csv(getPath(), index=False)


