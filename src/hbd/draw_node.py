import math

from utils import Log
from utils.xmlx import _

from hbd.STYLE import RADIUS, STYLE
from hbd.DISTRICT_CAPITAL_LIST import DISTRICT_CAPITAL_LIST

log = Log(__name__)


class DrawNode:
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
        color = self.node_to_color_set[node].pop()

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
        default_font_size = int(STYLE.NODE_TEXT['font_size'])
        default_font_weight = int(STYLE.NODE_TEXT['font_weight'])
        
        label = node
        log.debug(f'{node} ({x}, {y})')
        cmp = self.get_node_cmp_value(node)

        font_size = default_font_size * (1 + (3- cmp) * 0.2)
        font_weight = default_font_weight * (1 + (3 - cmp) * 0.2)

        for district_name in DISTRICT_CAPITAL_LIST:
            if district_name in label:
                label = label.replace(district_name, district_name.upper())

        return _(
            'text',
            label,
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
