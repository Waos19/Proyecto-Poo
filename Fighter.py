from Character import Character
import os
import pygame

class Fighter(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        image_path = os.path.join('assets', 'Sprites', 'Player', 'Nautolan Ship - Scout - Sprite.png')
        self.set_sprite(image_path)  # Cambiar sprite usando el método 'set_sprite'

        self.max_health = 100  
        self.current_health = self.max_health
        self.max_ammo = 40  
        self.current_ammo = self.max_ammo
        self.speed=7
        self.armor = 50
        
        # Personalización de la hitbox para el Tank (más grande para reflejar su tamaño)
        self.collision_rect = pygame.Rect(self.x - 30, self.y - 30, 60, 60)