from hbd import Draw, Line, Network, Styler

config_idx = {}


def get_latest_config():
    return list(config_idx.values())[-1]


def init_year(year):
    if config_idx:
        latest_config = get_latest_config()
        config = latest_config.copy(title=str(year))
    else:
        config = Network(
            title=str(year),
            footer_text='History of the Railways in Sri Lanka',
            line_idx={},
        )
    config_idx[year] = config
    return config


def add_line(line_name, color, station_list, path):
    config = get_latest_config()
    config.line_idx[line_name] = Line(
        color=color,
        station_list=station_list,
        path=path,
    )


def extend_line(line_name, station_list, path):
    config = get_latest_config()
    line = config.line_idx[line_name]
    line.station_list += station_list
    line.path += ' ' + path


def update_line(line_name, station_list, path):
    config = get_latest_config()
    config.line_idx[line_name] = Line(
        color=config.line_idx[line_name].color,
        station_list=station_list,
        path=path,
    )


def remove_line(line_name):
    config = get_latest_config()
    del config.line_idx[line_name]


init_year(1864)
add_line(
    'Main',
    'red',
    ['Colombo Fort', 'Maradana', 'Ragama', 'Gampaha', 'Ambepussa'],
    '4NE',
)

init_year(1867)
extend_line('Main', ['Polgahawela', 'Peradeniya'], '2E')
add_line('Matale', 'purple', ['Peradeniya', 'Kandy'], '1NE')

init_year(1874)
extend_line('Main', ['Nawalapitiya'], '1SE')

init_year(1877)
add_line('Coastal', 'cyan', ['Colombo Fort', 'Panadura'], '1S')

init_year(1878)
extend_line('Coastal', ['Kalutara North'], '1S')

init_year(1880)
extend_line('Matale', ['Matale'], '1E')

init_year(1885)
extend_line('Main', ['Nanu Oya'], '1SE')

init_year(1890)
extend_line('Coastal', ['Aluthgama'], '1SE')

init_year(1892)
extend_line('Coastal', ['Kosgoda'], '1SE')

init_year(1893)
extend_line('Coastal', ['Ambalangoda'], '1SE')

init_year(1894)
extend_line('Main', ['Bandarawela'], '1E')
extend_line('Coastal', ['Galle'], '1SE')
add_line('Northern', 'orange', ['Polgahawela', 'Kurunegala'], '1N')

init_year(1895)
extend_line('Coastal', ['Matara'], '1E')

init_year(1902)
add_line(
    'Kelani Valley',
    'darkblue',
    ['Maradana', 'Homagama', 'Avissawella', 'Yatiyantota'],
    '1SE 1E 1NE',
)

init_year(1903)
add_line(
    'Udu Pussellawa',
    'gray',
    ['Nanu Oya', 'Nuwara Eliya', 'Kandapola'],
    '1N 1NE',
)

init_year(1904)
extend_line('Udu Pussellawa', ['Ragala'], '1E')
extend_line('Northern', ['Maho', 'Anuradhapura'], '2N')

init_year(1905)
extend_line(
    'Northern',
    [
        'Mihintale Junction',
        'Medavachchiya',
        'Vavuniya',
        'Omanthai',
        'Kilinochchi',
        'Jaffna',
        'Kankesanthurai',
    ],
    '5N 1NW 1N',
)

init_year(1909)
add_line('Puttalam', 'green', ['Ragama', 'Negombo'], '1NW')

init_year(1912)
add_line(
    'Opanayaka', 'lightblue', ['Avissawella', 'Ratnapura', 'Opanayaka'], '1SE 1E'
)

init_year(1914)
add_line(
    'Mannar', 'blue', ['Medavachchiya', 'Mannar', 'Talaimanar Pier'], '1NW 1W'
)

init_year(1916)
extend_line('Puttalam', ['Chilaw'], '1NW')

init_year(1924)
extend_line('Main', ['Badulla'], '1NE')

init_year(1926)
extend_line('Puttalam', ['Bangadeniya', 'Puttalam'], '2N')

init_year(1928)
add_line(
    'Batticaloa',
    'darkgreen',
    ['Maho', 'Gal Oya', 'Polonnaruwa', 'Batticaloa'],
    '1NE 1SE 1E',
)
add_line('Trincomalee', 'silver', ['Gal Oya', 'Trincomalee'], '1NE')

init_year(1942)
update_line(
    'Kelani Valley', ['Maradana', 'Homagama', 'Avissawella'], '1SE 1E'
)

init_year(1943)
update_line(
    'Puttalam', ['Ragama', 'Negombo', 'Chilaw', "Bangadeniya"], '1NW 2N'
)

init_year(1946)
extend_line('Puttalam', ['Puttalam', 'Periyanagavillu'], '2N')

init_year(1948)
remove_line('Udu Pussellawa')

init_year(1973)
remove_line('Opanayaka')
update_line('Kelani Valley', ['Maradana', 'Homagama'], '1SE')

init_year(1978)
extend_line('Kelani Valley', ['Avissawella'], '1E')

init_year(1990)
update_line(
    'Northern',
    [
        'Polgahawela',
        'Kurunegala',
        'Maho',
        'Anuradhapura',
        'Mihintale Junction',
        'Medavachchiya',
        'Vavuniya'
    ],
    '6N',
)
remove_line('Mannar')

init_year(1993)
add_line('Mihintale', 'maroon', ['Mihintale Junction', 'Mihintale'], '1E')

init_year(1996)
update_line('Batticaloa', ['Maho', 'Gal Oya', 'Polonnaruwa'], '1NE 1SE')

init_year(2003)
extend_line('Batticaloa', ['Batticaloa'], '1E')

init_year(2011)
extend_line('Northern', ['Omanthai'], '1N')

init_year(2013)
extend_line('Northern', ['Kilinochchi'], '1N')
add_line('Mannar', 'blue', ['Medavachchiya', 'Madhu Road'], '1NW')

init_year(2014)
extend_line('Northern', ['Jaffna'], '1NW')

init_year(2015)
extend_line('Northern', ['Kankesanthurai'], '1N')
extend_line('Mannar', ['Mannar', 'Talaimanar Pier'], '1NW 1W')

init_year(2019)
extend_line('Coastal', ['Beliatta'], '1E')

styler = Styler(DIM=1300)


png_path_list = []
for year, config in config_idx.items():
    draw = Draw(config, styler)
    png_path = f'images/lk_rail_history/{year}.png'
    png_path = draw.draw(png_path, False)
    png_path_list.append(png_path)

gif_path = 'images/lk_rail_history/timeline.gif'
Draw.build_animated_gif(png_path_list, gif_path)
