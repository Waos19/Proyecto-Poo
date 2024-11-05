import pygame, Settings


class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Devuelve la posición ajustada de la entidad en función de la cámara
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        # Centra la cámara en el jugador
        self.camera_rect = self.calculate_camera_rect(target)

    def calculate_camera_rect(self, target):
        # Calcula el desplazamiento de la cámara
        x = -target.rect.centerx + int(Settings.Width / 2)
        y = -target.rect.centery + int(Settings.Height / 2)
        
        # Restringe el desplazamiento para que la cámara no muestre zonas vacías
        x = min(0, x)  # No dejar mover más allá de la izquierda
        x = max(-(self.width - Settings.Width), x)  # No dejar mover más allá de la derecha
        y = min(0, y)  # No dejar mover más allá de arriba
        y = max(-(self.height - Settings.Height), y)  # No dejar mover más allá de abajo
        
        return pygame.Rect(x, y, self.width, self.height)
