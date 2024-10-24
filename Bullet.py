import pygame
import math
import Settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, shooter):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.x, self.y = pos
        self.angle = angle
        self.speed = 5
        self.damage = 10
        self.shooter = shooter

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def is_off_screen(self):
        return self.x < 0 or self.x > Settings.world_width or self.y < 0 or self.y > Settings.world_heigh

    def check_collision(self, player):
        if player != self.shooter and player.check_bullet_collision(self):
            player.take_damage(self.damage)
            self.kill()