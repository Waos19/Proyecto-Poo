import pygame
import math
import Settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, shooter_id, damage, bullet_speed):
        super().__init__()
        self.original_image = pygame.Surface((10, 20))
        self.original_image.fill((255, 255, 255))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=pos)
        self.x, self.y = pos
        self.angle = angle
        self.speed = 5
        self.damage = damage
        self.shooter_id = shooter_id  # Store the shooter's ID instead of the shooter object
        self.life_time = 3000
        self.creation_time = pygame.time.get_ticks()
        self.bullet_speed = bullet_speed

    def update(self):
        self.x += self.bullet_speed * math.cos(math.radians(self.angle))
        self.y -= self.bullet_speed * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)
        if pygame.time.get_ticks() - self.creation_time > self.life_time:
            self.kill()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def is_off_screen(self):
        return self.x < 0 or self.x > Settings.world_width or self.y < 0 or self.y > Settings.world_height

    def check_collision(self, player_id, player_rect):
        # Check collision using player_id instead of player object
        if player_id != self.shooter_id and self.rect.colliderect(player_rect):
            return True
        return False

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "shooter_id": self.shooter_id,
            "damage": self.damage
        }