import os
import webbrowser
from functools import cache

from utils import Log
from utils.xmlx import _

from hbd import bbox_utils
from hbd.config import Config
from hbd.draw_line import DrawLine
from hbd.draw_node import DrawNode
from hbd.styler import Styler

log = Log(__name__)


class Draw(DrawNode, DrawLine):
    def __init__(self, config, styler):
        self.config = config
        self.styler = styler

    @property
    def svg_path(self) -> str:
        return self.config.config_path.replace('.json', '.svg')

    @cache
    def get_t(self):
        return bbox_utils.get_t(self.styler, self.config.loc_list)

    def draw_nodes(self):
        t = self.get_t()
        nodes = []
        for label, (x, y) in self.config.node_idx.items():
            nodes.append(self.draw_node(label, x, y, t))
        return nodes

    def draw_lines(self):
        t = self.get_t()
        lines = []
        for line in self.config.line_list:
            lines.append(self.draw_line(line, t))
        return lines

    def draw_rect_border(self):
        return _('rect', None, self.styler.rect_border)

    def draw_title(self):
        title = self.config.title
        font_size = self.styler.svg['width'] / len(title)
        return _(
            'text', title, self.styler.text_title | dict(font_size=font_size)
        )

    def draw(self):
        svg = _(
            'svg',
            [self.draw_rect_border(), self.draw_title()]
            + self.draw_lines()
            + self.draw_nodes(),
            self.styler.svg,
        )
        svg.store(self.svg_path)
        log.debug(f'Saved {self.svg_path}')

        webbrowser.open(os.path.abspath(self.svg_path))


if __name__ == '__main__':
    draw_list = [
        Draw(Config('data/lk_rail.json'), Styler(DIM=900)),
        Draw(Config('data/lk_rail_all.json'), Styler(DIM=2000)),
        Draw(Config('data/lk_rail_kv_closed.json'), Styler(DIM=700)),
        Draw(
            Config('data/lk_rail_udupussellawa_closed.json'), Styler(DIM=700)
        ),
    ]
    for draw in draw_list:
        draw.draw()
