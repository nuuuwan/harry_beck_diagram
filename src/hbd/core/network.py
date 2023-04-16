import copy
from functools import cache, cached_property

from utils import JSONFile, Log

from hbd.core.DISTRICT_CAPITAL_LIST import DISTRICT_CAPITAL_LIST
from hbd.core.line import Line

TEXT_SPACE = 2
ANGLE_CONFIG = [
    [1, 0, 0],
    [-1, 0, 180],
    [1, 1, 45],
    [-1, 1, 135],
    [1, -1, 315],
    [-1, -1, 215],
    [1, 0.5, 22.5],
    [1, -0.5, 360 - 22.5],
    [0, 1, 90],
    [0, -1, 270],
]

HACK_NODE_IDX = {'Pallai': [4, 13]}

log = Log(__name__)


def xy_to_k(x, y):
    return f'{x:.1f}:{y:.1f}'


def parse_direction(direction):
    dx, dy = 0, 0
    if 'N' in direction:
        dy = 1
    if 'S' in direction:
        dy = -1
    if 'E' in direction:
        dx = 1
    if 'W' in direction:
        dx = -1
    return [dx, dy]


class Network:
    def __init__(
        self, title: str, footer_text: str, line_idx: dict[str, Line]
    ):
        self.title = title
        self.footer_text = footer_text
        self.line_idx = line_idx

    @staticmethod
    def from_file(config_path):
        config = JSONFile(config_path).read()
        title = config.get('title', 'Untitled')
        footer_text = config.get('footer_text', ' ')
        line_idx = []
        for line in config['line_idx']:
            line_idx.append(Line.from_dict(line))
        return Network(title, footer_text, line_idx)

    def copy(self, title=None, footer_text=None, line_idx=None):
        return Network(
            title=title or self.title,
            footer_text=footer_text or self.footer_text,
            line_idx=line_idx
            or dict(
                [x[0], copy.deepcopy(x[1])] for x in self.line_idx.items()
            ),
        )

    @property
    def line_idx_sorted(self) -> list[Line]:
        return list(
            filter(
                lambda line: 'direction_list' in line,
                self.line_idx,
            )
        )

    @cached_property
    def node_idx_unsorted(self):
        node_idx = {}
        first_line = list(self.line_idx.values())[0]
        center_node = first_line.station_list[0]
        node_idx[center_node] = [0, 0]

        for line in self.line_idx.values():
            i_cur = 0
            for n, direction in line.direction_list:
                [dx, dy] = parse_direction(direction)
                cur_node = line.station_list[i_cur]
                if cur_node not in node_idx:
                    node_idx[cur_node] = HACK_NODE_IDX.get(cur_node)
                if not node_idx[cur_node]:
                    log.error(f'No node_idx for {cur_node}')
                x_cur, y_cur = node_idx[cur_node]
                for i in range(0, n):
                    node = line.station_list[i_cur + i + 1]
                    if node in node_idx:
                        continue
                    node_idx[node] = [
                        x_cur + dx * (i + 1),
                        y_cur + dy * (i + 1),
                    ]
                i_cur += n
        return node_idx

    @cache
    def get_node_cmp_value(self, node):
        if node in self.terminal_list:
            return 0
        if node in self.junction_list:
            return 1
        if node in DISTRICT_CAPITAL_LIST:
            return 2
        return 3

    @cached_property
    def node_idx(self):
        return dict(
            sorted(
                self.node_idx_unsorted.items(),
                key=lambda x: self.get_node_cmp_value(x[0]),
            )
        )

    @cached_property
    def loc_list(self):
        return list(self.node_idx.values())

    @cached_property
    def node_to_color_set(self):
        node_to_color_set = {}
        for line in self.line_idx.values():
            station_list = line.station_list
            color = line.color
            for node in station_list:
                if node not in node_to_color_set:
                    node_to_color_set[node] = set()
                node_to_color_set[node].add(color)
        return node_to_color_set

    @cached_property
    def node_to_n(self):
        node_to_n = {}
        for node, color_set in self.node_to_color_set.items():
            node_to_n[node] = len(color_set)
        return node_to_n

    @cached_property
    def junction_list(self):
        junction_list = []
        for node, n in self.node_to_n.items():
            if n >= 2:
                junction_list.append(node)
        return junction_list

    @staticmethod
    def is_point_free(x, y, dx, dy, used_ks):
        for d in range(TEXT_SPACE):
            k = xy_to_k(x + dx * (d + 1), y + dy * (d + 1))
            if k in used_ks:
                return False
        return True

    @staticmethod
    def get_node_text_angle(used_ks, x, y):
        for dx, dy, angle in ANGLE_CONFIG:
            if not Network.is_point_free(x, y, dx, dy, used_ks):
                continue

            for d in range(TEXT_SPACE):
                k = xy_to_k(x + dx * (d + 1), y + dy * (d + 1))
                used_ks.add(k)
            return used_ks, angle
        return used_ks, None

    @cached_property
    def node_to_text_angle(self):
        used_ks = set()

        for node, (x, y) in self.node_idx.items():
            used_ks.add(xy_to_k(x, y))

        node_to_text_angle = {}
        for node, (x, y) in self.node_idx.items():
            used_ks, text_angle = Network.get_node_text_angle(used_ks, x, y)
            node_to_text_angle[node] = text_angle

        return node_to_text_angle

    @cached_property
    def node_to_neighbors(self):
        node_to_neighbors = {}
        for line in self.line_idx.values():
            station_list = line.station_list
            for i in range(len(station_list) - 1):
                node1, node2 = station_list[i], station_list[i + 1]
                if node1 not in node_to_neighbors:
                    node_to_neighbors[node1] = set()
                if node2 not in node_to_neighbors:
                    node_to_neighbors[node2] = set()
                node_to_neighbors[node1].add(node2)
                node_to_neighbors[node2].add(node1)
        return node_to_neighbors

    @cached_property
    def terminal_list(self):
        terminal_list = []
        for node, neighbors in self.node_to_neighbors.items():
            if len(neighbors) == 1:
                terminal_list.append(node)
        return terminal_list
