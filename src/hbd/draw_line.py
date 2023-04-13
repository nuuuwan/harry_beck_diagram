from utils import Log
from utils.xmlx import _

from hbd.STYLE import RADIUS, STYLE

log = Log(__name__)


class DrawLine:
    def draw_line_blip(self, sx_end2, sx_end, sy_end, color):
        dx = sx_end - sx_end2

        sx=sx_end - RADIUS * 2
        sy=sy_end - RADIUS * 2
        text_angle = 0

        transform = ' '.join(
            [
                f'translate({sx},{sy})',
                f'rotate(-{text_angle})',
                f'translate({-sx},{-sy})',
            ]
        )

        return _(
            'rect',
            None,
            STYLE.LINE_END_BLIP
            | dict(
                x=sx,
                y=sy,
                width=RADIUS *4,
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
        x0, y0 = None, None
        for node in node_list:
            x, y = self.node_idx[node]
            sx, sy = t(x, y)
            points.append(f'{sx},{sy}')
            if x0 is not None:
                dx, dy = x - x0, y - y0
                if [abs(dx), abs(dy)] not in [[1.0, 0], [0, 1.0], [1.0, 1.0]]:
                    log.warning(f'Invalid jump: {node} ({dx}, {dy})')
            x0, y0 = x, y

        x_start, y_start = self.node_idx[node_list[0]]
        sx_start, sy_start = t(x_start, y_start)
        x_end, y_end = self.node_idx[node_list[-1]]
        x_end2, y_end2 = self.node_idx[node_list[-1]]
        sx_end, sy_end = t(x_end, y_end)
        sx_end2, sy_end2 = t(x_end2, y_end2)
        return _(
            'g',
            [
                self.draw_line_polyline(points, color),
                self.draw_line_blip(sx_end2, sx_end, sy_end, color),
            ],
        )
