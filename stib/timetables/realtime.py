import requests
from xml.etree import ElementTree
from utils import children_to_dict

def get_positions(**kwargs):
    line = kwargs.get('line', None)
    way = kwargs.get('way', None)
    route = kwargs.get('route', None)
    if not route is None:
        line = route.id
        way = route.way

    stop_points = []

    r = requests.get('http://m.stib.be/api/getitinerary.php?line={}&iti={}'.format(line, way))
    stops = ElementTree.fromstring(r.text)

    for stop in stops:
        node = children_to_dict(stop)
        present = False if node.get('present', False) is False else True
        stop_points.append((node['id'], present))

    return stop_points
