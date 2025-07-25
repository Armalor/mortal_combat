import pygame

class Player:
    # Текстуры для разных воинов (warrior 1 и warrior 2)
    TEXTURES = {
        1: [
            'textures/base.png',
            'textures/block.png',
            'textures/strike1.png',
            'textures/strike2.png',
            'textures/strike3.png'
        ],
        2: [
            'textures/2_base.png',
            'textures/2_block.png',
            'textures/2_strike1.png',
            'textures/2_strike2.png',
            'textures/2_strike3.png'
        ]
    }
    
    def __init__(self, x, y, screen, controls, flip=False, is_player1=True, warrior=1):
        self.warrior = warrior if is_player1 else 2  # Игрок 1 - warrior 1, игрок 2 - warrior 2
        
        try:
            self.original_base = pygame.image.load(self.TEXTURES[self.warrior][0]).convert_alpha()
            self.original_block = pygame.image.load(self.TEXTURES[self.warrior][1]).convert_alpha()
            self.original_strike1 = pygame.image.load(self.TEXTURES[self.warrior][2]).convert_alpha()
            self.original_strike2 = pygame.image.load(self.TEXTURES[self.warrior][3]).convert_alpha()
            self.original_strike3 = pygame.image.load(self.TEXTURES[self.warrior][4]).convert_alpha()
            
            print(pygame.image.load(self.TEXTURES[self.warrior][4]).convert_alpha())

            # Масштабирование текстур для второго бойца
            if self.warrior == 2:
                self.original_base = pygame.transform.scale(self.original_base, 
                    (int(self.original_base.get_width() / 4.1), 
                     int(self.original_base.get_height() / 4.1)))
                self.original_block = pygame.transform.scale(self.original_block, 
                    (int(self.original_block.get_width() // 2), 
                     int(self.original_block.get_height() // 2)))
                self.original_strike1 = pygame.transform.scale(self.original_strike1, 
                    (int(self.original_strike1.get_width() // 2), 
                     int(self.original_strike1.get_height() // 2)))
                self.original_strike2 = pygame.transform.scale(self.original_strike2, 
                    (int(self.original_strike2.get_width() // 2), 
                     int(self.original_strike2.get_height() // 2)))
                self.original_strike3 = pygame.transform.scale(self.original_strike3, 
                    (int(self.original_strike3.get_width() // 2), 
                     int(self.original_strike3.get_height() // 2)))
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
        
        # Для warrior 1
        if self.warrior == 1:
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
        # Для warrior 2
        else:
            self.original_base = pygame.Surface(size2_base, pygame.SRCALPHA)
            pygame.draw.rect(self.original_base, (0, 0, 255, 255), (0, 0, size2_base[0], size2_base[1]))
            pygame.draw.polygon(self.original_base, (255, 255, 255, 255), 
                              [(size2_base[0]-10, 10), (10, size2_base[1]//2), (size2_base[0]-10, size2_base[1]-10)])
            
            self.original_block = pygame.Surface(size2_other, pygame.SRCALPHA)
            self.original_block.fill((255, 0, 255, 255))
            
            self.original_strike1 = pygame.Surface(size2_other, pygame.SRCALPHA)
            self.original_strike1.fill((0, 255, 255, 255))
            
            self.original_strike2 = pygame.Surface(size2_other, pygame.SRCALPHA)
            self.original_strike2.fill((0, 165, 255, 255))
            
            self.original_strike3 = pygame.Surface(size2_other, pygame.SRCALPHA)
            self.original_strike3.fill((0, 69, 255, 255))
    
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
        if (self.is_attacking and 
            self.attack_frame >= 5 and self.attack_frame < 15 and
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
        hp_width = (self.hp / self.max_hp) * bar_width
        
        if self.is_player1:
            x = 20
            text_x = x + 10
            color = (255, 0, 0)
        else:
            x = self.screen.get_width() - bar_width - 20
            text_x = x + bar_width - 110
            color = (0, 0, 255)
        
        y = 20
        
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, color, (x, y, hp_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        font = pygame.font.Font(None, 24)
        text = font.render(f"Игрок {'1' if self.is_player1 else '2'}: {self.hp}/{self.max_hp}", True, (255, 255, 255))
        self.screen.blit(text, (text_x, y - 2))
    
    def draw(self):
        if self.is_alive:
            self.screen.blit(self.current_texture, self.rect)
            self.draw_hp_bar()

def get_midpoint(player1, player2):
    return ((player1.rect.centerx + player2.rect.centerx) // 2, 
            (player1.rect.centery + player2.rect.centery) // 2)