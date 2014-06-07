def children_to_dict(elem):
    d = {}
    for tag in elem:
        d[tag.tag] = tag.text

    return d
