from functools import cache, cached_property

from utils import Log
from utils.xmlx import _

from hbd.config import Config
from hbd.STYLE import RADIUS, STYLE

log = Log(__name__)


class Draw(Config):
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
        x_span = max_x - min_x
        y_span = max_y - min_y
        max_span = max(x_span, y_span)

        padding = STYLE.SVG['padding']
        inner_width = STYLE.SVG['width'] - 2 * padding
        inner_height = STYLE.SVG['height'] - 2 * padding

        def t(x: float, y: float) -> list[int]:
            px = (x - min_x) / max_span
            py = (y - min_y) / max_span
            sx = int(px * inner_width + padding)
            sy = int((1 - py) * inner_height + padding)
            return sx, sy

        return t

    def draw_node(self, label, x, y, t):
        log.debug(f"({x},{y}) {label}")
        sx, sy = t(x, y)
        inner_list = []

        if label in self.junction_list:
            inner_list.append(
                _(
                    'circle',
                    None,
                    STYLE.NODE_CIRCLE
                    | dict(
                        cx=sx,
                        cy=sy,
                        r=RADIUS * 2,
                    ),
                ),
            )
        inner_list.append(
            _(
                'circle',
                None,
                STYLE.NODE_CIRCLE
                | dict(
                    cx=sx,
                    cy=sy,
                ),
            ),
        )

        angle = self.node_to_angle[label] + 270
        transform = f'translate({sx},{sy}) rotate(-{angle}) translate({-sx},{-sy})'
        inner_list.append(
            _(
                'text',
                label,
                STYLE.NODE_TEXT
                | dict(
                    x=sx + RADIUS * 2,
                    y=sy,
                    transform=transform,
                ),
            ),
        )
        return _(
            'g',
            inner_list,
        )

    def draw_nodes(self):
        t = self.get_t()
        nodes = []
        for label, (x, y) in self.node_idx.items():
            nodes.append(self.draw_node(label, x, y, t))
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
    log.debug(draw.node_to_angles)
