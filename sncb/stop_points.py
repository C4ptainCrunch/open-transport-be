import const
import requests
import json

def get_list():
    url = "http://www.railtime.be/website/map/StationLocatorService.asmx/GetRailwayPointsForJson"
    payload = "{applicationId: 'irtmap'}"
    ret = requests.post(url, data=payload, headers=const.HEADERS)

    irail_url = "http://api.irail.be/stations/?format=json"
    irail_ret = requests.get(irail_url, headers=const.IRAIL_HEADERS)
    irail_stations = irail_ret.json()['station']

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

        corresponding = list(filter(lambda x: x['name'] == name['nl'],irail_stations))
        if len(corresponding) > 0:
            real_id = corresponding[0]['id']
        else:
            real_id = "UNKNOWN.UNKNOWN.{}".format(id)


        stations.append({
            'sncb_id': id,
            'id': real_id,
            'latitude': latitude,
            'longitude': longitude,
            'name': name,
        })

    return stations
