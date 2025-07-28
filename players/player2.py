from utils import get_pure_path
from players import Player


class Player2(Player):
    NAME = 'Человек-Борян'

    TEXTURES = [
        get_pure_path('textures/2_boris_chai/base.png'),
        get_pure_path('textures/2_boris_chai/block.png'),
        get_pure_path('textures/2_boris_chai/strike1.png'),
        get_pure_path('textures/2_boris_chai/strike2.png'),
        get_pure_path('textures/2_boris_chai/strike3.png'),
    ]
