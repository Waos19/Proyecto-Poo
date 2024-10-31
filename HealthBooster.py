from Boosters import Booster

class HealthBooster(Booster):
    def __init__(self, x, y, duration):
        image_path = 'assets/Sprites/Boosters/health.png'  # Ruta de la imagen del potenciador de salud
        super().__init__('health', duration, image_path)
        self.position = (x, y)

    def apply_effect(self, player):
        """Restaurar salud al jugador."""
        player.current_health += 20  # Ejemplo: restaurar 20 puntos de salud
        player.current_health = min(player.current_health, player.max_health)  # No superar la salud máxima
