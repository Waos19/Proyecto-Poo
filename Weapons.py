# weapon.py
import pygame
import math
import random
from Bullet import Bullet
import Settings

class Weapon:
    def __init__(self, shooter):
        self.shooter = shooter
        self.damage = 10  # Daño base (esto se puede sobrescribir en subclases)
        self.max_ammo = None  # Armas ilimitadas tendrán None como munición máxima
        self.current_ammo = None
        self.reload_time = 2000
        self.last_reload_time = 0
        self.reloading = False
        self.shoot_cooldown = 100
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)

    def shoot(self, angle):
        current_time = pygame.time.get_ticks()
        
        if not self.reloading and self.current_ammo != 0 and (current_time - self.last_shot_time) > self.shoot_cooldown:
            bullet = Bullet(self.shooter.rect.center, angle, self.shooter, self.damage)
            self.bullets.add(bullet)
            self.last_shot_time = current_time
            if self.current_ammo is not None:
                self.current_ammo -= 1
            return True
        return False

    def reload(self):
        if not self.reloading and self.current_ammo < self.max_ammo:
            self.reloading = True
            self.last_reload_time = pygame.time.get_ticks()

    def draw_bullets(self, screen, camera):
        # Dibuja todas las balas en pantalla
        for bullet in self.bullets:
            bullet.draw(screen, camera)  # Utiliza el método `draw` de `Bullet`
            
    def DrawAmmo(self, screen):
        ammo_text = self.font.render(f'Munición: {self.current_ammo}', True, (255, 255, 255))
        screen.blit(ammo_text, (10, 10))  

        if self.reloading:
            current_time = pygame.time.get_ticks()
            reload_progress = (current_time - self.last_reload_time) / self.reload_time
            reload_bar_length = 200  
            bar_color = (0, 255, 0)  

            pygame.draw.rect(screen, bar_color, (10, 50, reload_bar_length * reload_progress, 20))

    def update(self):
        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_reload_time >= self.reload_time:
                self.current_ammo = self.max_ammo
                self.reloading = False
        self.bullets.update()
