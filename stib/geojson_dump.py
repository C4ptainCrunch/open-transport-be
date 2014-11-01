import geojson

def stops_to_geojson(stops):
    features = []
    for stop in stops:
        g = geojson.Point(stop["point"].coords[0])
        f = geojson.Feature(geometry=g, properties={"name": stop["name_fr"]})
        features.append(f)

    return geojson.FeatureCollection(features)

def lines_to_geojson(lines):
    features = []
    for line in lines:
        point = geojson.Point(line["point"].coords[0])

        point_list = map(lambda x: x.coords[0], line["linestring"].geoms)
        linestring = geojson.LineString(point_list)

        geom_collection = geojson.GeometryCollection([linestring, point])

        f = geojson.Feature(geometry=geom_collection, properties={"id": line["other_id"]})
        features.append(f)

    return geojson.FeatureCollection(features)


if __name__ == '__main__':
    import get_static_data as gsd

    open("data/lines.geojson", "w").write(str(lines_to_geojson(gsd.get_lines())))
    open("data/stops.geojson", "w").write(str(stops_to_geojson(gsd.get_stops())))

