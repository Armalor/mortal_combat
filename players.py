import pygame
from abc import ABC

from utils import get_pure_path


class Player (ABC):
    """Это базовый абстрактный класс, создавать его объекты НЕЛЬЗЯ. """

    TEXTURES = []

    NAME = None
    
    def __init__(self, x, y, screen, controls, flip=False, is_player1=True):
        
        try:
            self.original_base = pygame.image.load(self.TEXTURES[0]).convert_alpha()
            self.original_block = pygame.image.load(self.TEXTURES[1]).convert_alpha()
            self.original_strike1 = pygame.image.load(self.TEXTURES[2]).convert_alpha()
            self.original_strike2 = pygame.image.load(self.TEXTURES[3]).convert_alpha()
            self.original_strike3 = pygame.image.load(self.TEXTURES[4]).convert_alpha()

        except Exception as err:
            print(f'{type(err)}: {err}')
            self.create_original_placeholder_textures()
        
        self.base = self.original_base.copy()
        self.block = self.original_block.copy()
        self.strike1 = self.original_strike1.copy()
        self.strike2 = self.original_strike2.copy()
        self.strike3 = self.original_strike3.copy()
        
        self.current_texture = self.base
        self.rect = self.current_texture.get_rect()
        self.rect.midbottom = (x, y)
        self.screen = screen
        self.velocity = 5
        self.controls = controls
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_cooldown = 0
        self.flip = flip
        self.should_flip = flip
        self.is_player1 = is_player1
        
        self.hp = 100
        self.max_hp = 100
        self.BLOCK = False
        self.last_hit_time = 0
        self.hit_cooldown = 500
        self.attack_range = 100
        self.is_alive = True
    
    def create_original_placeholder_textures(self):
        # Размеры для первого бойца
        size1 = (50, 80)
        # Размеры для второго бойца (уменьшенные)
        size2_base = (int(50 / 4.1), int(80 / 4.1))
        size2_other = (int(50 / 2), int(80 / 2))

        self.original_base = pygame.Surface(size1, pygame.SRCALPHA)
        pygame.draw.rect(self.original_base, (255, 0, 0, 255), (0, 0, size1[0], size1[1]))
        pygame.draw.polygon(self.original_base, (255, 255, 255, 255),
                            [(40, 10), (10, 40), (40, 70)])

        self.original_block = pygame.Surface(size1, pygame.SRCALPHA)
        self.original_block.fill((0, 255, 0, 255))

        self.original_strike1 = pygame.Surface(size1, pygame.SRCALPHA)
        self.original_strike1.fill((255, 255, 0, 255))

        self.original_strike2 = pygame.Surface(size1, pygame.SRCALPHA)
        self.original_strike2.fill((255, 165, 0, 255))

        self.original_strike3 = pygame.Surface(size1, pygame.SRCALPHA)
        self.original_strike3.fill((255, 69, 0, 255))
    
    def update_texture_direction(self, other_player):
        if not self.is_alive or not other_player.is_alive:
            return
            
        new_flip = self.rect.centerx > other_player.rect.centerx
        
        if new_flip != self.should_flip:
            self.should_flip = new_flip
            self.base = pygame.transform.flip(self.original_base, self.should_flip, False)
            self.block = pygame.transform.flip(self.original_block, self.should_flip, False)
            self.strike1 = pygame.transform.flip(self.original_strike1, self.should_flip, False)
            self.strike2 = pygame.transform.flip(self.original_strike2, self.should_flip, False)
            self.strike3 = pygame.transform.flip(self.original_strike3, self.should_flip, False)
            
            if self.is_attacking:
                if self.attack_frame < 5:
                    self.current_texture = self.strike1
                elif self.attack_frame < 10:
                    self.current_texture = self.strike2
                elif self.attack_frame < 15:
                    self.current_texture = self.strike3
            else:
                self.current_texture = self.base
    
    def check_hit(self, other_player):
        if not self.is_alive or not other_player.is_alive:
            return
            
        current_time = pygame.time.get_ticks()
        if (self.is_attacking and 5 <= self.attack_frame < 15 and
            abs(self.rect.centerx - other_player.rect.centerx) < self.attack_range and
            abs(self.rect.centery - other_player.rect.centery) < 100 and
            current_time - other_player.last_hit_time > self.hit_cooldown):
            
            damage = 1 if other_player.BLOCK else 10
            other_player.hp = max(0, other_player.hp - damage)
            other_player.last_hit_time = current_time
            
            if other_player.hp <= 0:
                other_player.is_alive = False
    
    def update(self, keys, other_player):
        if not self.is_alive:
            return
            
        self.update_texture_direction(other_player)
        
        if keys[self.controls["left"]]:
            self.rect.x -= self.velocity
        if keys[self.controls["right"]]:
            self.rect.x += self.velocity
        
        if keys[self.controls["attack"]] and self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_cooldown = 30
        
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame < 5:
                self.current_texture = self.strike1
            elif self.attack_frame < 10:
                self.current_texture = self.strike2
            elif self.attack_frame < 15:
                self.current_texture = self.strike3
            else:
                self.is_attacking = False
                self.current_texture = self.base
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.rect.x = max(0, min(self.rect.x, self.screen.get_width() - self.rect.width))
        self.check_hit(other_player)
    
    def draw_hp_bar(self):
        if not self.is_alive:
            return
            
        bar_width = 200
        bar_height = 20
        hp_width = int((self.hp / self.max_hp) * bar_width)
        
        if self.is_player1:
            x = 20
            text_x = x + 10
            color = (255, 0, 0)
        else:
            x = self.screen.get_width() - bar_width - 20
            text_x = x + bar_width - 190
            color = (0, 0, 255)
        
        y = 20
        
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, color, (x, y, hp_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        font = pygame.font.Font(get_pure_path('fonts/verdanab.ttf'), 12)
        text = font.render(f"Игрок {'1' if self.is_player1 else '2'}:     {self.hp}/{self.max_hp}", True, (255, 255, 255))
        self.screen.blit(text, (text_x, y + 2))
    
    def draw(self):
        if self.is_alive:
            self.screen.blit(self.current_texture, self.rect)
            self.draw_hp_bar()


class Player1(Player):

    NAME = 'Мега-СВШ'

    TEXTURES = [
            get_pure_path('textures/1_svsh/base.png'),
            get_pure_path('textures/1_svsh/block.png'),
            get_pure_path('textures/1_svsh/strike1.png'),
            get_pure_path('textures/1_svsh/strike2.png'),
            get_pure_path('textures/1_svsh/strike3.png'),
        ]


class Player2(Player):

    NAME = 'Человек-Борян'

    TEXTURES = [
            get_pure_path('textures/2_boris_chai/base.png'),
            get_pure_path('textures/2_boris_chai/block.png'),
            get_pure_path('textures/2_boris_chai/strike1.png'),
            get_pure_path('textures/2_boris_chai/strike2.png'),
            get_pure_path('textures/2_boris_chai/strike3.png'),
        ]


class Player3(Player):

    NAME = 'Гигантский Стефан'

    TEXTURES = [
            get_pure_path('textures/3_gigant_stefan/base.png'),
            get_pure_path('textures/3_gigant_stefan/base.png'),
            get_pure_path('textures/3_gigant_stefan/base.png'),
            get_pure_path('textures/3_gigant_stefan/base.png'),
            get_pure_path('textures/3_gigant_stefan/base.png'),
        ]


def get_midpoint(player1: Player, player2: Player):

    return ((player1.rect.centerx + player2.rect.centerx) // 2, 
            (player1.rect.centery + player2.rect.centery) // 2)
