RADIUS = 3
DIM = 700
OPACITY = 1
PADDING = 200
FONT_FAMILY = 'Trebuchet MS'
FONT_SIZE = 12

class STYLE:
    SVG = dict(
        width=DIM,
        height=DIM,
        padding=PADDING,
    )

    TEXT_TITLE = dict(
        fill='gray',
        stroke='none',
        font_size=FONT_SIZE*4,
        font_family=FONT_FAMILY,
        x=DIM / 2,
        y=PADDING * 2,
        text_anchor='middle',
    )

    RECT_BORDER = dict(
        x=PADDING / 2,
        y=PADDING / 2,
        width=DIM - PADDING,
        height=DIM - PADDING,
        fill='white',
        stroke='gray',
    )
    NODE_CIRCLE = dict(
        r=RADIUS*2,
        fill='white',
        stroke='black',
        stroke_width=RADIUS * 0.7,
    )
    NODE_TEXT = dict(
        fill='black',
        stroke='none',
        font_size=FONT_SIZE,
        font_family=FONT_FAMILY,
        font_weight="100",
        text_anchor='start',
        dominant_baseline='central',
    )

    LINE_END_BLIP = dict(stroke="none", fill_opacity=OPACITY)

    LINE_PATH = dict(
        fill='none',
        stroke_width=RADIUS * 2.1,
        stroke_opacity=OPACITY,
    )
