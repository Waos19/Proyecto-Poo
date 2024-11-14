from Weapons import Weapon

class MachineGun(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.max_ammo = 100
        self.current_ammo = self.max_ammo
        self.shoot_cooldown = 650  # Disparo rápido para la ametralladora
        self.damage = 7
        self.bullet_speed = 8.5