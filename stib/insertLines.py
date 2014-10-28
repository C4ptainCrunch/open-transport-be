import network
import time

import psycopg2
import ppygis

connection = psycopg2.connect(database='nikita')
cursor = connection.cursor()

a = network.Agency()
for line in a.lines:
	direction = 0
	print "\n" + str(line.id)
	time.sleep(0.5)
	for route in (line.to_route(1), line.to_route(2)):
		direction += 1
		cursor.execute(
			"INSERT INTO journey_pattern(direction) VALUES (%s)",
			(direction,)
		)
		for stop in route.stop_points:
			print ".",
			cursor.execute(
				"UPDATE stop_point SET journey_pattern_id=lastval() WHERE gml_id = '%s'",
				(stop.id,)
			)
	connection.commit()


connection.commit()
cursor.close()
connection.close()