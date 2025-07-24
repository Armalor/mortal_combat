import pygame
from players import Player1
from time import sleep
from threading import Thread
import sys
WIDTH, HEIGHT = 1200, 700
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ДИАЛОГ КОМБАТ")
clock = pygame.time.Clock()

# Загрузка текстур
try:
    bg_back = pygame.image.load("textures/background_back.png").convert_alpha()
    bg_mid = pygame.image.load("textures/background_mid.png").convert_alpha()
    bg_front = pygame.image.load("textures/background_front.png").convert_alpha()
    bg_back_2 = pygame.image.load("textures/background_back_2.png").convert_alpha()

except Exception as e:
    print( {e})
    # Создаем заглушки для текстур
    bg_back = pygame.Surface((WIDTH, 720))
    bg_back.fill(BLUE)
    bg_mid = pygame.Surface((WIDTH, 357))
    bg_mid.fill(GREEN)
    bg_front = pygame.Surface((960, 329))
    bg_front.fill(RED)
    bg_back_2 = pygame.Surface((WIDTH, 720))
    bg_back_2.fill((100, 100, 255))

# Масштабирование текстур
bg_front = pygame.transform.scale(bg_front, (960, HEIGHT // 2))
bg_mid = pygame.transform.scale(bg_mid, (WIDTH * 2, HEIGHT // 2))
bg_back = pygame.transform.scale(bg_back, (WIDTH * 1.5, HEIGHT * 1.5))
bg_back_2 = pygame.transform.scale(bg_back_2, (WIDTH * 1.5, HEIGHT * 1.5))


class ParallaxBackground:
    def __init__(self):
        self.back_pos = 0
        self.mid_pos = 0
        self.front_pos = 0
        self.max_offset = 960

        self.back_speed = 0.3
        self.mid_speed = 0.5
        self.front_speed = 2.0

        self.max_mid_offset = (bg_mid.get_width() - WIDTH) / 2
        self.max_back_offset = (bg_back.get_width() - WIDTH) / 2

    def update(self, midpoint_x):
        # Рассчитываем прогресс (0 - левая граница, 1 - правая)
        progress = (midpoint_x - WIDTH // 2) / (WIDTH // 2)
        progress = max(-1, min(1, progress))  # Ограничиваем от -1 до 1

        # Обновляем позиции фона
        self.front_pos = progress * self.max_offset
        self.mid_pos = progress * self.max_mid_offset
        self.back_pos = progress * self.max_back_offset

    def draw(self, surface):
        # Задний фон
        back_y = (HEIGHT - bg_back.get_height()) // 2
        surface.blit(bg_back, (self.back_pos - (bg_back.get_width() - WIDTH) // 2, back_y))


        # Средний слой
        mid_y = 350
        surface.blit(bg_mid, (self.mid_pos - (bg_mid.get_width() - WIDTH) // 2, mid_y))

        # Передний слой
        front_y = HEIGHT - bg_front.get_height()
        surface.blit(bg_front, (self.front_pos, front_y))
        surface.blit(bg_front, (self.front_pos + bg_front.get_width(), front_y))
        surface.blit(bg_front, (self.front_pos - bg_front.get_width(), front_y))

parallax_bg = ParallaxBackground()
def main():
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DIALOG-KOMBAT")
    running = True

    player1 = Player1(10, 300, 600, screen)
    st = Thread(target=strike_th, args=(player1,), daemon=True)

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        strike = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    strike = True

        keys = pygame.key.get_pressed()

        if strike and not st.is_alive():
            st = Thread(target=strike_th, args=(player1,), daemon=True)
            st.start()



        player1.move(keys)
        player1.draw()
        screen.fill(BLACK)
        parallax_bg.draw(screen)
        pygame.display.flip()

def strike_th (player1):
    print('STRIKE!')

    pause = 0.35 / 3
    player1.change_texture(2)
    sleep(pause)
    player1.change_texture(3)
    sleep(pause)
    player1.change_texture(4)
    sleep(pause)
    player1.change_texture(0)


if __name__ == '__main__':
    main()
