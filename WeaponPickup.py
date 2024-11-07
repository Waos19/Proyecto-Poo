# weapon_pickups.py
import pygame
import random
import Settings

class WeaponPickup(pygame.sprite.Sprite):
    def __init__(self, weapon_type, pos):
        super().__init__()
        self.weapon_type = weapon_type
        self.image = self.load_image(weapon_type)
        self.rect = self.image.get_rect(center=pos)
    
    def load_image(self, weapon_type):
        # Cargar diferentes imágenes para cada tipo de arma
        if weapon_type == "LaserGun":
            return pygame.image.load("assets/Sprites/Boosters/2.png").convert_alpha()
        elif weapon_type == "MachineGun":
            return pygame.image.load("assets/Sprites/Boosters/0.png").convert_alpha()
        elif weapon_type == "RocketLauncher":
            return pygame.image.load("assets/Sprites/Boosters/1.png").convert_alpha()
    
    def update(self):
        # Puedes implementar lógica adicional, como rotación o animación
        pass
