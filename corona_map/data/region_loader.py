from flask import current_app
import pandas
import os
from corona_map.data import geolocation_mapper


def getMyRegion(url):
    regions = current_app.config['REGIONS']
    value = next((x for x in regions if x['URL'] == url), None)
    return value

def _getValues(region):
    if region['TYPE'] == 'csv':
        return _getCSVValues(region['FILE'])
    return None

def _getCSVValues(file):
    file_path  = os.path.join(os.path.abspath(current_app.root_path), 'database',  file)
    data = pandas.read_csv(file_path, delimiter=';', header=0, encoding='utf-8')
    data['date'] = pandas.to_datetime(data['Zeitpunkt'], dayfirst=True)

    return data


def getDataFrameFromRegion(region):

    data = _getValues(region)
    geoDataFrame =  geolocation_mapper.getLocationsDataframe()

    data = data.set_index(['Region']).join(geoDataFrame.set_index(['region']), lsuffix='_caller', rsuffix='_other')
    data = data.reset_index()
    data.rename(columns={'index': 'Region'}, inplace=True)

    #Fill Gaps in Location
    missingGeo = data[data['lat'].isnull()]
    missingMunicipalities = missingGeo['Region'].drop_duplicates(keep='first')

    if (len(missingMunicipalities) > 0):
        for index, municipality in missingMunicipalities.items():
            lat, lon = geolocation_mapper.searchForGeolocation(municipality, region['OSM_DISTRICT'])
            print('Found for ' + municipality + ', ' + (lat if lat != None else 'None') + ', ' + (lon if lon != None else 'None'))
            if lat is not None and lon is not None:
                geolocation_mapper.saveGeoLoactionForRegion(municipality=municipality, district=region['TITLE'], lat=lat, lon=lon)
            else:
                print('Found no Coordination for ' + municipality)

        data = _getValues(region)
        geoDataFrame = geolocation_mapper.getLocationsDataframe()
        data = data.set_index(['Region']).join(geoDataFrame.set_index(['region']), lsuffix='_caller', rsuffix='_other')
        data = data.reset_index()
        data.rename(columns={'index': 'Region'}, inplace=True)


    return data