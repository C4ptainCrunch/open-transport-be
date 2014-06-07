import requests
from xml.etree import ElementTree
from utils import children_to_dict

METRO, BUS, TRAM = 'M', 'B', 'T'

class Agency(object):

    def __init__(self):
        self.lines = []
        self._get_data()

    def _get_data(self):
        r = requests.get('http://m.stib.be/api/getlinesnew.php')
        lines = ElementTree.fromstring(r.text)

        for line in lines:
            line = children_to_dict(line)
            number = int(line['id'])
            if number > 200: # Noctis lines
                number = "N{}".format(number - 200)
            mode = line['mode'] if line['mode'] else TRAM # Tram 93 returns None
            terminuses = {1: line['destination1'].capitalize(), 2: line['destination2'].capitalize()}
            colors = {'fg': line['fgcolor'], 'bg': line['bgcolor']}
            self.lines.append(Line(number, mode, terminuses, colors))

    def __repr__(self):
        return "<Agency: {} lines>".format(len(self.lines))


class Line(object):

    def __init__(self, number, mode, terminuses, colors):
        self.id = number
        self.mode = mode
        self.terminuses = terminuses
        self.colors = colors

    def to_route(self, way):
        wanted_way = way
        if not wanted_way in (1, 2):
            for key, name in self.terminuses.items():
                if name == wanted_way:
                    way = key
                    break

        return Route(self.id, way)

    def __repr__(self):
        return "<Line: {}{} '{}'-'{}'>".format(self.mode, self.id, self.terminuses[1], self.terminuses[2])



class Route(object):

    def __init__(self, id, way):
        '''Init of a route, params :
        id (int) : number of the stib line
        way (int) : 1 or 2, way of the line (see stib website)'''
        self.id = id
        self.way = way
        self.stop_points = []

        r = requests.get('http://m.stib.be/api/getitinerary.php?line={}&iti={}'.format(self.id, self.way))
        stop_points = ElementTree.fromstring(r.text)

        for stop_point in stop_points:
            self.stop_points.append(StopPoint.from_xml(stop_point, self))


    @property
    def terminus(self):
        '''Return the last stop_point'''
        return self.stop_points[-1]

    @property
    def start(self):
        '''Return the first stop_point'''
        return self.stop_points[0]

    def __repr__(self):
        return "<Route {}: direction {}, {} stops>".format(self.id, self.terminus.name, len(self.stop_points))


class StopPoint(object):
    def __init__(self, id, name, route):
        self.id = id
        self.name = name
        self.route = route

    @classmethod
    def from_xml(klass, node, route):
        node = children_to_dict(node)

        name = node['name'].capitalize()
        id = int(node['id'])

        return StopPoint(id, name, route)

    def __repr__(self):
        return "<Stop {} (#{}) (route {}#{})>".format(self.name, self.id, self.route.id, self.route.way)
