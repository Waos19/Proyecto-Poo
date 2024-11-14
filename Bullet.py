# bullet.py
import pygame
import math
import Settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, shooter, damage, bullet_speed):
        super().__init__()
        self.original_image = pygame.Surface((10, 20))  # Crea un sprite de la bala
        self.original_image.fill((255, 255, 255))
        self.image = pygame.transform.rotate(self.original_image, -angle)  # Rotar la imagen de la bala
        self.rect = self.image.get_rect(center=pos)
        self.x, self.y = pos
        self.angle = angle
        self.speed = 5
        self.damage = damage  # Usar el daño recibido de la clase de arma
        self.shooter = shooter
        self.life_time = 3000  # Tiempo de vida de la bala (3 segundos)
        self.creation_time = pygame.time.get_ticks()
        self.bullet_speed = bullet_speed

    def update(self):
        # Actualizar la posición de la bala
        # Mover la bala en función de la velocidad proporcionada por el arma
        self.x += self.bullet_speed * math.cos(math.radians(self.angle))
        self.y -= self.bullet_speed * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)
        if pygame.time.get_ticks() - self.creation_time > self.life_time:
            self.kill()  # Elimina la bala

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def is_off_screen(self):
        return self.x < 0 or self.x > Settings.world_width or self.y < 0 or self.y > Settings.world_height

    def check_collision(self, player):
        # Verifica si la bala colisiona con el jugador
        if player != self.shooter and self.rect.colliderect(player.rect):
            player.take_damage(self.damage)  # Aplica daño
            self.kill()  # Elimina la bala
