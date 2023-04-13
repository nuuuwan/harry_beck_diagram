from utils import Log
from utils.xmlx import _

from hbd.STYLE import RADIUS, STYLE

log = Log(__name__)


class DrawLine:
    def draw_line_blip(self, sx_start, sx_end, sy_end, color):
        dx = sx_end - sx_start

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
                if [abs(dx), abs(dy)] not in [[1.0,0], [0,1.0], [1.0,1.0]]: 
                    log.warning(f'Invalid jump: {node} ({dx}, {dy})')
            x0, y0 = x, y

        x_start, y_start = self.node_idx[node_list[0]]
        sx_start, sy_start = t(x_start, y_start)
        x_end, y_end = self.node_idx[node_list[-1]]
        sx_end, sy_end = t(x_end, y_end)

        return _(
            'g',
            [
                self.draw_line_polyline(points, color),
                self.draw_line_blip(sx_start, sx_end, sy_end, color),
            ],
        )
