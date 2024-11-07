# Pistol.py
from Weapons import Weapon

class Pistol(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.max_ammo = 12  # Máxima munición de la pistola
        self.current_ammo = self.max_ammo
        self.shoot_cooldown = 500  # Tiempo de recarga más largo para la pistola
        self.reload_time = 1500  # Tiempo de recarga
        self.damage = 3
