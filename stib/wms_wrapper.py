from owslib.wms import WebMapService
import fastkml

def get_layer(layer_name):

    wms = WebMapService('http://geoserver.gis.irisnetlab.be/geoserver/wfs', version="1.3")

    kml = wms.getmap(
        layers=[layer_name],
        srs="epsg:4326",
        bbox=wms[layer_name].boundingBox[:-1],
        size=(3000, 3000),
        format='kml', 
        transparent=True
    ).read()

    return kml

def get_placemarks(layer):
    k = fastkml.KML()
    k.from_string(layer)

    placemarks_gen = k.features().next().features()

    return placemarks_gen