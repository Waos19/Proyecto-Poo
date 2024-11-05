from Weapons import Weapon

class MachineGun(Weapon):
    def __init__(self, shooter):
        super().__init__(shooter)
        self.shoot_cooldown = 50  # Disparo más rápido