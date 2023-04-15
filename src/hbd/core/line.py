from functools import cached_property
import re


class Line:
    def __init__(
        self, color: str, node_list: list[str], path: str
    ):
        self.color = color
        self.node_list = node_list
        self.path = path
    
    @cached_property
    def direction_list(self):
        direction_list = []
        for segment in self.path.split(' '):
            if segment == '':
                continue

            n_steps = int(re.findall('\d+', segment)[0])
            direction = re.findall('[A-Z]+', segment)[0]
            direction_list.append([n_steps, direction])

        return direction_list
            