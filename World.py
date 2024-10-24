import pygame

class World:
    # Constructor del mundo
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = pygame.image.load('assets/Background/SpaceBg.jpg').convert_alpha()
    
    # Método que dibuja al mundo teniendo en cuenta la cámara
    def Draw(self, screen, camera):
        # Ajustar la posición del fondo usando la cámara
        screen.blit(self.background, camera.apply(self))

    # Necesitamos un rectángulo para que la cámara pueda aplicar su lógica
    @property
    def rect(self):
        return pygame.Rect(0, 0, self.width, self.height)
