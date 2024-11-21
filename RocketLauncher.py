from Weapons import Weapon
from Bullet import Bullet
import math
import pygame

class RocketLauncher(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.max_ammo = 5  # Menos munición
        self.current_ammo = self.max_ammo
        self.shoot_cooldown = 1000  # Disparo más 
        self.damage = 20
        self.bullet_speed = 9
        self.bullets = []

    def shoot(self, angle):
        current_time = pygame.time.get_ticks()
        if not self.reloading and self.current_ammo > 0 and (current_time - self.last_shot_time) > self.shoot_cooldown:
            radius = self.shooter.rect.width / 2
            bullet_x = self.shooter.x + radius * math.cos(math.radians(angle))
            bullet_y = self.shooter.y - radius * math.sin(math.radians(angle))

            bullet = Bullet((bullet_x, bullet_y), angle, self.shooter, self.damage, self.bullet_speed)  # Sin dispersión
            self.bullets.append(bullet)
            self.current_ammo -= 1
            self.last_shot_time = current_time

            if self.current_ammo == 0:
                self.reload()