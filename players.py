import pygame


class Player:
    MOVE_KEYS: list = list()

    def __init__(self, velocity, x, y, screen: pygame.surface.Surface, TEXTURES: list):
        self.base    = pygame.image.load(TEXTURES[0]).convert_alpha()
        self.block   = pygame.image.load(TEXTURES[1]).convert_alpha()
        self.strike1 = pygame.image.load(TEXTURES[2]).convert_alpha()
        self.strike2 = pygame.image.load(TEXTURES[3]).convert_alpha()
        self.strike3 = pygame.image.load(TEXTURES[4]).convert_alpha()

        self.texture = self.base

        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y - self.texture_rect.height // 2)
        self.screen = screen
        self.velocity = velocity

    def move(self, keys: pygame.key.ScancodeWrapper):
        if keys[self.MOVE_KEYS[0]]:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)

        if keys[self.MOVE_KEYS[1]]:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def change_texture(self, index: int):  # index - number of image in TEXTURES
        self.texture = pygame.image.load(self.TEXTURES[index]).convert_alpha()


class Player1(Player):
    MOVE_KEYS = [pygame.K_LEFT, pygame.K_RIGHT]


class Player2(Player):
    MOVE_KEYS = [pygame.K_a, pygame.K_d]
