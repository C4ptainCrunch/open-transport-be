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


def insert_lines(cursor, lines):
	for line in lines:
		point = ppygis.Point(*line["point"].coords[0])
		linestring = ppygis.LineString(map(lambda x: ppygis.Point(*x), line["linestring"].coords))

		mode = line['other_id'][-1].upper()
		line_numer = line['other_id'][:-1]
		if line_numer.startswith("0"):
			line_numer = line_numer[1:]

		a = cursor.execute(
			"INSERT INTO journey_pattern(uid, mode, line_number, start_point, shape) VALUES (%s, %s, %s, %s, %s)",
			(line["id"], mode, line_numer, point, linestring)
		)

	connection.commit()



if __name__ == '__main__':
	import get_static_data as gsd

	connection = psycopg2.connect(database='nikita')
	cursor = connection.cursor()

	insert_stops(cursor, gsd.get_stops())
	insert_lines(cursor, gsd.get_lines())

	cursor.close()
	connection.close()