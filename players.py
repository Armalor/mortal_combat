import pygame

class Player:
    def __init__(self, x, y, width, height, color, controls):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.controls = controls  # Словарь с клавишами управления
        self.speed = 5
    
    def update(self, keys):
        if keys[self.controls["up"]]:
            self.rect.y -= self.speed
        if keys[self.controls["down"]]:
            self.rect.y += self.speed
        if keys[self.controls["right"]]:
            self.rect.x -= self.speed
        if keys[self.controls["left"]]:
            self.rect.x += self.speed
        
        # Ограничение движения в пределах экрана
        self.rect.x = max(0, min(self.rect.x, 960 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 720 - self.rect.height))
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

def get_midpoint(player1, player2):
    return ((player1.rect.centerx + player2.rect.centerx) // 2, 
            (player1.rect.centery + player2.rect.centery) // 2)