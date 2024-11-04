from Character import Character
import os
import pygame

class Tank(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        image_path = os.path.join('assets', 'Sprites', 'Player', 'Klaed - Frigate - Base.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Carga la imagen de Fighter
        self.image = pygame.transform.scale(self.original_image, (self.rect.width, self.rect.height))  # Escala la imagen
        self.rect = self.image.get_rect(center=(x, y))  # Ajusta el rectángulo de colisión
        self.max_health = 200
        self.current_health = self.max_health
        self.max_ammo = 20  
        self.current_ammo = self.max_ammo
        self.speed = 4.5  
        self.armor = 50
        
        # Personalización de la hitbox para el Tank (más grande para reflejar su tamaño)
        self.collision_rect = pygame.Rect(self.x - 30, self.y - 30, 60, 60)