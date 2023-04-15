import os
import webbrowser
from functools import cache

from utils import Log
from utils.xmlx import _

from hbd import bbox_utils
from hbd.draw_line import DrawLine
from hbd.draw_node import DrawNode

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
        

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
        font_size = min(
            self.styler.text_title['font_size'],
            self.styler.svg['width'] / len(title),
        )
        return _(
            'text', title, self.styler.text_title | dict(font_size=font_size)
        )

    def draw_footer_text(self):
        footer_text = self.config.footer_text
        font_size = min(
            self.styler.text_footer_text['font_size'],
            self.styler.svg['width'] / len(footer_text),
        )
        return _(
            'text',
            footer_text,
            self.styler.text_footer_text | dict(font_size=font_size),
        )

    def draw(self):
        svg = _(
            'svg',
            [
                self.draw_title(),
                self.draw_footer_text(),
            ]
            + self.draw_lines()
            + self.draw_nodes(),
            self.styler.svg,
        )
        svg.store(self.svg_path)
        log.debug(f'Saved {self.svg_path}')

       

        Draw.convert_svg_to_png(self.svg_path)


    @staticmethod
    def convert_svg_to_png(svg_path):
        png_path = svg_path[:-3] + 'png'
        
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        log.debug(f'Saved {png_path}')

        webbrowser.open(os.path.abspath(png_path))