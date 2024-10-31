import pygame

class Booster:
    def __init__(self, booster_type, duration, image_path):
        self.booster_type = booster_type  # Tipo de potenciador
        self.duration = duration  # Duración del efecto en segundos
        self.active = False  # Estado del potenciador (activo o no)
        self.start_time = None  # Momento en que se activa el potenciador
        self.position = (0, 0)  # Posición del potenciador en el mundo
        self.image = pygame.image.load(image_path).convert_alpha()  # Cargar la imagen

    def activate(self, player):
        """Activar el potenciador, aplicando su efecto al jugador."""
        if not self.active:
            self.active = True
            self.start_time = pygame.time.get_ticks()  # Guarda el tiempo actual
            self.apply_effect(player)  # Aplica el efecto al jugador

    def apply_effect(self, player):
        """Método a ser sobrescrito por las subclases para aplicar efectos específicos."""
        raise NotImplementedError("Este método debe ser implementado en las subclases.")

    def update(self):
        """Actualizar el estado del potenciador para comprobar si debe desactivarse."""
        if self.active:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Tiempo transcurrido en segundos
            if elapsed_time >= self.duration:
                self.deactivate()

    def deactivate(self):
        """Desactivar el potenciador."""
        self.active = False
        self.start_time = None

    def draw(self, screen, camera):
        """Dibujar el potenciador en la pantalla usando su imagen."""
        image_rect = self.image.get_rect(center=camera.apply_pos(self.position))  # Centrar la imagen en la posición
        screen.blit(self.image, image_rect)  # Dibujar la imagen en la pantalla
