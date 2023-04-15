if __name__ == '__main__':
    import os

    from hbd import Config, Draw, Styler

    for file_name in os.listdir('data/lk_rail_history'):
        if not file_name.endswith('.json'):
            continue
        draw = Draw(
            Config(f'data/lk_rail_history/{file_name}'), Styler(DIM=1000)
        )
        draw.draw()
