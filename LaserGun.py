# weapon.py
import pygame
import random
from Bullet import Bullet
from Weapons import Weapon
import Settings

class LaserGun(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.max_ammo = 50
        self.current_ammo = self.max_ammo
        self.shoot_cooldown = 80  # Rápido
        self.heat = 0  # Nivel de sobrecalentamiento actual
        self.max_heat = 100  # Máximo nivel de sobrecalentamiento
        self.overheat_threshold = 80  # Umbral de sobrecalentamiento (por encima no puede disparar)
        self.heat_increase_per_shot = 5  # Calor generado por cada disparo
        self.heat_dissipation_rate = 2  # Cuánto se enfría por cada frame si no dispara
        self.is_overheated = False  # Estado de sobrecalentamiento
        self.damage = 5

    def shoot(self, angle):
        current_time = pygame.time.get_ticks()
        
        # Disparar solo si no está sobrecalentada
        if not self.reloading and not self.is_overheated and (current_time - self.last_shot_time) > self.shoot_cooldown:
            bullet = Bullet(self.shooter.rect.center, angle, self.shooter, self.damage)
            self.bullets.add(bullet)
            self.last_shot_time = current_time
            
            # Aumentar el calor
            self.heat += self.heat_increase_per_shot
            if self.heat >= self.max_heat:
                self.is_overheated = True  # Sobrecargar el arma si llega al límite
            
            return True  # Indicar que se disparó correctamente
        return False  # Indicar que no se pudo disparar

    def update(self):
        # Si está sobrecalentada, comprobar si el calor ha bajado lo suficiente para reactivarse
        if self.is_overheated and self.heat <= self.overheat_threshold:
            self.is_overheated = False

        # Disipar el calor si no está disparando
        if self.heat > 0:
            self.heat -= self.heat_dissipation_rate
            self.heat = max(0, self.heat)  # Asegurarse de que el calor no sea negativo

        # Llamar a la actualización de Weapon (para recargar y otras funciones)
        super().update()

    def draw_heat_bar(self, screen):
        # Dibujar la barra de sobrecalentamiento en la pantalla
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 80
        
        # Progreso de la barra (basado en el calor actual)
        heat_ratio = self.heat / self.max_heat
        filled_width = bar_width * heat_ratio
        bar_color = (255, 0, 0) if self.is_overheated else (255, 165, 0)  # Cambia de color si está sobrecalentada

        # Dibujar la barra
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)  # Bordes de la barra
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, filled_width, bar_height))  # Relleno de la barra
