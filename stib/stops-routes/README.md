# STIB data

## Lines


Download and install https://pypi.python.org/pypi/OWSLib

```
wms = WebMapService('http://geoserver.gis.irisnetlab.be/geoserver/wfs', version="1.1.0")

(142503.5170999989, 161513.0, 160195.0, 179610.0, 'EPSG:31370')


kml = wms.getmap(
    layers=['stib_mivb:ACTU_LIGNES_BRUTES'],
    srs='EPSG:31370',
    # Get the exact, updated bbox from wms['stib_mivb:ACTU_LIGNES_BRUTES'].boundingBox
    bbox=(142503.5170999989, 161513.0, 160195.0, 179610.0),
    size=(3000, 3000),
    format='kml',
    transparent=True )

out = open('lines.kml', 'wb')
out.write(kml.read())
out.close()
```

Then, convert the kml file with http://mapbox.github.io/togeojson/ because http://ogre.adc4gis.com/ does not handle files so big.

Seems like the license is compatible with ODbL, have fun !

## Stops

Les données viennent de `http://www.bruxellesmobilite.irisnet.be/urbis/geoserver/wfs`. Faire une requête `POST` avec à la barbare ces arguements :

```
<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="feature:STIB_STOP_GEO" xmlns:feature="http://mobility.irisnet.be"><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:BBOX><ogc:PropertyName>GEOM</ogc:PropertyName><gml:Box xmlns:gml="http://www.opengis.net/gml" srsName="EPSG:31370"><gml:coordinates decimal="." cs="," ts=" ">047033.95140118,063110.89946181 254971.46727622,270455.74748485</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter></wfs:Query></wfs:GetFeature>
```

Introduire le résultat sur http://ogre.adc4gis.com/ avec comme srs de source `epsg:31370` et destination `epsg:4326`

Licence libre. (Faut juste mentionner la source)

http://geonode.geobru.irisnet.be/en/webservices/#stib a l'air d'être une vraie mine d'or (même si c'est caché dans une API immonde)

Avec en vrac comme url potentiellement intéressantes :
* http://www.bruxellesmobilite.irisnet.be/map/intermodal/?zoom=1&lon=150500&lat=170000&active_layers=switch_villo0,switch_cameras0,switch_alerts0,switch_levels_of_service0,switch_levels_of_service1,switch_levels_of_service2&ref=/
* http://geonetwork.geobru.irisnet.be/geonetwork/srv/fre/csw?Request=GetRecordById&Service=CSW&Version=2.0.2&elementSetName=full&outputSchema=http://www.isotc211.org/2005/gmd&id=f288e3d2-7e38-40f5-a664-f0e42a499167
