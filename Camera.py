import pygame, Settings


class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        self.camera_rect = self.calculate_camera_rect(target)

    def calculate_camera_rect(self, target):
        x = -target.rect.centerx + int(Settings.Width / 2)
        y = -target.rect.centery + int(Settings.Height / 2)

        x = min(0, x)
        x = max(-(self.width - Settings.Width), x)
        y = min(0, y)
        y = max(-(self.height - Settings.Height), y)

        return pygame.Rect(x, y, self.width, self.height)

    def apply_pos(self, pos):
        x, y = pos
        return x + self.camera_rect.x, y + self.camera_rect.y

