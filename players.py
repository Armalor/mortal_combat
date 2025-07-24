import pygame


class Player:
    TEXTURES: list = list()

    def __init__(self, velocity, x, y, screen: pygame.surface.Surface):
        self.base    = pygame.image.load(self.TEXTURES[0]).convert_alpha()
        self.block   = pygame.image.load(self.TEXTURES[1]).convert_alpha()
        self.strike1 = pygame.image.load(self.TEXTURES[2]).convert_alpha()
        self.strike2 = pygame.image.load(self.TEXTURES[3]).convert_alpha()
        self.strike3 = pygame.image.load(self.TEXTURES[4]).convert_alpha()

        self.texture = self.base

        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y - self.texture_rect.height // 2)
        self.screen = screen
        self.velocity = velocity

    def move(self, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)

        if keys[pygame.K_RIGHT]:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)

    def draw(self):
        # Отображение текстуры
        self.screen.blit(self.texture, self.texture_rect)

    def change_texture(self, index: int):  # index - number of image in TEXTURES
        self.texture = pygame.image.load(self.TEXTURES[index]).convert_alpha()


class Player1(Player):
    TEXTURES = [
        'images/base.png',
        'images/block.png',
        'images/strike1.png',
        'images/strike2.png',
        'images/strike3.png'
    ]


class Player2(Player):
    pass
