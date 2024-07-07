from hbd import Draw, Line, Network, Styler

config = Network(
    title='Mahaweli Ganga (335 km)',
    subtitle="River and Tributaries",
    footer_text='Not to scale.',
    line_idx={
        'Mahaweli Ganga': Line(
            color="darkblue",
            station_list=[
                "Bay of Bengal",
                "Trincomalee",
                "Somawathiya",
                "Manampitiya",
                "Kalinga Nuwara",
                "Dehiattakandiya",
                "Habarawa",
                "Ginnoruwa",
                "Mahiyanganaya",
                "Minipe",
                "Uma Oya",
                "Randenigala Res.",
                "Victoria Res.",
                "Gurudeniya",
                "Katugastota",
                "Peradeniya",
                "Ganegoda",
                "Gampola",
                "Moragolla",
                "Nawalapitiya",
                "Kothmale Res.",
            ],
            path="3SW 5S 1SW 5W 1S 3S 2SE",
        ),
        'Mahaweli Ganga2': Line(
            color="lightblue",
            station_list=[
                "Nawalapitiya",
                "Ginigathena",
                "Watawala",
                "Hatton",
                "Sri Paada Range",
            ],
            path="3SW 1S",
        ),
        'Ramboda Oya/Puna Oya': Line(
            color="lightblue",
            station_list=[
                "Kothmale Res.",
                "Ramboda",
                "Labukelle",
                "Pidurutalagala Range",
            ],
            path="2E 1SE",
        ),
        'Pundalu Oya': Line(
            color="lightblue",
            station_list=[
                "Kothmale Res.",
                "Pundalu Oya",
                "Dunsinane Falls",
            ],
            path="2SE",
        ),
        'Kothmale Oya': Line(
            color="darkblue",
            station_list=[
                "Kothmale Res.",
                "Kothmale Oya2",
                "St. Clair Falls",
                "Thalawakele",
            ],
            path="3S",
        ),
        'Kothmale Oya2': Line(
            color="lightblue",
            station_list=[
                "Kothmale Oya2",
                "Devon Falls",
                "Dimbula",
                "Kotagala",
            ],
            path="3SW",
        ),
        'Nanu Oya': Line(
            color="lightblue",
            station_list=[
                "Thalawakele",
                "Upper Kothmale Res.",
                "Nanu Oya",
                "Nuwara Eliya",
                "Lake Gregory",
                "Pidurutalagala Range",
            ],
            path="3E 2N",
        ),
        'Agra Oya': Line(
            color="darkblue",
            station_list=[
                "Thalawakele",
                "Lindula",
                "Elgin Falls",
                "Ambewela",
                "Black Pool",
                "Horton Plains",
            ],
            path="3SE 2S",
        ),
        'Atabage Oya': Line(
            color="lightblue",
            station_list=["Moragolla", "Atabage", "Stellenberg"],
            path="2E",
        ),
        'Nillambe Oya': Line(
            color="lightblue",
            station_list=["Ganegoda", "Nillambe", "Morahena"],
            path="1E 1SE",
        ),
        'Thalathu Oya': Line(
            color="lightblue",
            station_list=["Gurudeniya", "Thalathuoya"],
            path="1SE",
        ),
        'Heen Ganga': Line(
            color="lightblue",
            station_list=[
                "Ginnoruwa",
                "Uduwelwala",
                "Meemure",
                "Knuckles Range",
            ],
            path="1W 1SW 1NW",
        ),
        'Hulu Ganga': Line(
            color="lightblue",
            station_list=[
                "Victoria Res.",
                "Orutota",
                "Hulu Ganga",
                "Knuckles Range",
            ],
            path="2N 1NE",
        ),
        'Uma Oya': Line(
            color="lightblue",
            station_list=[
                "Uma Oya",
                "Puhulpola",
                "Welimada",
                "Hewanakumbubura",
            ],
            path="1S 1SW 1W",
        ),
        'Loggal Oya': Line(
            color="lightblue",
            station_list=[
                "Minipe",
                "Loggal Oya",
                "Gerandi Ella",
                "Passara",
            ],
            path="1E 1SE 1S",
        ),
        'Badulu Oya': Line(
            color="lightblue",
            station_list=[
                "Minipe",
                "Kandaketiya",
                "Thaldena",
                "Dunhinda Falls",
                "Badulla",
                "Muthiyanganaya",
                "Hali Ela",
                "Demodara",
                "Namunukula Range",
            ],
            path="1SE 4S 1SW 1SE 1E",
        ),
        'Amban Ganga': Line(
            color="lightblue",
            station_list=[
                "Manampitiya",
                "Parakrama Samudraya",
                "Angamedilla",
                "Elahera",
                "Moragahakanda Res.",
                "Bowatenna Res.",
            ],
            path="1W 1SW 3W",
        ),
        'Sudu Ganga': Line(
            color="lightblue",
            station_list=[
                "Bowatenna Res.",
                "Rajjammana",
                "Matale",
            ],
            path="2S",
        ),
        'Kalu Ganga': Line(
            color="lightblue",
            station_list=[
                "Elahera",
                "Kalu Ganga Res.",
                "Ilukkumbura",
                "Knuckles Range",
            ],
            path="3S",
        ),
    },
)

styler = Styler(DIM=5000)

Draw(config, styler).draw('images/lk_rivers_mahaweli.png')
