from Weapons import Weapon
from Bullet import Bullet
import math
import pygame

class LaserGun(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.heat = 0  # Calor actual
        self.max_heat = 100  # Calor máximo antes de sobrecalentarse
        self.heat_increase = 5  # Aumento de calor por disparo
        self.heat_decrease = 2  # Disminución de calor por segundo
        self.shooting = False  # Indica si se está disparando

    def shoot(self, angle):
        if self.heat < self.max_heat:  # Solo dispara si no se ha sobrecalentado
            current_time = pygame.time.get_ticks()
            radius = self.shooter.rect.width / 2
            bullet_x = self.shooter.x + radius * math.cos(math.radians(angle))
            bullet_y = self.shooter.y - radius * math.sin(math.radians(angle))

            bullet = Bullet((bullet_x, bullet_y), angle, self.shooter)
            self.bullets.add(bullet)
            self.current_ammo -= 1

            self.heat += self.heat_increase  # Aumenta el calor
            if self.heat >= self.max_heat:
                self.heat = self.max_heat  # Limitar el calor a su máximo

    def update(self):
        super().update()  # Actualiza la lógica de la clase base
        if self.shooting:
            self.shoot(self.shooter.lookAtMouse())  # Dispara continuamente mientras se mantiene el clic
        # Disminuye el calor con el tiempo
        if self.heat > 0:
            self.heat -= self.heat_decrease * (pygame.time.get_ticks() / 1000)  # Ajusta según el tiempo
            if self.heat < 0:
                self.heat = 0