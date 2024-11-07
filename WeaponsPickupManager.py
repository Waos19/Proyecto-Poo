# weapon_pickups_manager.py
import pygame
import random
from WeaponPickup import WeaponPickup
from LaserGun import LaserGun
from Machinegun import MachineGun
from RocketLauncher import RocketLauncher
import Settings

class WeaponPickupsManager:
    def __init__(self, weapon_types, spawn_interval=5000, max_pickups=5):
        self.weapon_types = weapon_types
        self.pickups = pygame.sprite.Group()
        self.spawn_timer = 0  # Temporizador para la generación de pickups
        self.spawn_interval = spawn_interval  # Intervalo en milisegundos entre cada generación
        self.max_pickups = max_pickups  # Número máximo de pickups en el mapa

    def generate_pickup(self):
        # Generar un pickup en una posición aleatoria
        if len(self.pickups) < self.max_pickups:  # Limitar la cantidad de pickups en el mapa
            pos = (random.randint(0, Settings.world_width), random.randint(0, Settings.world_height))
            weapon_type = random.choice(self.weapon_types)
            pickup = WeaponPickup(weapon_type, pos)
            self.pickups.add(pickup)

    def update(self, delta_time):
        # Actualizar el temporizador y generar pickup si es necesario
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.generate_pickup()
            self.spawn_timer = 0  # Reiniciar el temporizador

        # Actualizar cada pickup en el grupo
        self.pickups.update()

    def draw(self, screen, camera):
        # Dibujar todos los pickups en el mapa
        for pickup in self.pickups:
            screen.blit(pickup.image, camera.apply(pickup))
    
    def handle_collision(self, player):
        # Verificar si el jugador recoge un arma
        collided_pickup = pygame.sprite.spritecollideany(player, self.pickups)
        if collided_pickup:
            # Cambiar el arma del jugador según el tipo de pickup
            if collided_pickup.weapon_type == "LaserGun":
                player.weapon = LaserGun(player)
            elif collided_pickup.weapon_type == "MachineGun":
                player.weapon = MachineGun(player)
            elif collided_pickup.weapon_type == "RocketLauncher":
                player.weapon = RocketLauncher(player)
            
            collided_pickup.kill()  # Eliminar el pickup del grupo tras recogerlo

