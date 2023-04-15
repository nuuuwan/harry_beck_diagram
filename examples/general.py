import os
import webbrowser

# Draw(Config('data/lk_rail.json'), Styler(DIM=900)),
#         Draw(Config('data/lk_rail_all.json'), Styler(DIM=2000)),
#         Draw(Config('data/lk_rail_kv_closed.json'), Styler(DIM=700)),
#         Draw(
#             Config('data/lk_rail_udupussellawa_closed.json'), Styler(DIM=700)
#         ),
#         Draw(
#             Config('data/lk_rail_wp_proposed.json'),
#             Styler(DIM=800, PADDING=80),
#         ),
#         Draw(
#             Config('data/lk_colombo_lrt_proposed.json'),
#             Styler(DIM=1300, PADDING=150),
#         ),

if __name__ == '__main__':
    from hbd import Network, Draw, Styler

    config_path = 'data/lk_rail_history/max.json'
    png_path = config_path[:-4] + 'png'
    Draw(
        Network.from_file(config_path),
        Styler(DIM=1024, PADDING=128),
    ).draw(png_path)
    webbrowser.open(os.path.abspath(png_path))
