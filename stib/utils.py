import re

def children_to_dict(elem):
    d = {}
    for tag in elem:
        d[tag.tag] = tag.text

    return d

def parse_description(description):
	info = re.sub('<[^<]+?>', '', description)
	info_dict = {}

	for line in info.split("\n"):
		line = line.strip()
		if ": " in line:
			split = line.split(": ")
			info_dict[split[0]] = split[1]

	return info_dict