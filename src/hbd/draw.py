import math
import os
import webbrowser
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

        padding = STYLE.SVG['padding']
        inner_width = STYLE.SVG['width'] - 2 * padding
        inner_height = STYLE.SVG['height'] - 2 * padding

        def t(x: float, y: float) -> list[int]:
            px = (x - min_x) / x_span
            py = (y - min_y) / y_span
            sx = int(px * inner_width + padding)
            sy = int((1 - py) * inner_height + padding)
            return sx, sy

        return t

    def draw_node_circle(self, sx, sy):
        return _(
                'circle',
                None,
                STYLE.NODE_CIRCLE
                | dict(
                    cx=sx,
                    cy=sy,
                    r=RADIUS * 2,
                ),
        )
        

    def draw_node_blip(self, sx, sy, node, text_angle):
        color = self.node_to_lines[node][0]

        dx = math.cos(math.radians(text_angle))
        dy = -math.sin(math.radians(text_angle))
        return _(
            'rect',
            None,
            STYLE.LINE_END_BLIP
            | dict(
                x=sx + RADIUS * (dx - 1),
                y=sy + RADIUS * (dy - 1),
                width=RADIUS * 2,
                height=RADIUS * 2,
                fill=color,
            ),
        )

    def draw_node_text(self, sx, sy, node, x, y, text_angle):
        text_anchor = 'start'
        space_dir = 1
        if 90 < text_angle <= 270:
            text_anchor = 'end'
            space_dir = -1
            text_angle -= 180

        transform = ' '.join(
            [
                f'translate({sx},{sy})',
                f'rotate(-{text_angle})',
                f'translate({-sx},{-sy})',
            ]
        )
        default_font_size = STYLE.NODE_TEXT['font_size']
        font_size = (
            int(default_font_size * 1.2)
            if (node in self.junction_list)
            else default_font_size
        )
        is_node_district_capital = node[:3] == node.upper()[:3]
        default_font_weight = STYLE.NODE_TEXT['font_weight']
        font_weight = default_font_weight

        return _(
                'text',
                f'{node} ({x}, {y})',
                STYLE.NODE_TEXT
                | dict(
                    x=sx + space_dir * (RADIUS * 1.5 + font_size * 0.5),
                    y=sy,
                    text_anchor=text_anchor,
                    transform=transform,
                    font_size=font_size,
                    font_weight=font_weight,
                ),
        )
        

    def draw_node(self, node, x, y, t):
        sx, sy = t(x, y)
        inner_list = []
        text_angle = self.node_to_text_angle[node]

        if node in self.junction_list:
            inner_list.append(self.draw_node_circle(sx, sy))
        else:
            if node not in self.terminal_list:
                inner_list.append(
                    self.draw_node_blip(sx, sy, node, text_angle)
                )

        if text_angle is not None:
            inner_list.append(
                self.draw_node_text(sx, sy, node, x, y, text_angle)
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

    def draw_line_blip(self, sx_end, sy_end, dx, color):
        sx1, sy1 = sx_end, sy_end
        if dx != 0:
            return _(
                'rect',
                None,
                STYLE.LINE_END_BLIP
                | dict(
                    x=sx1 - RADIUS,
                    y=sy1 - RADIUS * 2,
                    width=RADIUS * 2,
                    height=RADIUS * 4,
                    fill=color,
                ),
            )
        return _(
            'rect',
            None,
            STYLE.LINE_END_BLIP
            | dict(
                x=sx1 - RADIUS * 2,
                y=sy1 - RADIUS,
                width=RADIUS * 4,
                height=RADIUS * 2,
                fill=color,
            ),
        )

    def draw_line_polyline(self, points, color):
        return _(
            'polyline',
            None,
            STYLE.LINE_POLYLINE
            | dict(
                points=' '.join(points),
                stroke=color,
            ),
        )

    def draw_line(self, line, t):
        node_list = line['node_list']
        color = line['color']
        points = []
        for node in node_list:
            x, y = self.node_idx[node]
            sx, sy = t(x, y)
            points.append(f'{sx},{sy}')

        x_start, y_start = self.node_idx[node_list[0]]
        sx_start, sy_start = t(x_start, y_start)
        x_end, y_end = self.node_idx[node_list[-1]]
        sx_end, sy_end = t(x_end, y_end)
        dx, dy = sx_end - sx_start, sy_end - sy_start

        return _(
            'g',
            [
                self.draw_line_polyline(points, color),
                self.draw_line_blip(sx_end, sy_end, dx, color),
            ],
        )

    def draw_lines(self):
        t = self.get_t()
        lines = []
        for line in self.line_list:
            lines.append(self.draw_line(line, t))
        return lines

    def draw(self):
        rect = _('rect', None, STYLE.RECT_BORDER)
        svg = _(
            'svg',
            [rect] + self.draw_lines() + self.draw_nodes(),
            STYLE.SVG,
        )
        svg.store(self.svg_path)
        log.debug(f'Saved {self.svg_path}')

        webbrowser.open(os.path.abspath(self.svg_path))


if __name__ == '__main__':
    config_path = 'data/lk_rail.json'

    draw = Draw(config_path)
    draw.draw()
