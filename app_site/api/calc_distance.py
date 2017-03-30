import geopy.distance
from scipy.spatial.distance import cdist
# your data

list = [
            (11.6702634, 72.313323), (11.6723698, 78.114523),
            (31.67342698, 78.465323), (12.6702634, 72.313323),
            (12.67342698, 75.465323)
        ]

coord = (11.6723698, 78.114523)

# Expected result is
# 11 40m 20.5313s N, 78 6m 52.2828s E
# (11.6723698, 78.114523)


def closest_node_test(node, nodes):
    return nodes[cdist([node], nodes).argmin()]


def nearest_point_test(coordinate, coordinate_list):
    pts = [geopy.Point(p[0], p[1]) for p in coordinate_list]
    onept = geopy.Point(coordinate[0], coordinate[1])
    alldist = [(p, geopy.distance.distance(p, onept).km) for p in pts]
    # This line will return the nearest item
    return min(alldist, key=lambda x: (x[1]))[0]


def nearest_catadores(coord_residue, catador_list):
    catadores = {}
    for p in catador_list:
        catadores[p.catador.id] = geopy.Point(p.georef.latitude, p.georef.longitude)

    onept = geopy.Point(coord_residue[0], coord_residue[1])

    alldist = [(cat, geopy.distance.distance(p, onept).km)
               for cat, p in zip(catadores.keys(), catadores.values())]
    return [i[0] for i in sorted(alldist, key=lambda tup: tup[1])[0:3]]

# point = nearest_point_test(coord, list)
# print(str(point.latitude) + ' - ' + str(point.longitude))
# print(closest_node_test(coord, list))
