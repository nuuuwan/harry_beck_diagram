class Line:
    def __init__(
        self, color: str, node_list: list[str], direction_list: list
    ):
        self.color = color
        self.node_list = node_list
        self.direction_list = direction_list

    @staticmethod
    def from_dict(d: dict):
        color = d['color']
        node_list = d['node_list']
        direction_list = d['direction_list']
        return Line(color, node_list, direction_list)
