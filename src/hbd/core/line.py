import copy
import re
from functools import cached_property

from utils import Log

log = Log("Line")


class Line:
    def __init__(self, color: str, station_list: list[str], path: str):
        self.color = color
        self.station_list = station_list
        self.path = path

    @staticmethod
    def path_to_direction_list(path: str) -> list[list[int, str]]:
        direction_list = []
        for segment in path.split(" "):
            if segment == "":
                continue

            n_steps = int(re.findall("\\d+", segment)[0])
            direction = re.findall("[A-Z]+", segment)[0]
            for _ in range(n_steps):
                direction_list.append(direction)

        return direction_list

    @staticmethod
    def direction_list_to_path(direction_list: list[list[int, str]]) -> str:
        path_segments = []
        prev_direction = None
        step_in_current_direction = 0
        for direction in direction_list:
            if direction == prev_direction:
                step_in_current_direction += 1
            else:
                if prev_direction is not None:
                    path_segments.append(
                        f"{step_in_current_direction}{prev_direction}"
                    )
                prev_direction = direction
                step_in_current_direction = 1

        if prev_direction is not None:
            path_segments.append(
                f"{step_in_current_direction}{prev_direction}"
            )
        return " ".join(path_segments)

    @cached_property
    def direction_list(self):
        direction_list = Line.path_to_direction_list(self.path)
        assert len(self.station_list) - 1 == len(direction_list), (
            "Mismatch between station list and path:"
            + f" {direction_list} vs {self.station_list}"
        )
        compressed_path = Line.direction_list_to_path(direction_list)
        compressed_direction_list = Line.path_to_direction_list(
            compressed_path
        )

        assert len(self.station_list) - 1 == len(compressed_direction_list), (
            "Mismatch between station list and path:"
            + f" {compressed_direction_list} vs {self.station_list}"
        )

        return compressed_direction_list

    def copy(self):
        return Line(
            color=self.color,
            station_list=copy.deepcopy(self.station_list),
            path=self.path,
        )
