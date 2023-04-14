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


class Draw(Config, Styler, DrawNode, DrawLine):
    def __init__(self, config_path):
        Config.__init__(self, config_path)
        Styler.__init__(self)
        DrawNode.__init__(self)
        DrawLine.__init__(self)
    
    @property
    def svg_path(self) -> str:
        return self.config_path.replace('.json', '.svg')

    @cache
    def get_t(self):
        return bbox_utils.get_t(self, self.loc_list)

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
            lines.append(self.draw_line(line, t))
        return lines

    def draw_rect_border(self):
        return _('rect', None, self.rect_border)

    def draw_title(self):
        font_size = self.svg['width'] / len(self.title)
        return _('text', self.title, self.text_title | dict(font_size=font_size))

    def draw(self):
        svg = _(
            'svg',
            [self.draw_rect_border(), self.draw_title()]
            + self.draw_lines()
            + self.draw_nodes(),
            self.svg,
        )
        svg.store(self.svg_path)
        log.debug(f'Saved {self.svg_path}')

        webbrowser.open(os.path.abspath(self.svg_path))


if __name__ == '__main__':
    config_path = 'data/lk_rail_udupussellawa_closed.json'

    draw = Draw(config_path)
    draw.draw()
