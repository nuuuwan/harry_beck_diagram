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
config_idx['1867'].line_idx['Main'].station_list += [
    "Polgahawela",
    "Peradeniya",
]
config_idx['1867'].line_idx['Main'].path += " 2E"

config_idx['1867'].line_idx['Matale'] = Line(
    color="purple",
    station_list=["Peradeniya", "Kandy"],
    path="1NE",
)

config_idx['1874'] = config_idx['1867'].copy(title="1874")
config_idx['1874'].line_idx['Main'].station_list += ["Nawalapitiya"]
config_idx['1874'].line_idx['Main'].path += " 1SE"

config_idx['1880'] = config_idx['1874'].copy(title="1880")
config_idx['1880'].line_idx['Matale'].station_list += ["Matale"]
config_idx['1880'].line_idx['Matale'].path += " 1E"

config_idx['1885'] = config_idx['1880'].copy(title="1885")
config_idx['1885'].line_idx['Main'].station_list += ["Nanu Oya"]
config_idx['1885'].line_idx['Main'].path += " 1SE"

config_idx['1894'] = config_idx['1885'].copy(title="1894")
config_idx['1894'].line_idx['Main'].station_list += ["Bandarawela"]
config_idx['1894'].line_idx['Main'].path += " 1E"

config_idx['1895'] = config_idx['1894'].copy(title="1895")
config_idx['1895'].line_idx['Coastal'] = Line(
    color="cyan",
    station_list=["Colombo Fort", "Kalutara North", "Galle", "Matara"],
    path="1S 1SE 1E",
)

config_idx['1902'] = config_idx['1895'].copy(title="1902")
config_idx['1902'].line_idx['Kelani Valley'] = Line(
    color="darkblue",
    station_list=["Maradana", "Homagama", "Avissawella", "Yatiyantota"],
    path="1SE 1E 1NE",
)

config_idx['1903'] = config_idx['1902'].copy(title="1903")
config_idx['1903'].line_idx['Udu Pussellawa'] = Line(
    color="gray",
    station_list=["Nanu Oya", "Nuwara Eliya", "Kandapola"],
    path="1N 1NE",
)

config_idx['1904'] = config_idx['1903'].copy(title="1904")
config_idx['1904'].line_idx['Udu Pussellawa'].station_list += ["Ragala"]
config_idx['1904'].line_idx['Udu Pussellawa'].path += " 1E"


config_idx['1905'] = config_idx['1904'].copy(title="1905")
config_idx['1905'].line_idx['Northern'] = Line(
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
    path="7N 1NW 1N",
)

config_idx['1912'] = config_idx['1905'].copy(title="1912")
config_idx['1912'].line_idx['Opanayaka'] = Line(
    color="lightblue",
    station_list=["Avissawella", "Ratnapura", "Opanayaka"],
    path="1SE 1E",
)

config_idx['1914'] = config_idx['1912'].copy(title="1914")
config_idx['1914'].line_idx['Mannar'] = Line(
    color="blue",
    station_list=["Medavachchiya", "Mannar", "Talaimannar Pier"],
    path="1NW 1W",
)

config_idx['1924'] = config_idx['1914'].copy(title="1924")
config_idx['1924'].line_idx['Main'].station_list += ["Badulla"]
config_idx['1924'].line_idx['Main'].path += " 1NE"


config_idx['1926'] = config_idx['1924'].copy(title="1926")
config_idx['1926'].line_idx['Puttalam'] = Line(
    color="green",
    station_list=["Ragama", "Puttalam", "Periyanurvillu"],
    path="1NW 1N",
)

config_idx['1928'] = config_idx['1926'].copy(title="1928")
config_idx['1928'].line_idx['Batticaloa'] = Line(
    color="darkgreen",
    station_list=["Maho", "Gal Oya", "Polonnaruwa", "Batticaloa"],
    path="1NE 1SE 1E",
)
config_idx['1928'].line_idx['Trincomalee'] = Line(
    color="silver",
    station_list=["Gal Oya", "Trincomalee"],
    path="1NE",
)

config_idx['1942'] = config_idx['1928'].copy(title="1942")
config_idx['1942'].line_idx['Kelani Valley'].station_list = [
    "Maradana",
    "Homagama",
    "Avissawella",
]
config_idx['1942'].line_idx['Kelani Valley'].path = "1SE 1E"

config_idx['1948'] = config_idx['1942'].copy(title="1948")
del config_idx['1948'].line_idx["Udu Pussellawa"]

config_idx['1973'] = config_idx['1948'].copy(title="1973")
del config_idx['1973'].line_idx["Opanayaka"]
config_idx['1973'].line_idx['Kelani Valley'].station_list = [
    "Maradana",
    "Homagama",
]
config_idx['1973'].line_idx['Kelani Valley'].path = "1SE"

config_idx['1978'] = config_idx['1973'].copy(title="1978")
config_idx['1978'].line_idx['Kelani Valley'].station_list = [
    "Maradana",
    "Homagama",
    "Avissawella",
]
config_idx['1978'].line_idx['Kelani Valley'].path = "1SE 1E"

config_idx['1993'] = config_idx['1978'].copy(title="1993")
config_idx['1993'].line_idx['Mihintale'] = Line(
    color="maroon",
    station_list=["Mihintale Junction", "Mihintale"],
    path="1E",
)

config_idx['2019'] = config_idx['1993'].copy(title="2019")
config_idx['2019'].line_idx['Coastal'].station_list += ["Beliatta"]
config_idx['2019'].line_idx['Coastal'].path += " 1E"


styler = Styler(DIM=1300)


png_path_list = []
for year, config in config_idx.items():
    draw = Draw(config, styler)
    png_path = f'images/lk_rail_history/{year}.png'
    png_path = draw.draw(png_path, False)
    png_path_list.append(png_path)

gif_path = 'images/lk_rail_history/timeline.gif'
Draw.build_animated_gif(png_path_list, gif_path)
