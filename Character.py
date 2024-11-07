import pygame
import Settings
import os
import math
from DefaultWeapon import Pistol

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        image_path = os.path.join('assets', 'Sprites', 'Player', 'Main Ship - Base - Full health.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (Settings.tamaño_personaje, Settings.tamaño_personaje))
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.rect.width // 2  # Radio para colisiones
        self.collision_rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        
        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length
        
        self.angle = 0  # Almacena el ángulo actual del personaje

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            print("Game Over")
    
    def draw_health(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (10, 40, self.health_bar_length, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 40, self.current_health / self.health_ratio, 20))

    def update(self):
        self.weapon.update()  # Actualizar el arma también

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        self.draw_health(screen)
    
    def DrawAmmo(self, screen):
        ammo_text = self.font.render(f'Munición: {self.current_ammo}/{self.max_ammo}', True, (255, 255, 255))
        screen.blit(ammo_text, (10, 10))  

        if self.reloading:
            current_time = pygame.time.get_ticks()
            reload_progress = (current_time - self.last_reload_time) / self.reload_time
            reload_bar_length = 200  
            bar_color = (0, 255, 0)  

            pygame.draw.rect(screen, bar_color, (10, 50, reload_bar_length * reload_progress, 20))
    
    def Movement(self, dx, dy):
        if dx != 0 and dy != 0:
            dx *= 0.7071  # Normalización de movimiento diagonal
        
        self.x += dx
        self.y += dy
        self.x = max(self.rect.width // 2, min(self.x, Settings.world_width - self.rect.width // 2))
        self.y = max(self.rect.height // 2, min(self.y, Settings.world_height - self.rect.height // 2))
        self.rect.center = (self.x, self.y)
        self.collision_rect.center = (self.x, self.y)

    def lookAtMouse(self, camera):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_world = mouse_x - camera.camera_rect.x
        mouse_y_world = mouse_y - camera.camera_rect.y

        dx = mouse_x_world - self.x
        dy = mouse_y_world - self.y
        angle = math.degrees(math.atan2(-dy, dx))  # Almacena el ángulo actual

        visual_angle = angle - 90  # Ajusta el ángulo visual
        
        scaled_image = pygame.transform.scale(self.original_image, (Settings.tamaño_personaje, Settings.tamaño_personaje))
        self.image = pygame.transform.rotate(scaled_image, visual_angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collision_rect.center = (self.x, self.y)

        return angle  # Devuelve el ángulo actual