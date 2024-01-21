from hbd import Draw, Line, Network, Styler

config = Network(
    title='Rivers of Sri Lanka',
    subtitle="Cities and Towns",
    footer_text='Not to scale.',
    line_idx={
        'Mahaweli Ganga': Line(
            color="darkblue",
            station_list=[
                "Trincomalee",
                "Somaswathiya",
                "Mahiyanganaya",
                "Randenigala Res.",
                "Victoria Res.",
                "Katugastota",
                "Peradeniya",
                "Gampola",
                "Nawalapitiya",
                "Kothmale Res.",
            ],
            path="2S 2W 2S 2S 1SE",
        ),
        'Mahaweli Ganga2': Line(
            color="darkblue",
            station_list=[
                "Nawalapitiya",
                "Ginigathena",
                "Watawala",
                "Hatton",
                "Sri Paada Range",
            ],
            path="3SW 1S",
        ),
        'Ramboda Oya': Line(
            color="blue",
            station_list=[
                "Kothmale Res.",
                "Ramboda",
                "Labukelle",
                "Pidurutalagala Range",
            ],
            path="2E 1SE",
        ),
        'Pundalu Oya': Line(
            color="blue",
            station_list=[
                "Kothmale Res.",
                "Pundalu Oya",
                "Dunsinane Falls",
            ],
            path="2SE",
        ),
        'Kothmale Oya': Line(
            color="blue",
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
                "Pidurutalagala Range",
            ],
            path="4E",
        ),
        'Agra Oya': Line(
            color="lightblue",
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
    },
)

styler = Styler(DIM=2000)

Draw(config, styler).draw('images/lk_rivers.png')
