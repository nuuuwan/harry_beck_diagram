RADIUS = 4
DIM = 1000
OPACITY = 1


class STYLE:
    SVG = dict(
        width=DIM,
        height=DIM,
        padding=200,
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
