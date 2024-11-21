# weapon.py
from Bullet import Bullet
from Weapons import Weapon

class LaserGun(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.max_ammo = 50
        self.current_ammo = self.max_ammo
        self.shoot_cooldown = 80  # Rápido
        self.damage = 5
        self.bullet_speed = 12
        self.bullets = []
