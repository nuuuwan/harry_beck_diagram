from hbd.STYLE import STYLE
from utils import Log
log = Log(__name__)

def get_bbox(anchor_loc_list: list) -> tuple[float, float, float, float]:
    x0, y0 = anchor_loc_list[0]
    min_x, min_y, max_x, max_y = x0, y0, x0, y0
    for x, y in anchor_loc_list:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return min_x, min_y, max_x, max_y


def get_t(anchor_loc_list: list):
    min_x, min_y, max_x, max_y = get_bbox(anchor_loc_list)
    x_span = max_x - min_x
    y_span = max_y - min_y
    max_span = max(x_span, y_span)
    log.debug(f'{x_span=}, {y_span=}')

    padding = STYLE.SVG['padding']
    diagram_width = STYLE.SVG['width'] - 2 * padding
    diagram_height = STYLE.SVG['height'] - 2 * padding

    inner_width = diagram_width * x_span / max_span
    inner_height = diagram_height * y_span / max_span
    padding_x = (diagram_width - inner_width) / 2
    padding_y = (diagram_height - inner_height) / 2

    def t(x: float, y: float) -> list[int]:
        px = (x - min_x) / x_span
        py = (y - min_y) / y_span
        sx = int(px * inner_width + padding_x + padding)
        sy = int((1 - py) * inner_height + padding_y + padding)
        return sx, sy

    return t
