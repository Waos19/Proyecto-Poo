from Character import Character
import os
import pygame

class Scout(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        image_path = os.path.join('assets', 'Sprites', 'Player', 'Nairan_-_Fighter_-_Engine_ Sprite.png')
        self.set_sprite(image_path)  # Cambiar sprite usando el método 'set_sprite'

        self.max_health = 75  
        self.current_health = self.max_health
        self.max_ammo = 25  
        self.current_ammo = self.max_ammo
        self.speed =10  
        self.armor = 50
        
        # Personalización de la hitbox para el Tank (más grande para reflejar su tamaño)
        self.collision_rect = pygame.Rect(self.x - 30, self.y - 30, 60, 60)

    def draw_health(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (10, 40, self.health_bar_length, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 40, self.current_health / self.health_ratio, 20))