import pygame
import sys

class VolumeBar:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.volume = 0.5  # Volumen inicial (0.0 a 1.0)
        self.slider_width = 10
        self.slider_pos = x + int(width * self.volume)  # Posición del slider

    def draw(self, surface):
        # Dibujar la barra de fondo
        pygame.draw.rect(surface, (200, 200, 200), self.rect)  # Barra de fondo
        # Dibujar la barra de volumen
        pygame.draw.rect(surface, (0, 150, 0), (self.rect.x, self.rect.y, int(self.rect.width * self.volume), self.rect.height))  # Barra de volumen
        # Dibujar el slider
        pygame.draw.rect(surface, (0, 0, 0), (self.slider_pos, self.rect.y, self.slider_width, self.rect.height))  # Slider

    def is_clicked(self, pos):
        # Comprobar si el botón fue clickeado o si el mouse esta encima del boton
        return self.rect.collidepoint(pos)
    
    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            # Calcular el nuevo volumen basado en la posición del clic
            mouse_x = pos[0]
            # Asegurarse de que el volumen esté en el rango [0.0, 1.0]
            self.volume = max(0, min(1, (mouse_x - self.rect.x) / self.rect.width))
            self.slider_pos = self.rect.x + int(self.rect.width * self.volume)  # Actualizar posición del slider
            pygame.mixer.music.set_volume(self.volume)  # Actualizar el volumen de la música
