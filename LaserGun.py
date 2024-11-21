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
        self.bullet_speed = 12
        self.bullets = []