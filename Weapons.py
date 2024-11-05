# weapon.py
import pygame
import math
import random
from Bullet import Bullet  # Asegúrate de que el nombre del archivo es correcto
import Settings

class Weapon:
    def __init__(self, shooter):
        self.shooter = shooter
        self.max_ammo = 30
        self.current_ammo = self.max_ammo
        self.reload_time = 2000  # Tiempo de recarga en milisegundos
        self.last_reload_time = 0
        self.reloading = False
        self.shoot_cooldown = 100  # Retraso entre disparos
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.magazines = 3  # Cantidad de cargadores

    def shoot(self):
        current_time = pygame.time.get_ticks()
        
        if not self.reloading and self.current_ammo > 0 and (current_time - self.last_shot_time) > self.shoot_cooldown:
            # Lógica para disparar
            self.current_ammo -= 1
            self.last_shot_time = current_time

            if self.current_ammo <= 0:
                self.magazines -= 1
                if self.magazines > 0:
                    self.reload()  # Recargar si hay cargadores restantes
                else:
                    self.current_ammo = 0  # Se queda sin munición
                    print("No more ammo in this weapon!")
                    return False  # Indicar que no se puede disparar

        return True  # Indicar que se disparó correctamente

    def reload(self):
        if not self.reloading and self.magazines > 0:
            self.reloading = True
            self.last_reload_time = pygame.time.get_ticks()
            self.current_ammo = self.max_ammo

    def update(self):
        # Lógica de actualización si es necesario
        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_reload_time >= self.reload_time:
                self.reloading = False

