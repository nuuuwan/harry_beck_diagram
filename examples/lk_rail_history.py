if __name__ == '__main__':
    import os
    import webbrowser

    from hbd import Config, Draw, Styler

    png_path_list = []
    for file_name in os.listdir('data/lk_rail_history'):
        if not file_name.endswith('.json'):
            continue
        draw = Draw(
            Config(f'data/lk_rail_history/{file_name}'), Styler(DIM=1000)
        )
        png_path = draw.draw()
        png_path_list.append(png_path)

        if len(png_path_list) >= 2:
            break

    gif_path = 'data/lk_rail_history/timeline.gif'
    Draw.create_animated_gif(png_path_list, gif_path)
    webbrowser.open(os.path.abspath(gif_path))
