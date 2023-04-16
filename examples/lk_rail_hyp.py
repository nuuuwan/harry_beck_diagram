from examples.lk_rail_history import build_config_idx
from hbd import Draw, Line, Network, Styler

config = list(build_config_idx().values())[-1]
config.title = 'Hypothetical New Lines'

styler = Styler(DIM=2880)

Draw(config, styler).draw('images/lk_rail_hyp.png')
