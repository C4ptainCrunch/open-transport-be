import psycopg2
import ppygis
import pygeoif
import time
import m_stib_wrapper as stib


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

        cursor.execute(
            "INSERT INTO journey_pattern(uid, mode, line_number, start_point, shape) VALUES (%s, %s, %s, %s, %s)",
            (line["id"], mode, line_numer, point, linestring)
        )

    connection.commit()


def extrapolate_route(cursor, line, route):
    ids = tuple(map(lambda x: x.id, route.stop_points))
    cursor.execute(
        "SELECT stib_id, ST_X(coord), ST_Y(coord) FROM stop_point WHERE stib_id IN %s",
        (ids,)
    )
    coords = {}

    for stop_id, x, y in cursor:
        coords[stop_id] = (x, y)

    linestring = []

    for stop in route.stop_points:
        try:
            linestring.append(coords[stop.id])
        except KeyError:
            print "Missing stop {} on line {}#{}".format(stop.id, line.id, route.way)

    start_point = ppygis.Point(linestring[0][0],linestring[0][1])
    linestring = ppygis.LineString(map(lambda x: ppygis.Point(x[0],x[1]), linestring))
    uid = "GENERATED_LIGNES.line{}-way{}.{}".format(line.id, route.way, line.mode)

    cursor.execute(
        "INSERT INTO journey_pattern(uid, mode, line_number, start_point, shape, direction) VALUES (%s, %s, %s, %s, %s, %s)",
        (uid, line.mode, line.id, start_point, linestring, str(route.way))
    )

    connection.commit()

    


def find_direction_and_assign_journey(cursor):
    for line in stib.Agency().lines:
        direction = 0
        time.sleep(0.1)
        
        # Find lines without geographic path
        cursor.execute("SELECT COUNT(*) FROM journey_pattern WHERE line_number=%s", (str(line.id),))
        items = cursor.fetchone()[0]
        routes =  (line.to_route(1), line.to_route(2))

        if items == 0:
            print "Extrapolating line {}...".format(line.id)
            for route in routes:
                extrapolate_route(cursor, line, route)

        for route in routes:
            direction += 1

            # Find the closest route starting from the start stop_point of the line
            cursor.execute(
                """SELECT journey_pattern.id, ST_distance(ST_PointN(journey_pattern.shape,1), stop_point.coord) AS distance
                FROM journey_pattern, stop_point
                WHERE (stop_point.stib_id=%s and journey_pattern.line_number=%s)
                ORDER BY distance ASC""",
                (route.stop_points[0].id, str(line.id))
            )

            result = cursor.fetchone()

            if result is None:
                print "Missing line {} with stop {}".format(line.id, route.stop_points[0].id)
                continue

            journey_id = result[0]

            # Set the direction to this route and set colors
            cursor.execute(
                "UPDATE journey_pattern SET direction=%s, bg_color=%s, fg_color=%s WHERE id=%s",
                (direction, "#"+line.colors["bg"], "#"+line.colors["fg"], journey_id)
            )

            # Set the journey_pattern_id and the order of every stop of this journey_pattern
            ids = map(lambda x: x.id, route.stop_points)

            for i, stop in enumerate(ids):
                cursor.execute(
                    "UPDATE stop_point SET journey_pattern_id=%s, pattern_order=%s WHERE stib_id=%s",
                    (journey_id, i, stop)
                )
    
    connection.commit()

if __name__ == '__main__':
    import get_static_data as gsd

    connection = psycopg2.connect(database='nikita')
    cursor = connection.cursor()

    print "Processing stops..."
    insert_stops(cursor, gsd.get_stops())

    print "Processing lines..."
    insert_lines(cursor, gsd.get_lines())

    print "Processing directions..."
    find_direction_and_assign_journey(cursor)

    print "Writing to db..."

    cursor.close()
    connection.close()

    print "Done."