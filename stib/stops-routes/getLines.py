from owslib.wms import WebMapService
from subprocess import check_output

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
open('/tmp/kml.kml', "w").write(result)
geojson = check_output(["../../vendor/node/bin/node", "../../vendor/node/bin/togeojson", "/tmp/kml.kml"])
open('/tmp/geo.geojson', "w").write(geojson)