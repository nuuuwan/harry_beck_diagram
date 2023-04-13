from hbd.STYLE import STYLE


def get_bbox(anchor_loc_list: list) -> tuple[float, float, float, float]:
    min_x, min_y, max_x, max_y = None, None, None, None
    for x, y in anchor_loc_list:
        if min_x is None or x < min_x:
            min_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_x is None or x > max_x:
            max_x = x
        if max_y is None or y > max_y:
            max_y = y
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
