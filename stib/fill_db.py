import psycopg2
import ppygis


def insert_stops(cursor, stops):
	for stop in stops:
		coord_gis = ppygis.Point(*stop["point"].coords[0])
		a = cursor.execute(
			"INSERT INTO stop_point(uid, stib_id, name_fr, name_nl, slug_fr, slug_nl, coord) VALUES (%s, %s, %s, %s, %s, %s, %s)",
			(stop["id"], stop["stop_id"], stop["name_fr"], stop["name_nl"], stop["slug_fr"], stop["slug_nl"], coord_gis)
		)

	connection.commit()



if __name__ == '__main__':
	import get_static_data as gsd

	# Connect to an existing spatially enabled database
	connection = psycopg2.connect(database='nikita')
	cursor = connection.cursor()

	insert_stops(cursor, gsd.get_stops())

	cursor.close()
	connection.close()