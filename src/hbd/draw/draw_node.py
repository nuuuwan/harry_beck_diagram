from utils import Log, xmlx

from hbd.core.DISTRICT_CAPITAL_LIST import DISTRICT_CAPITAL_LIST

_ = xmlx._


log = Log(__name__)


class DrawNode:
    def draw_node_circle(self, sx, sy):
        return _(
            'circle',
            None,
            self.styler.node_circle
            | dict(
                cx=sx,
                cy=sy,
            ),
        )

    @staticmethod
    def get_transform(sx, sy, text_angle):
        return ' '.join(
            [
                f'translate({sx},{sy})',
                f'rotate({-text_angle})',
                f'translate({-sx},{-sy})',
            ]
        )

    def draw_node_text(self, sx, sy, node, x, y, text_angle):
        text_anchor = 'start'
        space_dir = 1
        if 90 < text_angle <= 270:
            text_anchor = 'end'
            space_dir = -1
            text_angle -= 180
        transform = DrawNode.get_transform(sx, sy, text_angle)
        label = node

        cmp = self.config.get_node_cmp_value(node)
        default_font_size = int(self.styler.node_text['font_size'])
        font_size = default_font_size * [1.4, 1.2, 1.1, 1][cmp]
        fill = 'black' if cmp < 2 else 'gray'

        for district_name in DISTRICT_CAPITAL_LIST:
            if district_name in label:
                label = label.replace(district_name, district_name.upper())

        return _(
            'text',
            label,
            self.styler.node_text
            | dict(
                x=sx
                + space_dir * (self.styler.RADIUS * 1.5 + font_size * 0.5),
                y=sy,
                text_anchor=text_anchor,
                transform=transform,
                font_size=font_size,
                fill=fill,
            ),
        )

    def draw_node(self, node, x, y, t):
        sx, sy = t(x, y)
        inner_list = []
        text_angle = self.config.node_to_text_angle[node]

        if node in self.config.junction_list:
            inner_list.append(self.draw_node_circle(sx, sy))
        # else:
        #     if node not in self.config.terminal_list:
        #         inner_list.append(
        #             self.draw_node_blip(sx, sy, node, text_angle)
        #         )

        if text_angle is not None:
            inner_list.append(
                self.draw_node_text(sx, sy, node, x, y, text_angle)
            )

        return _(
            'g',
            inner_list,
        )
