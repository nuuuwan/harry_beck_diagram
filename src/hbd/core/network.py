import copy
from functools import cache, cached_property

from utils import Log

from hbd.core.DISTRICT_CAPITAL_LIST import DISTRICT_CAPITAL_LIST
from hbd.core.Line import Line

TEXT_SPACE = 1
ANGLE_CONFIG = [
    # 360
    [1, 0, 0],
    # 180
    [-1, 0, 180],
    # 90
    [0, 1, 90],
    [0, -1, 270],
    # 45
    [1, 1, 45],
    [-1, 1, 135],
    [-1, -1, 225],
    [1, -1, 315],
    # 22.5
    [1, 0.5, 22.5],
    [0.5, 1, 67.5],
    [-0.5, 1, 112.5],
    [-1, 0.5, 157.5],
    [-1, -0.5, 202.5],
    [-0.5, -1, 247.5],
    [0.5, -1, 292.5],
    [1, -0.5, 337.5],
]


log = Log(__name__)


def xy_to_k(x, y):
    return f"{x:.1f}:{y:.1f}"


def parse_direction(direction):
    dx, dy = 0, 0
    if "N" in direction:
        dy = 1
    if "S" in direction:
        dy = -1
    if "E" in direction:
        dx = 1
    if "W" in direction:
        dx = -1
    return [dx, dy]


class Network:
    def __init__(
        self,
        title: str,
        subtitle: str,
        footer_text: str,
        line_idx: dict[str, Line],
    ):
        self.title = title
        self.subtitle = subtitle
        self.footer_text = footer_text
        self.line_idx = line_idx

    @classmethod
    def from_year(cls, year: int):
        return cls(
            title=str(year),
            subtitle="",
            footer_text=" ~ ".join(
                [
                    "data from multiple sources",
                    "music by @bensound",
                    "visualization by @nuuuwan",
                ]
            ),
            line_idx={},
        )

    def copy(
        self, title=None, subtitle=None, footer_text=None, line_idx=None
    ):
        return Network(
            title=title or self.title,
            subtitle=subtitle or self.subtitle,
            footer_text=footer_text or self.footer_text,
            line_idx=line_idx
            or dict(
                [x[0], copy.deepcopy(x[1])] for x in self.line_idx.items()
            ),
        )

    @staticmethod
    def _process_line(line, node_idx):
        i_cur = 0
        for n, direction in line.direction_list:
            [dx, dy] = parse_direction(direction)
            cur_node = line.station_list[i_cur]
            if cur_node not in node_idx:
                if cur_node == "Pallai":
                    node_idx[cur_node] = [4, 13]
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

    @cached_property
    def node_idx_unsorted(self):
        node_idx = {}
        first_line = list(self.line_idx.values())[0]
        center_node = first_line.station_list[0]
        node_idx[center_node] = [0, 0]

        for line in self.line_idx.values():
            node_idx = Network._process_line(line, node_idx)

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
    def node_to_color_set(self) -> dict:
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
    def node_to_n(self) -> dict:
        node_to_n = {}
        for line in self.line_idx.values():
            station_list = line.station_list
            for node in station_list:
                if node not in node_to_n:
                    node_to_n[node] = 0
                node_to_n[node] += 1
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

    def add_line(self, line_name, color, station_list, path):
        self.line_idx[line_name] = Line(
            color=color,
            station_list=station_list,
            path=path,
        )

    def extend_line(self, line_name, station_list, path):
        line = self.line_idx[line_name]
        line.station_list += station_list
        line.path += " " + path

    def update_line(self, line_name, station_list, path):
        self.line_idx[line_name] = Line(
            color=self.line_idx[line_name].color,
            station_list=station_list,
            path=path,
        )

    def remove_line(self, line_name):
        del self.line_idx[line_name]

    def rename_station(self, old_name, new_name):
        for line in self.line_idx.values():
            line.station_list = [
                new_name if x == old_name else x for x in line.station_list
            ]

    def update_line_at_start(self, line_name, station_name, path_item):
        line = self.line_idx[line_name]
        line.station_list = [station_name] + line.station_list
        line.path = path_item + " " + line.path
