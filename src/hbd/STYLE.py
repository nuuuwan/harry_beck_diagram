RADIUS = 5
DIM = 1000


class STYLE:
    SVG = dict(
        width=DIM,
        height=DIM,
        padding=50,
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
        text_anchor='start',
        font_family='Arial',
        font_weight="600",
        alignment_baseline='middle',
    )

    LINE_POLYLINE = dict(
        fill='none',
        stroke_width=RADIUS * 2.1,
    )
