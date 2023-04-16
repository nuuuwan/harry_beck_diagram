from hbd import Draw, Line, Network, Styler

config = Network(
    title='Proposed Railway Interventions',
    subtitle='Western Province, Sri Lanka',
    footer_text='Not to scale. Not all stations are displayed.',
    line_idx={
        'Main': Line(
            color="red",
            station_list=[
                "Colombo Fort",
                "Maradana",
                "Kelaniya",
                "Ragama Junction",
                "Gampaha",
                "Daraluwa",
                "Veyangoda",
                "Meerigama",
            ],
            path="4NE 3E",
        ),
        'Coastal': Line(
            color="cyan",
            station_list=[
                "Colombo Fort",
                "Kollupitiya",
                "Bambalapitiya",
                "Wellawatte",
                "Dehiwela",
                "Ratmalana",
                "Moratuwa",
                "Panadura",
            ],
            path="7S",
        ),
        'Puttalam': Line(
            color="green",
            station_list=[
                "Ragama Junction",
                "Kandana",
                "Ja-Ela",
                "Seeduwa",
                "Colombo Airport Katunayake",
                "Negombo",
            ],
            path="2NW 3N",
        ),
        'Kelani Valley': Line(
            color="darkblue",
            station_list=[
                "Maradana",
                "Narahenpita",
                "Nugegoda",
                "Maharagama",
                "Kottawa",
                "Homagama",
                "Padukka",
                "Waga",
                "Kosgama",
                "Puwakpitiya",
                "Avissawella",
            ],
            path="3SE 2E 2NE 3N",
        ),
        'Kelani Valley-2': Line(
            color="orange",
            station_list=[
                "Kelaniya",
                "Weliwita",
                "Biyagama",
                "Kaduwela",
                "Kandewatta",
                "Dompe",
                "Kosgama",
            ],
            path="5E",
        ),
        'Horana': Line(
            color="purple",
            station_list=[
                "Kottawa",
                "Polgasowita",
                "Gonapola",
                "Pokunuwita",
                "Horana",
            ],
            path="4S",
        ),
    },
)

styler = Styler(DIM=2000)

Draw(config, styler).draw('images/lk_wp_proposed.png')
