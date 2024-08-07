import os
import webbrowser
from functools import cache

import imageio
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from utils import Log, _

from hbd.core import bbox_utils
from hbd.draw.DrawLine import DrawLine
from hbd.draw.DrawNode import DrawNode

log = Log(__name__)


class Draw(DrawNode, DrawLine):
    def __init__(self, config, styler):
        self.config = config
        self.styler = styler

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
        for line in self.config.line_idx.values():
            lines.append(self.draw_line(line, t))
        return lines

    def draw_title(self):
        self.config.title
        return _('text', self.config.title, self.styler.text_title)

    def draw_subtitle(self):
        return _('text', self.config.subtitle, self.styler.text_subtitle)

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

    def draw_watermark(self):
        return _(
            'text',
            '@nuuuwan',
            self.styler.text_watermark,
        )

    def draw(self, png_path, do_open=True):
        svg = _(
            'svg',
            [
                self.draw_watermark(),
                self.draw_title(),
                self.draw_subtitle(),
                self.draw_footer_text(),
            ]
            + self.draw_lines()
            + self.draw_nodes(),
            self.styler.svg,
        )
        svg_path = png_path[:-3] + 'svg'
        svg.store(svg_path)
        log.debug(f'Saved {svg_path}')

        png_path = Draw.convert_svg_to_png(svg_path)
        if do_open:
            webbrowser.open(os.path.abspath(png_path))
        return png_path

    @staticmethod
    def convert_svg_to_png(svg_path):
        png_path = svg_path[:-3] + 'png'

        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        log.info(f'Saved {png_path}')

        return png_path

    @staticmethod
    def build_animated_gif(png_path_list, gif_path):
        png_path_list.sort()
        last_png_path = png_path_list[-1]
        for i in range(0, 5):
            png_path_list.append(last_png_path)

        images = []
        for png_path in png_path_list:
            images.append(imageio.imread(png_path))
        DURATION = 55.70 / 24
        imageio.mimwrite(gif_path, images, duration=DURATION)
        log.info(f'Built {gif_path} (from {len(png_path_list)} png files)')
        webbrowser.open(os.path.abspath(gif_path))
