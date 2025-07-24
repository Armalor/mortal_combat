import pygame
import sys
from players import Player, get_midpoint

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FPS = 60

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

# Загрузка текстур фона
try:
    bg_back = pygame.image.load("textures/background_back.png").convert_alpha()
    bg_mid = pygame.image.load("textures/background_mid.png").convert_alpha()
    bg_front = pygame.image.load("textures/background_front.png").convert_alpha()
    bg_back_2 = pygame.image.load("textures/background_back_2.png").convert_alpha()
    print('ТЕКСТУРЫ ФОНА ЗАГРУЗИЛИСЬ УРАААААААААААААААААААААААААА')
except Exception as e:
    print(f"БЛИН ТЕКСТУР ФОНА НЕТУ ЧЕЛ!! ОШИБКА: {e}")
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
bg_back = pygame.transform.scale(bg_back, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))
bg_back_2 = pygame.transform.scale(bg_back_2, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))

# Создаем игроков
player1 = Player(
    x=200, 
    y=720, 
    screen=screen,
    controls={
        "left": pygame.K_a,
        "right": pygame.K_d,
        "attack": pygame.K_RCTRL
    },
    flip=False,
    is_player1=True
)

player2 = Player(
    x=700, 
    y=720, 
    screen=screen,
    controls={
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "attack": pygame.K_f
    },
    flip=False,
    is_player1=False
)
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


# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    # Обновление игроков
    player1.update(keys, player2)
    player2.update(keys, player1)
    
    # Обновление фона
    midpoint = get_midpoint(player1, player2)
    parallax_bg.update(midpoint[0])
    
    # Отрисовка
    screen.fill((0, 0, 0))
    parallax_bg.draw(screen)
    player1.draw()
    player2.draw()
    
    pygame.display.flip()
    clock.tick(FPS)

# Выход
print('ИГРА ЗАКРЫЛАСЬ! ПОЧЕМУ ТЫ ВЫШЕЛ АААААААААААААААААА?')
pygame.quit()
sys.exit()