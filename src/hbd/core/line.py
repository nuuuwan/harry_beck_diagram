import copy
import re
from functools import cached_property

from utils import Log

log = Log('Line')


class Line:
    def __init__(self, color: str, station_list: list[str], path: str):
        self.color = color
        self.station_list = station_list
        self.path = path

    @cached_property
    def direction_list(self):
        direction_list = []
        total_n_steps = 0
        for segment in self.path.split(' '):
            if segment == '':
                continue

            n_steps = int(re.findall('\\d+', segment)[0])
            direction = re.findall('[A-Z]+', segment)[0]
            direction_list.append([n_steps, direction])
            total_n_steps += n_steps

        if total_n_steps != len(self.station_list) - 1:
            log.error(
                f'Invalid {str(direction_list)} for {str(self.station_list)}'
            )
        return direction_list

    def copy(self):
        return Line(
            color=self.color,
            station_list=copy.deepcopy(self.station_list),
            path=self.path,
        )
