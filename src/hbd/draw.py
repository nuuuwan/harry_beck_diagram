import copy
from functools import cache, cached_property

from utils import JSONFile, Log
from utils.xmlx import _

log = Log(__name__)

RADIUS = 5


class STYLE:
    SVG = dict(
        width=600,
        height=600,
        padding=50,
    )
    NODE_CIRCLE = dict(
        r=RADIUS,
        fill='white',
        stroke='black',
        stroke_width=RADIUS * 0.7,
    )
    NODE_TEXT = dict(
        fill='black',
        stroke='none',
        font_size=10,
        text_anchor='start',
        font_family='sans-serif',
        alignment_baseline='middle',
    )

    LINE_POLYLINE = dict(
        fill='none',
        stroke_width=RADIUS,
    )


class Draw:
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
                q = i / n
                p = 1 - q
                node = node_list[i]
                node_idx[node] = [
                    int(p * start_loc[0] + q * end_loc[0]),
                    int(p * start_loc[1] + q * end_loc[1]),
                ]

        return node_idx

    @property
    def svg_path(self) -> str:
        return self.config_path.replace('.json', '.svg')

    @cached_property
    def bbox(self) -> tuple[float, float, float, float]:
        min_x, min_y, max_x, max_y = None, None, None, None
        for x, y in self.anchor_loc_list:
            if min_x is None or x < min_x:
                min_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_x is None or x > max_x:
                max_x = x
            if max_y is None or y > max_y:
                max_y = y
        return min_x, min_y, max_x, max_y

    @cache
    def get_t(self):
        min_x, min_y, max_x, max_y = self.bbox
        padding = STYLE.SVG['padding']
        inner_width = STYLE.SVG['width'] - 2 * padding
        inner_height = STYLE.SVG['height'] - 2 * padding

        def t(x: float, y: float) -> list[int]:
            px = (x - min_x) / (max_x - min_x)
            py = (y - min_y) / (max_y - min_y)
            sx = int(px * inner_width + padding)
            sy = int((1 - py) * inner_height + padding)
            return sx, sy

        return t

    def draw_nodes(self):
        t = self.get_t()
        nodes = []
        for label, (x, y) in self.node_idx.items():
            sx, sy = t(x, y)
            nodes.append(
                _(
                    'g',
                    [
                        _(
                            'circle',
                            None,
                            STYLE.NODE_CIRCLE
                            | dict(
                                cx=sx,
                                cy=sy,
                            ),
                        ),
                        _(
                            'text',
                            label,
                            STYLE.NODE_TEXT
                            | dict(
                                x=sx + STYLE.NODE_CIRCLE['r'] * 1.5,
                                y=sy,
                            ),
                        ),
                    ],
                )
            )
        return nodes

    def draw_lines(self):
        t = self.get_t()
        lines = []
        for line in self.line_list:
            node_list = line['node_list']
            color = line['color']
            points = []
            for node in node_list:
                x, y = self.node_idx[node]
                sx, sy = t(x, y)
                points.append(f'{sx},{sy}')
            lines.append(
                _(
                    'polyline',
                    None,
                    STYLE.LINE_POLYLINE
                    | dict(
                        points=' '.join(points),
                        stroke=color,
                    ),
                )
            )
        return lines

    def draw(self):
        svg = _(
            'svg',
            self.draw_lines() + self.draw_nodes(),
            STYLE.SVG,
        )
        svg.store(self.svg_path)
        log.debug(f'Saved {self.svg_path}')


if __name__ == '__main__':
    draw = Draw('data/lk_rail.json')
    draw.draw()
