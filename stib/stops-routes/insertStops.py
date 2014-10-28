import psycopg2
import ppygis
import json

# Connect to an existing spatially enabled database
connection = psycopg2.connect(database='nikita')
cursor = connection.cursor()

geoj = json.loads(open('/tmp/points.json').read())

i = 0
for feature in geoj["features"]:
	prop = feature["properties"]
	coord = feature["geometry"]["coordinates"]
	gml_id = prop['gml_id'].split('.')[-1]
	coord_gis = ppygis.Point(*coord)
	a = cursor.execute(
		"INSERT INTO stop_point(gml_id, name_fr, name_nl, coord) VALUES (%s, %s, %s, %s)",
		(gml_id, prop['NAME_FR'], prop['NAME_NL'], coord_gis)
	)
	
	i += 1
	#print "Insert " + prop['NAME_FR']

print i
connection.commit()
cursor.close()
connection.close()