import copy
from functools import cache, cached_property

from utils import JSONFile, Log

from hbd.DISTRICT_CAPITAL_LIST import DISTRICT_CAPITAL_LIST

ANGLE_CONFIG = [
    [1, 0, 0],
    [-1, 0, 180],
    [1, 1, 45],
    [1, -1, 315],
    [0, 1, 90],
    [0, -1, 270],
    [-1, 1, 135],
    [-1, -1, 215],
    [1, 0.5, 22.5],
    [1, -0.5, 360 - 22.5],
]

log = Log(__name__)


def xy_to_k(x, y):
    return f'{x:.1f}:{y:.1f}'


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path

    @property
    def config(self) -> dict:
        return JSONFile(self.config_path).read()

    @property
    def anchor_idx(self) -> dict:
        return self.config['anchor_idx']

    @property
    def anchor_loc_list(self) -> list[float]:
        return list(self.anchor_idx.values())

    @property
    def line_list(self) -> list[dict]:
        return self.config['line_list']

    @cached_property
    def node_idx_unsorted(self):
        node_idx = copy.deepcopy(self.anchor_idx)

        for line in self.line_list:
            node_list = line['node_list']
            n = len(node_list)
            i_start, i_end = 0, 1
            while True:
                while node_list[i_end] not in node_idx:
                    print(node_list[i_end])
                    i_end += 1

                start, end = node_list[i_start], node_list[i_end]
                assert start in node_idx

                log.debug(f'{start} -> {end}')
                start_loc = node_idx[start]
                end_loc = node_idx[end]
                span = i_end - i_start

                for i in range(i_start + 1, i_end):
                    node = node_list[i]
                    if node in node_idx:
                        log.warning(f'{node} already in node_idx')
                        continue

                    q = (i - i_start) * 1.0 / span
                    p = 1 - q

                    x = round(p * start_loc[0] + q * end_loc[0], 0)
                    y = round(p * start_loc[1] + q * end_loc[1], 0)

                    node_idx[node] = [x, y]

                    log.debug([span, i, q, node, x, y, start_loc, end_loc])

                i_start = i_end
                i_end += 1
                if i_end >= n:
                    break

        return node_idx

    @cache
    def get_node_cmp_value(self, node):
        if node in self.junction_list:
            return 0
        if node in self.terminal_list:
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
    def node_to_color_set(self):
        node_to_color_set = {}
        for line in self.line_list:
            node_list = line['node_list']
            color = line['color']
            for node in node_list:
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
    def get_node_text_angle(used_ks, x, y):
        for dx, dy, angle in ANGLE_CONFIG:
            x1, y1 = x + dx, y + dy
            k1 = xy_to_k(x1, y1)
            if k1 in used_ks:
                continue

            used_ks.add(k1)
            return used_ks, angle
        return used_ks, None

    @cached_property
    def node_to_text_angle(self):
        used_ks = set()

        for node, (x, y) in self.node_idx.items():
            used_ks.add(xy_to_k(x, y))

        node_to_text_angle = {}
        for node, (x, y) in self.node_idx.items():
            used_ks, text_angle = Config.get_node_text_angle(used_ks, x, y)
            node_to_text_angle[node] = text_angle

            logger = log.error if text_angle is None else log.debug
            logger(f'{node} {text_angle}')

        return node_to_text_angle

    @cached_property
    def node_to_neighbors(self):
        node_to_neighbors = {}
        for line in self.line_list:
            node_list = line['node_list']
            for i in range(len(node_list) - 1):
                node1, node2 = node_list[i], node_list[i + 1]
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
