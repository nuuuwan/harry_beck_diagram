from hbd.STYLE import STYLE


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

    padding = STYLE.SVG['padding']
    inner_width = STYLE.SVG['width'] - 2 * padding
    inner_height = STYLE.SVG['height'] - 2 * padding

    def t(x: float, y: float) -> list[int]:
        px = (x - min_x) / x_span
        py = (y - min_y) / y_span
        sx = int(px * inner_width + padding)
        sy = int((1 - py) * inner_height + padding)
        return sx, sy

    return t
