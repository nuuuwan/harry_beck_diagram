from functools import cached_property

import svglib.svglib as svglib


DEFAULT_FONT_FAMILY = 'GIL_____'
DEFAULT_FONT_PATH = 'C:\\Windows\\Fonts\\GIL_____.TTF'

svglib.register_font(DEFAULT_FONT_FAMILY, DEFAULT_FONT_PATH, weight='normal', style='normal')


class Styler:
    def __init__(
        self,
        RADIUS=4,
        DIM=700,
        OPACITY=1,
        PADDING=200,
        FONT_FAMILY=DEFAULT_FONT_FAMILY,
        FONT_SIZE=15,
    ):
        self.RADIUS = RADIUS
        self.DIM = DIM
        self.OPACITY = OPACITY
        self.PADDING = PADDING
        self.FONT_FAMILY = FONT_FAMILY
        self.FONT_SIZE = FONT_SIZE

    @cached_property
    def svg(self):
        return dict(
            width=self.DIM,
            height=self.DIM,
            padding=self.PADDING,
        )

    @cached_property
    def text_title(self):
        return dict(
            fill='gray',
            stroke='none',
            font_size=self.FONT_SIZE * 4,
            font_family=self.FONT_FAMILY,
            x=self.DIM / 2,
            y=self.PADDING / 2 + self.FONT_SIZE,
            text_anchor='middle',
            dominant_baseline='hanging',
        )

    @cached_property
    def text_footer_text(self):
        return dict(
            fill='gray',
            stroke='none',
            font_size=self.FONT_SIZE,
            font_family=self.FONT_FAMILY,
            x=self.DIM / 2,
            y=self.DIM - (self.PADDING / 2 + self.FONT_SIZE),
            text_anchor='middle',
            dominant_baseline='text-top',
        )

    @cached_property
    def rect_border(self):
        return dict(
            x=self.PADDING / 2,
            y=self.PADDING / 2,
            width=self.DIM - self.PADDING,
            height=self.DIM - self.PADDING,
            fill='white',
            stroke='gray',
        )

    @cached_property
    def node_circle(self):
        return dict(
            r=self.RADIUS * 2,
            fill='white',
            stroke='black',
            stroke_width=self.RADIUS * 0.5,
        )

    @cached_property
    def node_text(self):
        return dict(
            fill='black',
            stroke='none',
            font_size=self.FONT_SIZE,
            font_family=self.FONT_FAMILY,
            font_weight="100",
            text_anchor='start',
            dominant_baseline='central',
        )

    @cached_property
    def line_end_blip(self):
        return dict(stroke="none", fill_opacity=self.OPACITY)

    @cached_property
    def line_path(self):
        return dict(
            fill='none',
            stroke_width=self.RADIUS * 2.1,
            stroke_opacity=self.OPACITY,
        )
