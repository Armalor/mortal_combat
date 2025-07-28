from utils import get_pure_path
from players import Player


class Player1(Player):
    NAME = 'Мега-СВШ'

    TEXTURES = [
        get_pure_path('textures/1_svsh/base_resized.png'),
        get_pure_path('textures/1_svsh/block_resized.png'),
        get_pure_path('textures/1_svsh/strike1_resized.png'),
        get_pure_path('textures/1_svsh/strike2_resized.png'),
        get_pure_path('textures/1_svsh/strike3_resized.png'),

        get_pure_path('textures/1_svsh/win_resized.png'),
        get_pure_path('textures/1_svsh/defeat_resized.png'),

        get_pure_path('textures/1_svsh/aperkot1_resized.png'),
        get_pure_path('textures/1_svsh/aperkot2_resized.png'),
        get_pure_path('textures/1_svsh/aperkot3_resized.png'),
    ]

