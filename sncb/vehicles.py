import json
import requests
import datetime

from const import IRAIL_HEADERS, HEADERS

def get_list():
    max_id = 0
    url = "http://www.railtime.be/website/map/StationLocatorService.asmx/GetTrainDataForJson"
    payload = "{{applicationId: 'irtmap', maxId: {}, trainId: ''}}"
    a = requests.post(url, data=payload.format(max_id), headers=HEADERS)

    trains = json.loads(a.json()['d'])
    trains = trains['TrainPositions']
    trains_list = []
    for raw_train in trains:
        departure_date = datetime.datetime.fromtimestamp(float(raw_train['DepartureDate'][6:-2]) / 1000)

        trains_list.append({
            'journey_id': raw_train['TrainNumber'],
            'canceled': raw_train['Deleted'],
            'journey_type': raw_train['TrainType'],
            'terminuses': {
                'start': raw_train['OriginStationId'],
                'stop': raw_train['DestinationStationId']
            },
            'last_known_stop_point': raw_train['StationId']
        })

    return trains_list

def get(id):
    url = "http://data.irail.be/NMBS/Vehicle/{0}/{1.year}/{1.month}/{1.day}/{1.hour}/{1.minute}.json"
    url = url.format(id, datetime.datetime.now())
    ret = requests.get(url, headers=HEADERS)

    return ret.json()
