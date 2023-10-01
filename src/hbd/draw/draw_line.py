import svgpathtools
from utils import Log
from utils import xmlx
_ = xmlx._

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
            self.styler.line_end_blip
            | dict(
                x=sx_end - self.styler.RADIUS * krx,
                y=sy_end - self.styler.RADIUS * kry,
                width=self.styler.RADIUS * 2 * kwidth,
                height=self.styler.RADIUS * 2 * kheight,
                fill=color,
            ),
        )

    def draw_line_polyline(self, points, color):
        d_str_list = []
        n = len(points)
        for i in range(n):
            x, y = points[i]
            if i == 0:
                d_str = f'M{x} {y}'
            else:
                d_str = f'L{x} {y}'
            d_str_list.append(d_str)
        d = ' '.join(d_str_list)
        path = svgpathtools.parse_path(d)
        smoothed_path = svgpathtools.smoothed_path(
            path, maxjointsize=self.styler.svg['width'], tightness=1
        )
        d = smoothed_path.d()

        return _(
            'path',
            None,
            self.styler.line_path
            | dict(
                d=d,
                stroke=color,
            ),
        )

    def draw_line(self, line, t):
        station_list = line.station_list
        color = line.color
        points = []
        x0, y0 = None, None
        for node in station_list:
            x, y = self.config.node_idx[node]
            sx, sy = t(x, y)
            points.append([sx, sy])
            if x0 is not None:
                dx, dy = x - x0, y - y0
                if [abs(dx), abs(dy)] not in [[1.0, 0], [0, 1.0], [1.0, 1.0]]:
                    log.warning(f'Invalid jump: {node} ({dx}, {dy})')
            x0, y0 = x, y

        x_end, y_end = self.config.node_idx[station_list[-1]]
        x_end2, y_end2 = self.config.node_idx[station_list[-2]]
        sx_end, sy_end = t(x_end, y_end)
        sx_end2, sy_end2 = t(x_end2, y_end2)
        return _(
            'g',
            [
                self.draw_line_polyline(points, color),
                self.draw_line_blip(sx_end2, sx_end, sy_end, color),
            ],
        )
