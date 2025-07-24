import pygame

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
FPS = 60

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Загрузка текстур
bg_back = pygame.image.load("textures/background_back.png").convert_alpha()
bg_mid = pygame.image.load("textures/background_mid.png").convert_alpha()
bg_front = pygame.image.load("textures/background_front.png").convert_alpha()

# Масштабирование текстур
bg_front = pygame.transform.scale(bg_front, (960, SCREEN_HEIGHT // 2))
bg_mid = pygame.transform.scale(bg_mid, (SCREEN_WIDTH * 2, SCREEN_HEIGHT // 2))


class ParallaxBackground:
    def __init__(self):
        self.back_pos = 0
        self.mid_pos = 0
        self.front_pos = 0
        self.max_offset = 960

        self.back_speed = 0.3
        self.mid_speed = 0.5
        self.front_speed = 2.0

        self.max_mid_offset = (bg_mid.get_width() - SCREEN_WIDTH) / 2
        self.max_back_offset = (bg_back.get_width() - SCREEN_WIDTH) / 2

    def update(self, midpoint_x):
        # Рассчитываем прогресс (0 - левая граница, 1 - правая)
        progress = (midpoint_x - SCREEN_WIDTH // 2) / (SCREEN_WIDTH // 2)
        progress = max(-1, min(1, progress))  # Ограничиваем от -1 до 1

        # Обновляем позиции фона
        self.front_pos = progress * self.max_offset
        self.mid_pos = progress * self.max_mid_offset
        self.back_pos = progress * self.max_back_offset

    def draw(self, surface):
        # Задний фон
        back_y = (SCREEN_HEIGHT - bg_back.get_height()) // 2
        surface.blit(bg_back, (self.back_pos - (bg_back.get_width() - SCREEN_WIDTH) // 2, back_y))

        # Средний слой
        mid_y = 350
        surface.blit(bg_mid, (self.mid_pos - (bg_mid.get_width() - SCREEN_WIDTH) // 2, mid_y))

        # Передний слой
        front_y = SCREEN_HEIGHT - bg_front.get_height()
        surface.blit(bg_front, (self.front_pos, front_y))
        surface.blit(bg_front, (self.front_pos + bg_front.get_width(), front_y))
        surface.blit(bg_front, (self.front_pos - bg_front.get_width(), front_y))
