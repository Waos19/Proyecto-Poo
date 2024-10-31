from Character import Character
import os
import pygame

class Fighter(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Cambiamos la imagen específica de Fighter
        image_path = os.path.join('assets', 'Sprites', 'Player', 'Nairan - Fighter - Base.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Carga la imagen de Fighter
        self.image = pygame.transform.scale(self.original_image, (self.rect.width, self.rect.height))  # Escala la imagen
        self.rect = self.image.get_rect(center=(x, y))  # Ajusta el rectángulo de colisión

        # Ajustes específicos para Fighter
        self.max_health = 80  
        self.current_health = self.max_health
        self.max_ammo = 40  
        self.current_ammo = self.max_ammo
        self.speed = 7
        self.collision_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
