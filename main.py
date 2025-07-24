import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FPS = 60

# Цвета (на случай, если текстуры не загрузятся)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Выбор фонов
print('НУ ЧЁ А ФОН КАКОЙ А? ВАРИАНТЫ 1 ИЛИ 2 ТАК И ПИШИ А!')
backgr = int(input())
if not (backgr == 1 or backgr == 2):
    print('НЕТУ ТАКОГО ВАРИАНТА ПОЧЕМУ ТЫ ТАК НАПИСАЛ А?????????????????')
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
except:
    print("БЛИН ТЕКСТУР НЕТУ ЧЕЛ!! ТЫ НЕ ЗАГРУЗИЛ!! КАРОЧ Я ЗАГЛУШКИ СДЕЛАЮУ")
    # Создаем заглушки для текстур
    bg_back = pygame.Surface((SCREEN_WIDTH, 720))
    bg_back.fill(BLUE)
    bg_mid = pygame.Surface((SCREEN_WIDTH, 357))
    bg_mid.fill(GREEN)
    bg_front = pygame.Surface((960, 329))
    bg_front.fill(RED)

# Масштабирование текстур под нужные размеры
# Передний план - 1/3 экрана (329 / 720 ≈ 0.457, близко к 1/3)
bg_front = pygame.transform.scale(bg_front, (960, SCREEN_HEIGHT // 2))
# Средний слой - половина экрана (357 / 720 ≈ 0.496, близко к 1/2)
bg_mid = pygame.transform.scale(bg_mid, (SCREEN_WIDTH * 2, SCREEN_HEIGHT // 2))
# Дальний слой - чуть больше экрана (720 / 720 = 1.0, но он должен быть больше)
bg_back = pygame.transform.scale(bg_back, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))
# Дальний слой 2 - чуть больше экрана (720 / 720 = 1.0, но он должен быть больше)
bg_back_2 = pygame.transform.scale(bg_back_2, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))

# Параллакс-эффект
class ParallaxBackground:
    def __init__(self):
        self.back_pos = 0
        self.mid_pos = 0
        self.front_pos = 0
        self.max_offset = 960  # Максимальное смещение (ширина переднего слоя)
        
        # Коэффициенты параллакса (как быстро движется каждый слой)
        self.back_speed = 0.3  # Должен прокручиваться половину раза
        self.mid_speed = 0.5   # Должен прокручиваться один раз
        self.front_speed = 2.0  # Должен прокручиваться два раза
        
        # Максимальные смещения для среднего и заднего слоев
        self.max_mid_offset = (bg_mid.get_width() - SCREEN_WIDTH) / 2
        self.max_back_offset = (bg_back.get_width() - SCREEN_WIDTH) / 2
    
    def update(self, direction):
        # direction: -1 - влево, 1 - вправо, 0 - остановка
        
        # Обновляем позиции с ограничениями
        if direction != 0:
            # Обновляем позицию переднего слоя
            new_front_pos = self.front_pos + direction * self.front_speed
            if abs(new_front_pos) <= self.max_offset:
                self.front_pos = new_front_pos
            
            # Рассчитываем позиции других слоев на основе переднего
            # (чтобы сохранить пропорции параллакса)
            progress = self.front_pos / self.max_offset
            self.mid_pos = progress * self.max_mid_offset
            self.back_pos = progress * self.max_back_offset
    
    def draw(self, surface):
        # Рисуем задний слой (только одну картинку)
        back_y = (SCREEN_HEIGHT - bg_back.get_height()) // 2
        if backgr == 1:
            surface.blit(bg_back, (self.back_pos - (bg_back.get_width() - SCREEN_WIDTH) // 2, back_y))
        elif backgr == 2:
            surface.blit(bg_back_2, (self.back_pos - (bg_back_2.get_width() - SCREEN_WIDTH) // 2, back_y))
        # Рисуем средний слой (только одну картинку)
        mid_y = 350
        surface.blit(bg_mid, (self.mid_pos - (bg_mid.get_width() - SCREEN_WIDTH) // 2, mid_y))
        
        # Рисуем передний слой (с повторением)
        front_y = SCREEN_HEIGHT - bg_front.get_height()
        surface.blit(bg_front, (self.front_pos, front_y))
        surface.blit(bg_front, (self.front_pos + bg_front.get_width(), front_y))
        surface.blit(bg_front, (self.front_pos - bg_front.get_width(), front_y))

# Создаем параллакс-фон
parallax_bg = ParallaxBackground()

# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Обработка клавиш
    keys = pygame.key.get_pressed()
    direction = 0
    if keys[pygame.K_LEFT]:
        direction = 5  # Движение фона влево (объекты двигаются вправо)
    elif keys[pygame.K_RIGHT]:
        direction = -5  # Движение фона вправо (объекты двигаются влево)
    
    # Обновление
    parallax_bg.update(direction)
    
    # Отрисовка
    screen.fill(BLACK)  # Заполняем черным (на случай, если текстуры не покроют весь экран)
    parallax_bg.draw(screen)
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

# Выход из игры
pygame.quit()
sys.exit()