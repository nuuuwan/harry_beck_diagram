from examples.lk_rail_history import build_config_idx
from hbd import Draw, Styler

config = list(build_config_idx().values())[-1]

config.title = 'Hypothetical New Lines'
config.subtitle = 'Sri Lanka Railways'
config.footer_text = 'Based off suggestions from #ChatGPT4'


config.extend_line('Coastal', ['Hambantota', 'Kataragama'], '2NE')
config.extend_line(
    'Kelani Valley',
    ['Ratnapura', 'Rakwana', 'Embilipitiya', 'Hambantota'],
    '4SE',
)
config.add_line(
    'Wilpattu', 'gold', ['Mannar', 'Vellankulam', 'Pooneryn', 'Jaffna'], '3N'
)
config.add_line(
    'East Coast',
    'olive',
    [
        'Trincomalee',
        'Vakarai',
        'Batticaloa',
        'Sammanthurai',
        'Akkaraipattu',
        'Pottuvil',
    ],
    '2SE 3S',
)
styler = Styler(DIM=2880)

Draw(config, styler).draw('images/lk_rail_hyp.png')
