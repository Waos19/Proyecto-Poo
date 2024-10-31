from Character import Character
import os
import pygame

class Scout(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        image_path = os.path.join('assets', 'Sprites', 'Player', 'Nairan - Fighter - Base.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Carga la imagen de Fighter
        self.image = pygame.transform.scale(self.original_image, (self.rect.width, self.rect.height))  # Escala la imagen
        self.rect = self.image.get_rect(center=(x, y))  # Ajusta el rectángulo de colisión
        self.max_health = 60  
        self.current_health = self.max_health
        self.max_ammo = 25  
        self.current_ammo = self.max_ammo
        self.speed = 10  
        
        # Personalización de la hitbox para el Scout (pequeña para mayor maniobrabilidad)
        self.collision_rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)