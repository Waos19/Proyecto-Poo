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
        self.active = True  # Variable para determinar si el pickup está activo

    def load_image(self, weapon_type):
        # Cargar diferentes imágenes para cada tipo de arma
        if weapon_type == "LaserGun":
            return pygame.image.load("assets/Sprites/Boosters/2.png").convert_alpha()
        elif weapon_type == "MachineGun":
            return pygame.image.load("assets/Sprites/Boosters/0.png").convert_alpha()
        elif weapon_type == "RocketLauncher":
            return pygame.image.load("assets/Sprites/Boosters/1.png").convert_alpha()
        return pygame.Surface((32, 32))  # Retorna una imagen vacía si no se encuentra el tipo de arma

    def update(self, delta_time):
        # Lógica de actualización del pickup. Por ejemplo:
        # 1. Verificar si está fuera de los límites del mapa
        if not self.active:
            return  # No hacer nada si el pickup está inactivo

        # 2. Comprobar si el pickup sale de los límites del mapa y desactivarlo
        if self.rect.x < 0 or self.rect.x > Settings.world_width or self.rect.y < 0 or self.rect.y > Settings.world_height:
            self.active = False  # Desactivar el pickup si está fuera de los límites

        # 3. Otras posibles lógicas de animación o movimiento (si fuera necesario)
        # Por ejemplo, podrías hacer que el pickup se desplace lentamente por la pantalla
        # self.rect.x += 50 * delta_time

    def collides_with_player(self, player):
        # Verificar si el pickup colide con el jugador
        if self.rect.colliderect(player.rect):
            return True
        return False
