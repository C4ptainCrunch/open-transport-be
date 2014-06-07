import const
import requests
import json

def get_list():
    url = "http://www.railtime.be/website/map/StationLocatorService.asmx/GetRailwayPointsForJson"
    payload = "{applicationId: 'irtmap'}"
    ret = requests.post(url, data=payload, headers=const.HEADERS)

    stations = []

    for station in json.loads(ret.json()['d']):
        id = station['StationId']
        latitude = station['Latitude']
        longitude = station['Longitude']
        name = {
            'fr': station['DescriptionFr'],
            'en': station['DescriptionEn'],
            'nl': station['DescriptionNl'],
            'de': station['DescriptionDe']
        }

        stations.append({
            'id': id,
            'latitude': latitude,
            'longitude': longitude,
            'name': name,
        })

    return stations
