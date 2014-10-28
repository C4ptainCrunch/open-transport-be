from owslib.wms import WebMapService
from subprocess import check_output
import requests
import json
import random

def get_lines_bloated():
	"""Return evaluated (geo)json containing the physical path of stib vehicules"""

	wms = WebMapService('http://geoserver.gis.irisnetlab.be/geoserver/wfs', version="1.1.0")
	kml = wms.getmap(
	    layers=['stib_mivb:ACTU_LIGNES_BRUTES'],
	    srs='EPSG:31370',
	    # Get the exact, updated bbox from wms['stib_mivb:ACTU_LIGNES_BRUTES'].boundingBox
	    bbox=(142503.5170999989, 161513.0, 160195.0, 179610.0),
	    size=(3000, 3000),
	    format='kml',
	    transparent=True)

	result = kml.read()
	rand_id = random.randint(0, 10000)
	open('/tmp/kml-{}.kml'.format(rand_id), "w").write(result)
	geojson = check_output([
		"../vendor/node/bin/node",
		"../vendor/node/bin/togeojson",
		"/tmp/kml-{}.kml".format(rand_id)
	])

	return json.loads(geojson)


def get_stops():
	"""Return evaluated (geo)json containing every vehicle stop of the stib"""

	a = requests.post(
		"http://www.bruxellesmobilite.irisnet.be/urbis/geoserver/wfs",
		data="""<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="feature:STIB_STOP_GEO" xmlns:feature="http://mobility.irisnet.be"><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:BBOX><ogc:PropertyName>GEOM</ogc:PropertyName><gml:Box xmlns:gml="http://www.opengis.net/gml" srsName="EPSG:31370"><gml:coordinates decimal="." cs="," ts=" ">047033.95140118,063110.89946181 254971.46727622,270455.74748485</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter></wfs:Query></wfs:GetFeature>"""
	)
	rand_id = random.randint(0, 10000)
	open("/tmp/points-{}".format(rand_id), "w").write(a.text)
	check_output([
		"ogr2ogr", "-f", "GeoJSON",
		"-t_srs", "epsg:4326",
		"-s_srs", "epsg:31370",
		"/tmp/points-{}.json".format(rand_id),
		"/tmp/points-{}".format(rand_id)
	])

	content = open("/tmp/points-{}.json".format(rand_id)).read()
	return json.loads(content)


if __name__ == '__main__':
	print "Gathering lines..."
	open("data/lines.geojson", 'w').write(json.dumps(get_lines()))

	print "Gathering stops..."
	open("data/stops.geojson", 'w').write(json.dumps(get_stops()))

	print "Done."