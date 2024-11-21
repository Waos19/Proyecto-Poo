import pygame
import math
import random
from Bullet import Bullet
import Settings

class Weapon:
    def __init__(self, shooter):
        self.shooter = shooter
        self.damage = 10
        self.max_ammo = None
        self.current_ammo = None
        self.reload_time = 2000
        self.last_reload_time = 0
        self.reloading = False
        self.shoot_cooldown = 100
        self.last_shot_time = 0
        self.bullets = []
        self.font = pygame.font.Font("assets/Font/calamity.ttf", 36)
        self.bullet_speed = 100

    def shoot(self, angle):
        current_time = pygame.time.get_ticks()
        if not self.reloading and self.current_ammo != 0 and (current_time - self.last_shot_time) > self.shoot_cooldown:
            start_x, start_y = self.shooter.get_gun_position()
            # Pass shooter_id instead of shooter object
            bullet = Bullet((start_x, start_y), angle, self.shooter.id, self.damage, self.bullet_speed)
            self.bullets.append(bullet)
            self.last_shot_time = current_time
            if self.current_ammo is not None:
                self.current_ammo -= 1
            return True
        return False

    def reload(self):
        if not self.reloading and self.current_ammo < self.max_ammo:
            self.reloading = True
            self.last_reload_time = pygame.time.get_ticks()


    def DrawAmmo(self, screen):
        ammo_text = self.font.render(f'Municion: {self.current_ammo}', True, (255, 255, 255))
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
        for bullet in self.bullets:
            bullet.update()

            # Elimina las balas fuera de la pantalla o que hayan expirado
            if bullet.is_off_screen() or pygame.time.get_ticks() - bullet.creation_time > bullet.life_time:
                bullet.kill()
