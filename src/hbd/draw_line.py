from utils import Log
from utils.xmlx import _

from hbd.STYLE import RADIUS, STYLE

log = Log(__name__)


class DrawLine:
    def draw_line_blip(self, sx_end2, sx_end, sy_end, color):
        dx = sx_end - sx_end2

        krx, kry, kwidth, kheight = 1, 1, 1, 1
        if dx != 0:
            kry = 2
            kheight = 2
        else:
            krx = 2
            kwidth = 2

        return _(
            'rect',
            None,
            STYLE.LINE_END_BLIP
            | dict(
                x=sx_end - RADIUS * krx,
                y=sy_end - RADIUS * kry,
                width=RADIUS * 2 * kwidth,
                height=RADIUS * 2 * kheight,
                fill=color,
            ),
        )

    def draw_line_polyline(self, points, color):
        d_str_list = []
        prev_x, prev_y = None, None
        for x,y in points:
            if prev_x is None:
                d_str = f'M{x} {y}'
            else:
                x1 ,y1 = (x + prev_x) / 2, (y + prev_y) / 2
                x2, y2 = x1, y1
                d_str = f'S{x1} {y1} {x} {y}'

            d_str_list.append(d_str)
            prev_x, prev_y = x, y
        d = ' '.join(d_str_list)
        return _(
            'path',
            None,
            STYLE.LINE_PATH
            | dict(
                d=d,
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
            points.append([sx, sy])
            if x0 is not None:
                dx, dy = x - x0, y - y0
                if [abs(dx), abs(dy)] not in [[1.0, 0], [0, 1.0], [1.0, 1.0]]:
                    log.warning(f'Invalid jump: {node} ({dx}, {dy})')
            x0, y0 = x, y

        x_end, y_end = self.node_idx[node_list[-1]]
        x_end2, y_end2 = self.node_idx[node_list[-2]]
        sx_end, sy_end = t(x_end, y_end)
        sx_end2, sy_end2 = t(x_end2, y_end2)
        return _(
            'g',
            [
                self.draw_line_polyline(points, color),
                self.draw_line_blip(sx_end2, sx_end, sy_end, color),
            ],
        )
