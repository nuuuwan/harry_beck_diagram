from utils import Log
from utils.xmlx import _

from hbd.STYLE import RADIUS, STYLE

log = Log(__name__)


class DrawLine:
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
