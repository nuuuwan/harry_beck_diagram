"""Map roads."""
import math

from clabs.cmd_utils import run_cmd
from clabs.io.file import read_json, write, write_json
from clabs.latlng_utils import get_bbox
from clabs.xml_utils import _, render_xml


def quantize_locations(locations, Q):
    """Quantize location."""

    def q(latlng):
        def q1(x):
            return round(x * Q, 0)

        lat, lng = latlng
        return q1(lat), q1(lng)

    return dict(
        list(
            map(
                lambda x: (x[0], q(x[1])),
                locations.items(),
            )
        )
    )


def normalize_locations(locations):
    """Normalize locations."""

    def build_index(x_list):
        x_list.sort()
        return dict(
            zip(
                x_list,
                range(0, len(x_list)),
            )
        )

    lat_index = build_index(
        list(
            map(
                lambda x: x[0],
                locations.values(),
            )
        )
    )
    lng_index = build_index(
        list(
            map(
                lambda x: x[1],
                locations.values(),
            )
        )
    )

    new_locations = {}
    for location_name, [lat, lng] in locations.items():
        new_locations[location_name] = [
            lat_index[lat],
            lng_index[lng],
        ]
    return new_locations


def get_junctions(roads):
    """Find junctions."""
    junction_set = set()
    location_to_neighbors = {}
    for ___, location_list in roads.items():
        junction_set.add(location_list[0])
        junction_set.add(location_list[-1])
        n = len(location_list)
        for i, location_name in enumerate(location_list):
            if location_name not in location_to_neighbors:
                location_to_neighbors[location_name] = []

            if i > 0:
                location_to_neighbors[location_name].append(
                    location_list[i - 1]
                )
            if i < n - 1:
                location_to_neighbors[location_name].append(
                    location_list[i + 1]
                )

    for location_name, neighbors in location_to_neighbors.items():
        if len(neighbors) >= 3:
            junction_set.add(location_name)

    return location_to_neighbors


def reset_locations(locations, roads):
    """Reset locations."""
    # return locations
    junction_info = get_junctions(roads)
    # quantized_locations = quantize_locations(locations, 15)

    # Junctions
    normalized_locations = locations
    # normalized_locations = normalize_locations(quantized_locations)

    new_locations = {}
    max_junction_name = sorted(
        junction_info.items(),
        key=lambda x: -len(x[1]),
    )[0][0]

    visited_set = set([max_junction_name])
    complete_set = set()
    new_locations[max_junction_name] = normalized_locations[max_junction_name]
    while visited_set:
        max_junction_name = None
        max_n_unvisited_nei_set = None
        for junction_name in visited_set:
            n_unvisited_nei_set = set()
            for nei_name in junction_info[junction_name]:
                if (
                    nei_name not in visited_set
                    and nei_name not in complete_set
                ):
                    n_unvisited_nei_set.add(nei_name)
            if max_n_unvisited_nei_set is None or len(
                max_n_unvisited_nei_set
            ) < len(n_unvisited_nei_set):
                max_junction_name = junction_name
                max_n_unvisited_nei_set = n_unvisited_nei_set
        if not max_n_unvisited_nei_set:
            break

        print('-' * 32)
        print(max_junction_name.upper(), max_n_unvisited_nei_set)
        complete_set.add(max_junction_name)

        for location_name in max_n_unvisited_nei_set:
            x1, y1 = new_locations[max_junction_name]
            x2, y2 = normalized_locations[location_name]

            dx = x2 - x1
            dy = y2 - y1

            r = math.sqrt(dx**2 + dy**2)
            theta = math.atan2(dy, dx)
            ROUND = math.pi / 4
            theta2 = round(theta / ROUND, 0) * ROUND

            x3 = x1 + r * math.cos(theta2)
            y3 = y1 + r * math.sin(theta2)
            new_locations[location_name] = [x3, y3]
            print(location_name, 45 * theta / ROUND, 45 * theta2 / ROUND)
            visited_set.add(location_name)

    for ___, location_list in roads.items():
        i1 = 0
        n = len(location_list)
        while i1 < n - 1:
            i2 = None
            for i in range(i1 + 1, n):
                if location_list[i] in new_locations:
                    i2 = i
                    break
            if i2 is None:
                i2 = n - 1
            lat1, lng1 = new_locations[location_list[i1]]
            lat2, lng2 = new_locations[location_list[i2]]

            for i in range(i1 + 1, i2):
                p = (i - i1) / (i2 - i1)
                lat = lat1 * (1 - p) + lat2 * p
                lng = lng1 * (1 - p) + lng2 * p
                new_locations[location_list[i]] = [lat, lng]
            i1 = i2

    # normalized_locations = normalize_locations(new_locations)
    return new_locations


