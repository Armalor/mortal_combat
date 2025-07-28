from utils import get_pure_path
from players import Player


class Player2(Player):
    NAME = 'Человек-Борян'

    TEXTURES = [
        get_pure_path('textures/2_boris_chai/base_resized.png'),
        get_pure_path('textures/2_boris_chai/block_resized.png'),
        get_pure_path('textures/2_boris_chai/strike1_resized.png'),
        get_pure_path('textures/2_boris_chai/strike2_resized.png'),
        get_pure_path('textures/2_boris_chai/strike3_resized.png'),
        get_pure_path('textures/2_boris_chai/win_resized.png'),
        get_pure_path('textures/2_boris_chai/defeat_resized.png'),
        get_pure_path('textures/2_boris_chai/aperkot1_resized.png'),
        get_pure_path('textures/2_boris_chai/aperkot2_resized.png'),
        get_pure_path('textures/2_boris_chai/aperkot3_resized.png'),
        get_pure_path('textures/2_boris_chai/block.png'),
    ]