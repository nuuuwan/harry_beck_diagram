from hbd import Draw, ImageHighlight, Network, Styler


def build_year_to_config():  # noqa
    year_to_config = {}

    def get_latest_config():
        return list(year_to_config.values())[-1]

    def add_year(year):
        if year_to_config:
            latest_config = get_latest_config()
            config = latest_config.copy(title=str(year))
        else:
            config = Network.from_year(year)
        year_to_config[year] = config
        return config

    def add_line(line_name, color, station_list, path):
        get_latest_config().add_line(line_name, color, station_list, path)

    def extend_line(line_name, station_list, path):
        get_latest_config().extend_line(line_name, station_list, path)

    def update_line(line_name, station_list, path):
        get_latest_config().update_line(line_name, station_list, path)

    def remove_line(line_name):
        get_latest_config().remove_line(line_name)

    def rename_station(old_name, new_name):
        get_latest_config().rename_station(old_name, new_name)

    def update_line_at_start(line_name, station_name, path_item):
        get_latest_config().update_line_at_start(
            line_name, station_name, path_item
        )

    add_year(1865)
    add_line(
        "Main",
        "red",
        ["Colombo Terminus", "Ragama", "Gampaha", "Ambepussa"],
        "3NE",
    )

    add_year(1867)
    extend_line("Main", ["Polgahawela", "Peradeniya"], "2E")
    add_line("Matale", "purple", ["Peradeniya", "Kandy"], "1NE")

    add_year(1873)
    extend_line("Main", ["Gampola"], "1SE")

    add_year(1874)
    extend_line("Main", ["Nawalapitiya"], "1SE")

    add_year(1875)
    extend_line("Main", ["Talawakele"], "1SE")

    add_year(1877)
    add_line("Coastal", "cyan", ["Colombo Terminus", "Panadura"], "1S")

    add_year(1878)
    extend_line("Coastal", ["Kalutara North"], "1S")

    add_year(1879)
    extend_line("Coastal", ["Wadduwa"], "1S")

    add_year(1880)
    extend_line("Matale", ["Matale"], "1E")

    add_year(1885)
    extend_line("Main", ["Nanu Oya"], "1SE")

    add_year(1890)
    extend_line("Coastal", ["Aluthgama"], "1SE")

    add_year(1892)
    extend_line("Coastal", ["Kosgoda"], "1SE")

    add_year(1893)
    extend_line("Coastal", ["Ambalangoda"], "1SE")
    extend_line("Main", ["Haputale"], "1E")

    add_year(1894)
    extend_line("Main", ["Bandarawela"], "1E")
    extend_line("Coastal", ["Galle"], "1E")
    add_line("Northern", "orange", ["Polgahawela", "Kurunegala"], "1N")

    add_year(1895)
    extend_line("Coastal", ["Matara"], "1E")

    add_year(1899)
    extend_line("Northern", ["Maho"], "1N")

    add_year(1902)
    add_line(
        "Kelani Valley",
        "darkblue",
        ["Colombo Terminus", "Homagama", "Avissawella"],
        "1SE 1E",
    )

    add_line(
        "Northern-2",
        "orange",
        [
            "Pallai",
            "Jaffna",
            "Kankesanthurai",
        ],
        "1NW 1N",
    )

    add_year(1903)
    add_line(
        "Udu Pussellawa",
        "gray",
        ["Nanu Oya", "Nuwara Eliya", "Kandapola"],
        "1N 1NE",
    )
    extend_line("Kelani Valley", ["Yatiyantota"], "1NE")

    add_year(1904)
    extend_line("Udu Pussellawa", ["Ragala"], "1E")
    extend_line("Northern", ["Anuradhapura"], "1N")

    add_year(1905)
    remove_line("Northern-2")
    extend_line(
        "Northern",
        [
            "Mihintale Junction",
            "Medavachchiya",
            "Vavuniya",
            "Omanthai",
            "Kilinochchi",
            "Pallai",
            "Jaffna",
            "Kankesanthurai",
        ],
        "5N 2NW 1N",
    )

    add_year(1908)
    rename_station("Colombo Terminus", "Maradana")
    add_line("Puttalam", "green", ["Ragama", "Ja-Ela"], "1NW")

    add_year(1909)
    extend_line("Puttalam", ["Katunayake South", "Negombo"], "2NW")

    add_year(1912)
    add_line(
        "Opanayaka",
        "lightblue",
        ["Avissawella", "Ratnapura", "Opanayaka"],
        "1SE 1E",
    )

    add_year(1914)
    add_line(
        "Mannar",
        "blue",
        ["Medavachchiya", "Madhu Road", "Mannar", "Talaimanar Pier"],
        "2NW 1W",
    )
    add_year(1915)
    extend_line("Puttalam", ["Madampe"], "1N")

    add_year(1916)
    extend_line("Puttalam", ["Chilaw"], "1N")

    add_year(1917)
    extend_line("Coastal", ["Kosgoda"], "1SE")
    update_line(
        "Coastal",
        [
            "Maradana",
            "Colombo Fort",
            "Panadura",
            "Kalutara North",
            "Wadduwa",
            "Aluthgama",
            "Kosgoda",
            "Ambalangoda",
            "Galle",
            "Matara",
        ],
        "3S 3SE 3E",
    )
    update_line_at_start("Main", "Colombo Fort", "1N")

    add_year(1924)
    extend_line("Main", ["Badulla"], "1NE")

    add_year(1926)
    extend_line("Puttalam", ["Bangadeniya", "Puttalam"], "2N")
    add_line(
        "Batticaloa",
        "darkgreen",
        ["Maho", "Gal Oya"],
        "1NE",
    )

    add_year(1927)
    add_line("Trincomalee", "silver", ["Gal Oya", "Trincomalee"], "1NE")

    add_year(1928)
    extend_line("Batticaloa", ["Polonnaruwa", "Batticaloa"], "1SE 1E")

    add_year(1942)
    update_line(
        "Kelani Valley",
        ["Maradana", "Homagama", "Avissawella"],
        "1SE 1E",
    )

    add_year(1943)
    update_line(
        "Puttalam",
        [
            "Ragama",
            "Ja-Ela",
            "Katunayake South",
            "Negombo",
            "Madampe",
            "Chilaw",
            "Bangadeniya",
        ],
        "3NW 3N",
    )

    add_year(1946)
    extend_line("Puttalam", ["Puttalam", "Periyanagavillu"], "2N")

    add_year(1948)
    remove_line("Udu Pussellawa")

    add_year(1970)
    add_line(
        "Katunayake",
        "pink",
        ["Katunayake South", "CMB Airport"],
        "1N",
    )

    add_year(1973)
    remove_line("Opanayaka")
    update_line("Kelani Valley", ["Maradana", "Homagama"], "1SE")

    add_year(1978)
    extend_line("Kelani Valley", ["Avissawella"], "1E")

    add_year(1985)
    remove_line("Mannar")

    add_year(1990)
    update_line(
        "Northern",
        [
            "Polgahawela",
            "Kurunegala",
            "Maho",
            "Anuradhapura",
            "Mihintale Junction",
            "Medavachchiya",
            "Vavuniya",
        ],
        "6N",
    )

    add_year(1993)
    add_line("Mihintale", "maroon", ["Mihintale Junction", "Mihintale"], "1E")

    add_year(1996)
    update_line("Batticaloa", ["Maho", "Gal Oya", "Polonnaruwa"], "1NE 1SE")

    add_year(2003)
    extend_line("Batticaloa", ["Batticaloa"], "1E")

    add_year(2011)
    extend_line("Northern", ["Omanthai"], "1N")

    add_year(2013)
    extend_line("Northern", ["Kilinochchi", "Pallai"], "1N 1NW")
    add_line("Mannar", "blue", ["Medavachchiya", "Madhu Road"], "1NW")

    add_year(2014)
    extend_line("Northern", ["Jaffna"], "1NW")

    add_year(2015)
    extend_line("Northern", ["Kankesanthurai"], "1N")
    extend_line("Mannar", ["Mannar", "Talaimanar Pier"], "1NW 1W")

    add_year(2019)
    extend_line("Coastal", ["Beliatta"], "1E")

    return year_to_config


if __name__ == "__main__":
    year_to_config = build_year_to_config()

    png_path_list = []
    prev_png_path = None
    for year, config in year_to_config.items():
        draw = Draw(config, Styler())
        png_path = f"images/lk_rail_history/{year}.png"
        png_path = draw.draw(png_path, False)

        if prev_png_path:
            png_path_highlight = png_path[:-4] + ".highlight.png"
            ImageHighlight(
                png_path,
                prev_png_path,
                400,
            ).write(png_path_highlight)
        else:
            png_path_highlight = png_path
        prev_png_path = png_path
        png_path_list.append(png_path_highlight)

    gif_path = "images/lk_rail_history/timeline.gif"
    Draw.build_animated_gif(png_path_list, gif_path)
