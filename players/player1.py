from utils import get_pure_path
from players import Player


class Player1(Player):
    NAME = 'Мега-СВШ'

    TEXTURES = [
        get_pure_path('textures/1_svsh/base.png'),
        get_pure_path('textures/1_svsh/block.png'),
        get_pure_path('textures/1_svsh/strike1.png'),
        get_pure_path('textures/1_svsh/strike2.png'),
        get_pure_path('textures/1_svsh/strike3.png'),
    ]

