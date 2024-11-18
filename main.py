import pygame
import sys
import socket
import pickle
import threading
import Settings
from World import World
from Camera import Camera
from WeaponsPickupManager import WeaponPickupsManager
from Menus import *
from Fighter import Fighter
from Tank import Tank
from Scout import Scout

# Inicializar pygame
pygame.init()

# Establecer la ventana principal
Screen = pygame.display.set_mode((Settings.Width, Settings.Height))
pygame.display.set_caption("ShipShoot")

# Variables globales
Clock = pygame.time.Clock()
Font = pygame.font.Font(None, 36)  # Fuente para el texto



# Conexión al servidor
class Client:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
        # Recibir el ID único del servidor al conectarse
        data = self.client.recv(4096)
        initial_info = pickle.loads(data)
        self.id = initial_info["id"]
        print(f"Conectado al servidor con ID: {self.id}")
        
        # Información inicial del jugador local
        self.player_info = {
            "id": self.id,
            "x": Settings.Width // 2,
            "y": Settings.Height // 2,
            "angle": 0,
            "health": 100,
            "ammo": 10,
            "ship_type": "Fighter",
            "is_alive": True
        }
        self.players = []
        self.bullets = []
        self.pickups = []  # Lista para almacenar los pickups remotos

    def receive_data(self):
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    game_data = pickle.loads(data)
                    self.players = game_data["players"]
                    self.bullets = game_data["bullets"]
                    self.pickups = game_data["pickups"]  # Recibe los pickups
                else:
                    print("El servidor ha cerrado la conexión.")
                    break
            except Exception as e:
                print(f"Error al recibir datos: {e}")
                break
    def send_data(self):
        try:
            # Envía la información del jugador al servidor
            self.client.send(pickle.dumps(self.player_info))
        except Exception as e:
            print(f"Error al enviar datos: {e}")

# Función principal del juego
def Main():
    # Crear el mundo y la cámara
    world = World(1920, 1200)
    camera = Camera(world.width, world.height)

    # Ejecutar el menú de selección de nave y obtener el tipo de nave seleccionado
    ship_type = Menu()  # Ahora esta función devuelve un string con el tipo de nave seleccionado

    # Crear el jugador según el tipo de nave
    if ship_type == "Fighter":
        Player = Fighter(Settings.Width // 2, Settings.Height // 2)
    elif ship_type == "Tank":
        Player = Tank(Settings.Width // 2, Settings.Height // 2)
    elif ship_type == "Scout":
        Player = Scout(Settings.Width // 2, Settings.Height // 2)

    # Crear el cliente y conectar al servidor
    client = Client()

    # Iniciar el hilo para recibir datos del servidor
    threading.Thread(target=client.receive_data, daemon=True).start()

    # Bucle principal del juego
    while True:
        delta_time = Clock.tick(Settings.Fps)

        # Eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx -= Player.speed
        if keys[pygame.K_d]:
            dx += Player.speed
        if keys[pygame.K_w]:
            dy -= Player.speed
        if keys[pygame.K_s]:
            dy += Player.speed
        if keys[pygame.K_r]:
            Player.weapon.reload()

        # Acción con el ratón
        Mouse = pygame.mouse.get_pressed()
        shot_fired = False
        if Mouse[0]:  # Si el botón izquierdo del ratón está presionado
            angle = Player.lookAtMouse(camera)  # Calcula el ángulo para rotar hacia el mouse
            if Player.weapon.shoot(angle):  # Si el disparo fue exitoso
                shot_fired = True

        client.player_info = {
            "id": client.id,
            "x": Player.x,
            "y": Player.y,
            "angle": Player.angle,
            "health": Player.current_health,
            "ammo": Player.weapon.current_ammo,
            "ship_type": ship_type,
            "shot_fired": shot_fired,  # Añadir esta información
            "is_alive": Player.is_alive
        }
        
        # Actualizar estado del jugador desde el servidor
        for player_info in client.players:
            if player_info["id"] == client.id:
                if player_info["health"] != Player.current_health:
                    Player.take_damage(Player.current_health - player_info["health"])
    
        client.send_data()

        # Mover al jugador
        Player.movement(dx, dy)

        # Rotar el personaje hacia el ratón
        Player.lookAtMouse(camera)

        # Actualizar los métodos del jugador
        Player.update()
        camera.update(Player)

        # Dibujar en pantalla
        Screen.blit(world.background, camera.apply(world))
        Player.draw(Screen, camera)
        Player.draw_health(Screen)
        #Player.weapon.draw_bullets(Screen, camera)
        Player.weapon.DrawAmmo(Screen)

        # Dibujar a los demás jugadores remotos
        for player_info in client.players:
            if player_info["id"] != client.id:
                if player_info["ship_type"] == "Fighter":
                    remote_player = Fighter(player_info["x"], player_info["y"])
                elif player_info["ship_type"] == "Tank":
                    remote_player = Tank(player_info["x"], player_info["y"])
                elif player_info["ship_type"] == "Scout":
                    remote_player = Scout(player_info["x"], player_info["y"])

                remote_player.is_alive = player_info.get("is_alive", True)
                if remote_player.is_alive:
                    remote_player.angle = player_info["angle"]
                    remote_player.current_health = player_info["health"]
                    visual_angle = remote_player.angle - 90
                    remote_player.update_frame()
                    remote_player.image = pygame.transform.rotate(remote_player.scaled_image, visual_angle)
                    remote_player.rect = remote_player.image.get_rect(center=(remote_player.x, remote_player.y))
                    remote_player.draw(Screen, camera)

        # Dibujar balas remotas
        for bullet in client.bullets:
            bullet_x = bullet["x"]
            bullet_y = bullet["y"]
            bullet_surface = pygame.Surface((10, 20), pygame.SRCALPHA)
            bullet_surface.fill((255, 0, 0))  # Rojo para las balas
            rotated_bullet = pygame.transform.rotate(bullet_surface, -bullet["angle"])
            bullet_rect = rotated_bullet.get_rect(center=(bullet_x, bullet_y))
            screen_pos = camera.apply_pos((bullet_x, bullet_y))
            bullet_rect.center = screen_pos
            Screen.blit(rotated_bullet, bullet_rect)
            
        for pickup in client.pickups:
            if pickup["active"]:
                pickup_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
                pickup_surface.fill((0, 255, 0))  # Color verde para los pickups
                pickup_rect = pickup_surface.get_rect(center=(pickup["x"], pickup["y"]))
                Screen.blit(pickup_surface, pickup_rect)

        pygame.display.flip()
        Clock.tick(Settings.Fps)

if __name__ == "__main__":
    Main()
