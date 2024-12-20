import pygame
import Settings
import os
import math
from DefaultWeapon import Pistol
import random

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, player_id = None):
        super().__init__()
        self.x = x
        self.y = y
        self.id = player_id

        # Inicializar variables de animación
        self.frame = 0
        self.angle = 0  # Ángulo para la rotación
        self.image = None
        self.rect = None
        self.original_image = None
        self.scaled_image = None # Imagen escalada
        self.is_alive = True
        self.respawn_delay = 2000  # 2 segundos en milisegundos
        self.death_time = 0

        # Cargar la hoja de sprites (sprite sheet)
        self.sheet = pygame.image.load(os.path.join('assets', 'Sprites', 'Player', 'Nautolan Ship - Scout - Sprite.png')).convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 0, 64, 64))  # Tamaño de cada frame: 64x64

        # Estados de animación para cada dirección
        self.left_states = {0: (0, 0, 64, 64), 1: (64, 0, 64, 64), 2: (128, 0, 64, 64), 3: (192, 0, 64, 64)}
        self.right_states = {0: (0, 0, 64, 64), 1: (64, 0, 64, 64), 2: (128, 0, 64, 64), 3: (192, 0, 64, 64)}
        self.up_states = {0: (0, 0, 64, 64), 1: (64, 0, 64, 64), 2: (128, 0, 64, 64), 3: (192, 0, 64, 64)}
        self.down_states = {0: (0, 0, 64, 64), 1: (64, 0, 64, 64), 2: (128, 0, 64, 64), 3: (192, 0, 64, 64)}

        self.direction_states = self.down_states  # Estado inicial de animación

        # Inicializar el arma
        self.weapon = Pistol(self)

        # Salud
        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length

        # Establecer sprite inicial
        self.set_sprite(os.path.join('assets', 'Sprites', 'Player', 'Nautolan Ship - Scout - Sprite.png'))

    def set_sprite(self, image_path):
        """ Método para cambiar el sprite del personaje """
        self.sheet = pygame.image.load(image_path).convert_alpha()  # Cargar el nuevo sprite
        self.sheet.set_clip(pygame.Rect(0, 0, 64, 64))  # Tamaño de cada frame

        # Escalar la imagen según el valor global de escala
        self.original_image = self.sheet.subsurface(self.sheet.get_clip())
        self.scaled_image = pygame.transform.scale(self.original_image, (Settings.Player_scale, Settings.Player_scale))

        # Establecer la imagen escalada
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Actualizar el rectángulo

    def update_frame(self):
        # Actualizar el frame de animación
        self.frame = (self.frame + 1) % len(self.direction_states)
        self.sheet.set_clip(pygame.Rect(self.direction_states[self.frame]))

        # Obtener la imagen base sin rotar
        self.original_image = self.sheet.subsurface(self.sheet.get_clip())

        # Aplicar la escala solo una vez
        self.scaled_image = pygame.transform.scale(self.original_image, (Settings.Player_scale, Settings.Player_scale))

        # Aplicar la rotación sobre la imagen escalada
        self.image = pygame.transform.rotate(self.scaled_image, self.angle - 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.update_frame()
        self.weapon.update()  # Actualizar el arma también

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))  # Asumiendo que camera.apply() ajusta la posición

    def movement(self, dx, dy):
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        self.x += dx
        self.y += dy
        self.x = max(self.rect.width // 2, min(self.x, Settings.world_width - self.rect.width // 2))
        self.y = max(self.rect.height // 2, min(self.y, Settings.world_height - self.rect.height // 2))
        self.rect.center = (self.x, self.y)

        # Actualizar la dirección de animación según el movimiento
        if dx > 0:
            self.direction_states = self.right_states
        elif dx < 0:
            self.direction_states = self.left_states
        elif dy < 0:
            self.direction_states = self.up_states
        elif dy > 0:
            self.direction_states = self.down_states

    def lookAtMouse(self, camera):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calcular la posición mundial del mouse con el desplazamiento de la cámara
        mouse_x_world = mouse_x - camera.camera_rect.x
        mouse_y_world = mouse_y - camera.camera_rect.y

        # Calcular el vector de dirección del personaje al mouse
        dx = mouse_x_world - self.rect.centerx
        dy = mouse_y_world - self.rect.centery

        # Calcular el ángulo en radianes y convertirlo a grados
        self.angle = math.degrees(math.atan2(-dy, dx))

        # Actualizar el ángulo de rotación
        self.image = pygame.transform.rotate(self.scaled_image, self.angle - 90)

        # Mantener la posición del centro al rotar
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        return self.angle
    
    def get_gun_position(self):
        offset_distance = 32
        gun_x = self.rect.centerx + math.cos(math.radians(self.angle)) * offset_distance
        gun_y = self.rect.centery - math.sin(math.radians(self.angle)) * offset_distance
        return gun_x, gun_y

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)
        if self.current_health <= 0 and self.is_alive:
            self.die()
    
    def die(self):
        self.is_alive = False
        self.death_time = pygame.time.get_ticks()
        self.respawn()
        
    def respawn(self):
        # Generar posición aleatoria dentro del mundo
        self.x = random.randint(100, Settings.world_width - 100)
        self.y = random.randint(100, Settings.world_height - 100)
        self.current_health = self.max_health
        self.is_alive = True
        self.rect.center = (self.x, self.y)
        