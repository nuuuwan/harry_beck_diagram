RADIUS = 3
DIM = 2000
OPACITY = 1
PADDING = 50


class STYLE:
    SVG = dict(
        width=DIM,
        height=DIM,
        padding=PADDING,
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
        r=RADIUS,
        fill='white',
        stroke='black',
        stroke_width=RADIUS * 0.7,
    )
    NODE_TEXT = dict(
        fill='black',
        stroke='none',
        font_size=10,
        font_family='Trebuchet MS',
        font_weight="100",
        text_anchor='start',
        dominant_baseline='central',
    )

    LINE_END_BLIP = dict(stroke="none", fill_opacity=OPACITY)

    LINE_POLYLINE = dict(
        fill='none',
        stroke_width=RADIUS * 2.1,
        stroke_opacity=OPACITY,
    )
