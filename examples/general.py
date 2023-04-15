if __name__ == '__main__':
    from hbd import Config, Draw, Styler

    draw_list = [
        Draw(Config('data/lk_rail.json'), Styler(DIM=900)),
        Draw(Config('data/lk_rail_all.json'), Styler(DIM=2000)),
        Draw(Config('data/lk_rail_kv_closed.json'), Styler(DIM=700)),
        Draw(
            Config('data/lk_rail_udupussellawa_closed.json'), Styler(DIM=700)
        ),
        Draw(
            Config('data/lk_rail_wp_proposed.json'),
            Styler(DIM=800, PADDING=80),
        ),
        Draw(
            Config('data/lk_colombo_lrt_proposed.json'),
            Styler(DIM=1300, PADDING=150),
        ),
    ]
    for draw in draw_list:
        draw.draw()
