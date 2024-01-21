from hbd import Draw, Line, Network, Styler

config = Network(
    title='Simplified Roadmap',
    subtitle="Colombo, Sri Lanka",
    footer_text='Not to scale.',
    line_idx={
        'Baseline Rd': Line(
            color="black",
            station_list=[
                "Peliyagoda",
                "Dematagoda",
                "Baseline Rd + A0",
                "Borella Junction",
                "Kanatta",
                "Kirula",
                "Pamankada",
            ],
            path="6S",
        ),
        'A0': Line(
            color="green",
            station_list=[
                "Baseline Rd + A0",
                "Rajagiriya",
                "Battaramulla",
            ],
            path="2E",
        ),
    },
)

styler = Styler(DIM=2000)

Draw(config, styler).draw('images/lk_cmb_roads.png')