def draw(data_dir):
    """Map roads."""
    locations_original = read_json('data/%s/LOCATIONS.json' % data_dir)
    roads = read_json('data/%s/ROADS.json' % data_dir)
    locations = reset_locations(locations_original, roads)
    # locations = locations_original
    write_json('data/%s/LOCATIONS.used.json' % data_dir, locations)

    latlng_list = list(locations.values())
    (min_lat, min_lng, lat_span, lng_span) = get_bbox([latlng_list])

    WIDTH, HEIGHT = 600, 900
    PADDING = 100

    def t(latlng):
        lat, lng = latlng
        px = (lng - min_lng) / lng_span
        py = (lat - min_lat) / lat_span
        return (
            (WIDTH - PADDING * 2) * px + PADDING,
            (HEIGHT - PADDING * 2) * (1 - py) + PADDING,
        )

    LOCATION_MARKER_RADIUS = 5
    LOCATION_MARKER_FONT_SIZE = 10

    def render_location(name_latlng):
        name, [lat, lng] = name_latlng
        x, y = t([lat, lng])
        return _(
            'svg',
            [
                _(
                    'circle',
                    [],
                    {
                        'cx': x,
                        'cy': y,
                        'r': LOCATION_MARKER_RADIUS,
                        'fill': 'white',
                        'stroke': 'black',
                        'stroke-width': LOCATION_MARKER_RADIUS / 2,
                    },
                ),
                _(
                    'text',
                    name,
                    {
                        'x': x + LOCATION_MARKER_RADIUS * 2,
                        'y': y + LOCATION_MARKER_RADIUS * 1,
                        'fill': 'black',
                        'stroke': None,
                        'text-anchor': 'start',
                        'font-family': 'Futura',
                        'font-size': LOCATION_MARKER_FONT_SIZE,
                    },
                ),
            ],
        )

    rendered_locations = list(map(render_location, locations.items()))
    ROAD_WIDTH = 3
    ROAD_FONT_SIZE = 8

    def render_road(name_location_list):
        road_name, location_list = name_location_list
        rendered_road_segments = []
        n = len(location_list)
        for i in range(0, n - 1):
            x1, y1 = t(locations[location_list[i]])
            x2, y2 = t(locations[location_list[i + 1]])
            x12 = (x1 + x2) / 2
            y12 = (y1 + y2) / 2
            rendered_road_segments.append(
                _(
                    'svg',
                    [
                        _(
                            'line',
                            [],
                            {
                                'x1': x1,
                                'y1': y1,
                                'x2': x2,
                                'y2': y2,
                                'fill': None,
                                'stroke': 'red',
                                'stroke-width': ROAD_WIDTH,
                            },
                        ),
                        _(
                            'text',
                            road_name,
                            {
                                'x': x12,
                                'y': y12,
                                'fill': 'gray',
                                'stroke': None,
                                'font-size': ROAD_FONT_SIZE,
                            },
                        ),
                    ],
                )
            )
        return _('svg', rendered_road_segments)

    rendered_roads = list(map(render_road, roads.items()))

    svg = _(
        'svg',
        rendered_roads + rendered_locations,
        {
            'width': WIDTH,
            'height': HEIGHT,
        },
    )
    svg_file_name = '/tmp/hbd.%s.svg' % (data_dir)
    write(svg_file_name, render_xml(svg))
    run_cmd('open %s' % svg_file_name)


if __name__ == '__main__':
    draw('sl_highways')
