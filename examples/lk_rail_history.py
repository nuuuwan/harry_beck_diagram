from hbd import Draw, Line, Network, Styler

config_idx = {}

config_idx['1864'] = Network(
    title='1864',
    footer_text='History of the Railways in Sri Lanka',
    line_idx={
        'Main': Line(
            color="red",
            station_list=[
                "Colombo Fort",
                "Maradana",
                "Ragama",
                "Gampaha",
                "Ambepussa",
            ],
            path="4NE",
        )
    },
)

config_idx['1867'] = config_idx['1864'].copy(title="1867")
config_idx['1867'].line_idx['main'].station_list += ["Polgahawela", "Peradeniya"]
config_idx['1867'].line_idx['main'].path += " 2E"

styler = Styler(DIM=1300)

png_path_list = []
for year, config in config_idx.items():
    draw = Draw(config, styler)
    png_path = f'images/lk_rail_history/{year}.png'
    png_path = draw.draw(png_path)
    png_path_list.append(png_path)

Draw.build_animated_gif(png_path_list, 'images/lk_rail_history/timeline.gif')
