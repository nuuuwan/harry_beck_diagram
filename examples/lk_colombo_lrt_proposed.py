from hbd import Draw, Line, Network, Styler

config = Network(
    title="Proposed Light Rail Transit",
    subtitle="Colombo, Sri Lanka",
    footer_text=" ",
    line_idx={
        'LR1': Line(
            color="green",
            station_list=[
                "Fort",
                "Galle Face",
                "Gangaramaya",
                "Public Library",
                "Kollupitiya",
                "Mahanama",
                "Bambamapitiya",
                "Thummulla",
                "Royal",
                "Torrington",
                "BMICH",
                "Kanatta",
                "Borella Junction",
                "NHSL",
                "Townhall",
                "Union Place",
                "Maradana",
                "Pettah",
                "Fort",
            ],
            path="1SW 2S 1SW 1S 1SE 3E 2NE 1N 1NW 1SW 1NW 1NE 1NW 1W",
        ),
        'LR4': Line(
            color="purple",
            station_list=[
                "Borella Junction",
                "Cotta Rd",
                "Rajagiriya",
                "Battaramulla",
                "Udumulla",
                "Malabe",
            ],
            path="5E",
        ),
        'LR6': Line(
            color="olive",
            station_list=[
                "Malabe",
                "SLIIT",
                "Kaduwela",
            ],
            path="2NE",
        ),
        'LR5': Line(
            color="darkblue",
            station_list=["Malabe", "Hokandara", "Kottawa"],
            path="2SE",
        ),
        'LR2a': Line(
            color="gold",
            station_list=[
                "Maradana",
                "Hulftsdorp",
                "Kotahena",
                "Grandpass",
                "Madampitiya",
                "Peliyagoda",
                "Kelaniya",
            ],
            path="2N 3NE 1E",
        ),
        'LR2b': Line(
            color="yellow",
            station_list=[
                "Kotahena",
                "Hettiyawatta",
                "Modara",
                "Mattakkuliya",
            ],
            path="1NW 1NE 1N",
        ),
        'LR7': Line(
            color="silver",
            station_list=[
                "Peliyagoda",
                "Kiribathgoda",
                "Mahara",
                "Kadawatha",
            ],
            path="3NE",
        ),
        'LR3b': Line(
            color="red",
            station_list=[
                "Borella Junction",
                "Kanatta",
                "Narehenpita",
                "Kirula",
                "Pamankada",
                "Kirulapone",
                "Havelock City",
                "Havelock Town",
                "Visakha",
                "Bambamapitiya",
            ],
            path="4S 4W 1NW",
        ),
        'LR3a': Line(
            color="red",
            station_list=[
                "Borella Junction",
                "Maligawatta",
                "Welikada",
                "Dematagoda",
            ],
            path="3N",
        ),
    },
)

styler = Styler(DIM=2000)

Draw(config, styler).draw('images/lk_colombo_lrt_proposed.png')
