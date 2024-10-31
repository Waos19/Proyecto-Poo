from Boosters import Booster

class WeaponBooster(Booster):
    def __init__(self, x, y, duration):
        image_path = 'assets/Sprites/Boosters/weapon_booster.png'  # Ruta de la imagen del potenciador de armas
        super().__init__('weapon', duration, image_path)
        self.position = (x, y)

    def apply_effect(self, player):
        """Proporcionar un nuevo arma al jugador."""
        player.add_weapon("Laser")  # Ejemplo: agregar un arma láser
