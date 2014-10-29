import wms_wrapper as ww

from utils import parse_description

def get_stops():
	pl = ww.get_placemarks(ww.get_layer('stib_mivb:ACTU_STOPS'))

	for placemark in pl:

		info_dict = parse_description(placemark.description)

		yield {
			"id": placemark.name,
			"mode":  info_dict["mode"],
			"stop_id" : info_dict["stop_id"],
			"name_nl" : info_dict["Alpha_NL"],
			"name_fr" : info_dict["Alpha_FR"],
			"slug_fr" : info_dict["DESCR_FR"],
			"slug_nl" : info_dict["DESCR_NL"],
			"point": placemark.geometry
		}


def get_lines():
	pl = ww.get_placemarks(ww.get_layer('stib_mivb:ACTU_LIGNES_BRUTES'))

	for placemark in pl:
		info_dict = parse_description(placemark.description)

		geoms = list(placemark.geometry.geoms)

		yield {
			"id": placemark.name,
			"other_id" : info_dict["NUM_LIGNE"],
			"point": geoms[0],
			"linestring": geoms[1]
		}