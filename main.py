import sys
import time
import random
from os import path

import pygame

__path__ = path.dirname(path.abspath(__file__))
sys.path.append(__path__)
from players import Player1, Player2, Player3, get_midpoint
from utils import get_pure_path

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ДИАЛОГ КОМБАТ")
clock = pygame.time.Clock()

# Рандомный выбор фона (1 или 2)
backgr = random.randint(1, 2)

# Загрузка текстур фона
try:
    bg_back = pygame.image.load(get_pure_path("textures/background_back.png")).convert_alpha()
    bg_mid = pygame.image.load(get_pure_path("textures/background_mid.png")).convert_alpha()
    bg_front = pygame.image.load(get_pure_path("textures/background_front.png")).convert_alpha()
    bg_back_2 = pygame.image.load(get_pure_path("textures/background_back_2.png")).convert_alpha()
except Exception as e:
    # Создаем заглушки для фона
    bg_back = pygame.Surface((SCREEN_WIDTH, 720))
    bg_back.fill((0, 0, 100))
    bg_mid = pygame.Surface((SCREEN_WIDTH, 357))
    bg_mid.fill((0, 100, 0))
    bg_front = pygame.Surface((960, 329))
    bg_front.fill((100, 0, 0))
    bg_back_2 = pygame.Surface((SCREEN_WIDTH, 720))
    bg_back_2.fill((50, 50, 150))

# Масштабирование текстур фона
bg_front = pygame.transform.scale(bg_front, (960, SCREEN_HEIGHT // 2))
bg_mid = pygame.transform.scale(bg_mid, (SCREEN_WIDTH * 2, SCREEN_HEIGHT // 2))
bg_back = pygame.transform.scale(bg_back, (int(SCREEN_WIDTH * 1.5), int(SCREEN_HEIGHT * 1.5)))
bg_back_2 = pygame.transform.scale(bg_back_2, (int(SCREEN_WIDTH * 1.5), int(SCREEN_HEIGHT * 1.5)))


def menushka(screen):
    player1_instance = player2_instance = None  # игроки изначально не выбраны
    curr_p1_idx = curr_p2_idx = 0
    curr_section = 1  # 1 -> player1; -1 -> player2

    players = [Player1, Player2, Player3]  # Список классов игроков

    player1_rect = pygame.Rect(100, 100, 300, 500)
    player2_rect = pygame.Rect(800, 100, 300, 500)

    font = pygame.font.SysFont('SysFont', 52)
    text1 = font.render('Выберите бойца', False, (255, 255, 255))
    font_small = pygame.font.SysFont('SysFont', 32)

    while (player1_instance is None) or (player2_instance is None):
        screen.fill((0, 0, 0))
        screen.blit(text1, (460, 100))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return (player1_instance, player2_instance)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # переключение панелей
                    curr_section *= -1

                elif event.key == pygame.K_RETURN:  # выбор игрока
                    if curr_section == 1 and player1_instance is None:  # если не выбран первый игрок
                        player1_instance = players[curr_p1_idx](
                            x=200,
                            y=690,
                            screen=screen,
                            controls={
                                "left": pygame.K_d,
                                "right": pygame.K_a,
                                "attack": pygame.K_RCTRL
                            },
                            flip=True,
                            is_player1=True
                        )
                    elif curr_section == -1 and player2_instance is None:
                        player2_instance = players[curr_p2_idx](
                            x=700,
                            y=690,
                            screen=screen,
                            controls={
                                "left": pygame.K_RIGHT,
                                "right": pygame.K_LEFT,
                                "attack": pygame.K_f
                            },
                            flip=False,
                            is_player1=False
                        )

                elif event.key == pygame.K_DOWN:  # переключение игроков
                    if player1_instance is None:
                        curr_p1_idx = (curr_p1_idx + 1) % len(players)

                    if player2_instance is None:
                        curr_p2_idx = (curr_p2_idx + 1) % len(players)

                elif event.key == pygame.K_UP:
                    if player1_instance is None:
                        curr_p1_idx = (curr_p1_idx - 1) % len(players)

                    if player2_instance is None:
                        curr_p2_idx = (curr_p2_idx - 1) % len(players)

        # переключение квадратов
        if curr_section == 1:
            pygame.draw.rect(screen, (0, 255, 0), player1_rect, 8)
            pygame.draw.rect(screen, (50, 50, 50), player2_rect, 8)
        else:
            pygame.draw.rect(screen, (50, 50, 50), player1_rect, 8)
            pygame.draw.rect(screen, (0, 255, 0), player2_rect, 8)

        # рисование бойцов
        player_img1 = pygame.image.load(players[curr_p1_idx].TEXTURES[0])
        player_img1_rect = player_img1.get_rect(center=(250, 350))

        player_img2 = pygame.image.load(players[curr_p2_idx].TEXTURES[0])
        player_img2_rect = player_img2.get_rect(center=(950, 350))

        screen.blit(player_img1, player_img1_rect)
        screen.blit(player_img2, player_img2_rect)

        if player1_instance is not None:
            text_selected1 = font_small.render("Боец 1 выбран", True, (255, 0, 0))
            screen.blit(text_selected1, (player1_rect.centerx - text_selected1.get_width() // 2, player1_rect.bottom + 10))
        if player2_instance is not None:
            text_selected2 = font_small.render("Боец 2 выбран", True, (255, 0, 0))
            screen.blit(text_selected2, (player2_rect.centerx - text_selected2.get_width() // 2, player2_rect.bottom + 10))

        pygame.display.flip()

    return (player1_instance, player2_instance)


player1, player2 = menushka(screen)


# Параллакс-эффект
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
        progress = (midpoint_x - SCREEN_WIDTH // 2) / (SCREEN_WIDTH // 2)
        progress = max(-1, min(1, progress))

        self.front_pos = progress * self.max_offset
        self.mid_pos = progress * self.max_mid_offset
        self.back_pos = progress * self.max_back_offset

    def draw(self, surface):
        back_y = (SCREEN_HEIGHT - bg_back.get_height()) // 2
        if backgr == 1:
            surface.blit(bg_back, (self.back_pos - (bg_back.get_width() - SCREEN_WIDTH) // 2, back_y))
        else:
            surface.blit(bg_back_2, (self.back_pos - (bg_back_2.get_width() - SCREEN_WIDTH) // 2, back_y))

        mid_y = 350
        surface.blit(bg_mid, (self.mid_pos - (bg_mid.get_width() - SCREEN_WIDTH) // 2, mid_y))

        front_y = SCREEN_HEIGHT - bg_front.get_height()
        surface.blit(bg_front, (self.front_pos, front_y))
        surface.blit(bg_front, (self.front_pos + bg_front.get_width(), front_y))
        surface.blit(bg_front, (self.front_pos - bg_front.get_width(), front_y))


parallax_bg = ParallaxBackground()

running = True
game_over = False
winner = None
game_over_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        player1.update(keys, player2)
        player2.update(keys, player1)

        midpoint = get_midpoint(player1, player2)
        parallax_bg.update(midpoint[0])

        # Проверка на победу
        if not player1.is_alive or not player2.is_alive:
            game_over = True
            winner = 2 if not player1.is_alive else 1
            game_over_time = pygame.time.get_ticks()
    else:
        # Ждем 3 секунды после победы
        if pygame.time.get_ticks() - game_over_time > 3000:
            running = False

    screen.fill((0, 0, 0))
    parallax_bg.draw(screen)
    player1.draw()
    player2.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
