from hbd import Draw, Line, Network, Styler

config = Network(
    title='Topographical Map of Railways',
    subtitle="Sri Lanka",
    footer_text='Not to scale.',
    line_idx={
        'Main': Line(
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
        ),
        'Coastal': Line(
            color="cyan",
            station_list=[
                "Colombo Fort",
                "Kalutara North",
                "Galle",
                "Matara",
                "Beliatta",
            ],
            path="4S",
        ),
        'Northern': Line(
            color="orange",
            station_list=[
                "Polgahawela",
                "Kurunegala",
                "Maho",
                "Anuradhapura",
                "Mihintale Junction",
                "Medavachchiya",
                "Vavuniya",
                "Kilinochchi",
                "Jaffna",
                "Kankesanthurai",
            ],
            path="9N",
        ),
        'Kelani Valley': Line(
            color="darkblue",
            station_list=["Maradana", "Avissawella"],
            path="1S",
        ),
        'Puttalam': Line(
            color="green",
            station_list=["Ragama", "Puttalam", "Periyanurvillu"],
            path="2N",
        ),
        'Matale': Line(
            color="purple",
            station_list=["Peradeniya", "Kandy", "Matale"],
            path="1N 1E",
        ),
        'Mihintale': Line(
            color="yellow",
            station_list=["Mihintale Junction", "Mihintale"],
            path="1E",
        ),
        'Mannar': Line(
            color="blue",
            station_list=["Medavachchiya", "Mannar", "Talaimannar Pier"],
            path="2W",
        ),
        'Batticaloa': Line(
            color="darkgreen",
            station_list=["Maho", "Galoya", "Polonnaruwa", "Batticaloa"],
            path="3E",
        ),
        'Trincomalee': Line(
            color="silver",
            station_list=["Galoya", "Trincomalee"],
            path="1N",
        ),
    },
)

styler = Styler(DIM=1300)

Draw(config, styler).draw('images/lk_rail_topo.png')
