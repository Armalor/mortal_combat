import pygame
import sys
from players import Player, get_midpoint

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Выбор фонов
print('НУ ЧЁ А ФОН КАКОЙ А? ВАРИАНТЫ 1 ИЛИ 2 ТАК И ПИШИ А!')
try:
    backgr = int(input())
    if backgr not in [1, 2]:
        print('НЕТУ ТАКОГО ВАРИАНТА ПОЧЕМУ ТЫ ТАК НАПИСАЛ А?????????????????')
        pygame.quit()
        sys.exit()
except ValueError:
    print('ЭЭЭЭ ТЫ ЧИСЛО ВВЕСТИ НЕ МОЖЕШЬ ЧТО ЛИ?? А????????')
    pygame.quit()
    sys.exit()

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ДИАЛОГ КОМБАТ")
clock = pygame.time.Clock()

# Загрузка текстур
try:
    bg_back = pygame.image.load("textures/background_back.png").convert_alpha()
    bg_mid = pygame.image.load("textures/background_mid.png").convert_alpha()
    bg_front = pygame.image.load("textures/background_front.png").convert_alpha()
    bg_back_2 = pygame.image.load("textures/background_back_2.png").convert_alpha()
    print('ТЕКСТУРЫ ЗАГРУЗИЛИСЬ УРАААААААААААААААААААААААААА')
except Exception as e:
    print(f"БЛИН ТЕКСТУР НЕТУ ЧЕЛ!! ТЫ НЕ ЗАГРУЗИЛ!! КАРОЧ Я ЗАГЛУШКИ СДЕЛАЮУ. ОШИБКА: {e}")
    # Создаем заглушки для текстур
    bg_back = pygame.Surface((SCREEN_WIDTH, 720))
    bg_back.fill(BLUE)
    bg_mid = pygame.Surface((SCREEN_WIDTH, 357))
    bg_mid.fill(GREEN)
    bg_front = pygame.Surface((960, 329))
    bg_front.fill(RED)
    bg_back_2 = pygame.Surface((SCREEN_WIDTH, 720))
    bg_back_2.fill((100, 100, 255))

# Масштабирование текстур
bg_front = pygame.transform.scale(bg_front, (960, SCREEN_HEIGHT // 2))
bg_mid = pygame.transform.scale(bg_mid, (SCREEN_WIDTH * 2, SCREEN_HEIGHT // 2))
bg_back = pygame.transform.scale(bg_back, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))
bg_back_2 = pygame.transform.scale(bg_back_2, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))

# Создаем игроков
player1 = Player(200, 360, 50, 50, RED, {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d
})

player2 = Player(700, 360, 50, 50, BLUE, {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
})

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
        if backgr == 1:
            surface.blit(bg_back, (self.back_pos - (bg_back.get_width() - SCREEN_WIDTH) // 2, back_y))
        else:
            surface.blit(bg_back_2, (self.back_pos - (bg_back_2.get_width() - SCREEN_WIDTH) // 2, back_y))
        
        # Средний слой
        mid_y = 350
        surface.blit(bg_mid, (self.mid_pos - (bg_mid.get_width() - SCREEN_WIDTH) // 2, mid_y))
        
        # Передний слой
        front_y = SCREEN_HEIGHT - bg_front.get_height()
        surface.blit(bg_front, (self.front_pos, front_y))
        surface.blit(bg_front, (self.front_pos + bg_front.get_width(), front_y))
        surface.blit(bg_front, (self.front_pos - bg_front.get_width(), front_y))

# Создаем параллакс-фон
parallax_bg = ParallaxBackground()

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Обновление игроков
    keys = pygame.key.get_pressed()
    player1.update(keys)
    player2.update(keys)
    
    # Обновление фона на основе средней точки
    midpoint = get_midpoint(player1, player2)
    parallax_bg.update(midpoint[0])
    
    # Отрисовка
    screen.fill(BLACK)
    parallax_bg.draw(screen)
    player1.draw(screen)
    player2.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

# Выход
print('ИГРА ЗАКРЫЛАСЬ! ПОЧЕМУ ТЫ ВЫШЕЛ АААААААААААААААААА?')
pygame.quit()
sys.exit()