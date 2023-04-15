from hbd import Config, Line, Styler, Draw

config = Config(
    title='Topographical Map of Railways in Sri Lanka',
    footer_text='Not to scale.',
    line_list=[
        Line(
            color="red",
            station_list=[
                "Colombo Fort",
                "Maradana",
                "Ragama",
                "Gampaha",
                "Polgahawela",
                "Peradeniya",
                "Badulla",
            ],
            path="6E",
        )
    ],
)

styler = Styler(DIM = 1000)

Draw(config, styler).draw('images/lk_rail_topo.png')