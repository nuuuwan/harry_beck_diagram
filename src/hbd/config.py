import copy
from functools import cached_property

from utils import JSONFile, Log

log = Log(__name__)


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
    def node_idx(self):
        node_idx = copy.deepcopy(self.anchor_idx)

        for line in self.line_list:
            node_list = line['node_list']
            start, end = node_list[0], node_list[-1]
            start_loc = node_idx[start]
            end_loc = node_idx[end]

            n = len(node_list)
            for i in range(1, n - 1):
                q = (i) / (n - 1)
                p = 1 - q
                node = node_list[i]
                node_idx[node] = [
                    int(p * start_loc[0] + q * end_loc[0]),
                    int(p * start_loc[1] + q * end_loc[1]),
                ]

        return node_idx

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

    @cached_property
    def node_to_text_angle(self):
        def xy_to_k(x, y):
            return f'{x:.1f}:{y:.1f}'

        used_ks = set()

        for node, (x, y) in self.node_idx.items():
            used_ks.add(xy_to_k(x, y))

        node_to_text_angle = {}
        for i_junction in [0, 1, 2]:
            for node, (x, y) in self.node_idx.items():
                is_node_junction = node in self.junction_list
                is_node_district_capital = node[:3] == node.upper()[:3]
                if i_junction == 0 and not is_node_junction:
                    continue

                if i_junction == 1 and not (
                    not is_node_junction and is_node_district_capital
                ):
                    continue

                if i_junction == 2 and not (
                    not is_node_junction and not is_node_district_capital
                ):
                    continue

                node_to_text_angle[node] = None

                for dx, dy, angle in [
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
                ]:
                    x1, y1 = x + dx, y + dy
                    k1 = xy_to_k(x1, y1)
                    if k1 not in used_ks:
                        used_ks.add(k1)
                        node_to_text_angle[node] = angle
                        break

                if node_to_text_angle[node] is None:
                    log.error(f'Could not find text angle for node {node}')

        return node_to_text_angle
