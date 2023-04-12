import copy
import math
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
    def node_to_neighbors(self):
        node_to_neighbors = {}
        for line in self.line_list:
            node_list = line['node_list']
            for i in range(len(node_list) - 1):
                node = node_list[i]
                neighbor = node_list[i + 1]
                if node not in node_to_neighbors:
                    node_to_neighbors[node] = set()
                node_to_neighbors[node].add(neighbor)

                if neighbor not in node_to_neighbors:
                    node_to_neighbors[neighbor] = set()
                node_to_neighbors[neighbor].add(node)

        return node_to_neighbors

    @cached_property
    def node_to_angles(self):
        node_to_angles = {}
        for node, neighbors in self.node_to_neighbors.items():
            angles = []
            for neighbor in neighbors:
                dx = self.node_idx[neighbor][0] - self.node_idx[node][0]
                dy = self.node_idx[neighbor][1] - self.node_idx[node][1]
                angle = abs(int(180 * math.atan2(dy, dx) / math.pi)) % 180
                angles.append(angle)
            node_to_angles[node] = angles
        return node_to_angles

    @cached_property
    def node_to_angle(self):
        node_to_angle = {}
        for node, angles in self.node_to_angles.items():
            angle = sum(angles) / len(angles)
            node_to_angle[node] = angle
        return node_to_angle