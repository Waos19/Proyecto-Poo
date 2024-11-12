import pygame
import math 

class Buttons:
    def __init__(self, image_path, hover_image_path, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.hover_image = pygame.image.load(hover_image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

    def draw(self, surface, mouse_pos):
        # Cambiar la imagen si el mouse está sobre el botón
        if self.is_clicked(mouse_pos):
            surface.blit(self.hover_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        # Comprobar si el botón fue clickeado o si el mouse esta encima del boton
        return self.rect.collidepoint(pos)

class CircularButton(Buttons):
    def __init__(self, image_path, hover_image_path, x, y, radius):
        # Calculamos el ancho y alto del rectángulo que encierra el círculo
        super().__init__(image_path, hover_image_path, x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.center = (x, y)
    def draw(self, surface, mouse_pos):
        # Cambiar la imagen si el mouse está sobre el botón
        if self.is_hovered(mouse_pos):
            surface.blit(self.hover_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)
    def is_hovered(self, pos):
        # Comprobar si el mouse está sobre el botón circular
        distance = math.sqrt((pos[0] - self.center[0]) ** 2 + (pos[1] - self.center[1]) ** 2)
        return distance <= self.radius
    def is_clicked(self, pos):
        # Comprobar si el botón circular fue clickeado
        return self.is_hovered(pos)
