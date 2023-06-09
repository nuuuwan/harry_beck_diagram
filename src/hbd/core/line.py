import copy
import re
from functools import cached_property


class Line:
    def __init__(self, color: str, station_list: list[str], path: str):
        self.color = color
        self.station_list = station_list
        self.path = path

    @cached_property
    def direction_list(self):
        direction_list = []
        for segment in self.path.split(' '):
            if segment == '':
                continue

            n_steps = int(re.findall('\\d+', segment)[0])
            direction = re.findall('[A-Z]+', segment)[0]
            direction_list.append([n_steps, direction])

        return direction_list

    def copy(self):
        return Line(
            color=self.color,
            station_list=copy.deepcopy(self.station_list),
            path=self.path,
        )
