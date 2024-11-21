import pygame
import sys
import socket
import json  
import threading
import Settings
from World import World
from Camera import Camera
from WeaponsPickupManager import WeaponPickupsManager
from Menus import *
from Fighter import Fighter
from Tank import Tank
from Scout import Scout
from HealthDisplay import HealthDisplay

# Inicializar pygame
pygame.init()

# Establecer la ventana principal
Screen = pygame.display.set_mode((Settings.Width, Settings.Height))
pygame.display.set_caption("ShipShoot")

# Variables globales
Clock = pygame.time.Clock()
Font = pygame.font.Font(None, 36)  # Fuente para el texto


# Clase para manejar la conexión al servidor
class Client:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.buffer = ""  # Buffer para manejar mensajes fragmentados
        self.health_display = HealthDisplay()
        # Recibir el ID único del servidor
        data = self.client.recv(4096)
        initial_info = json.loads(data.decode('utf-8'))
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
        self.pickups = []

    def receive_data(self):
        while True:
            try:
                # Recibir datos y acumularlos en el buffer
                data = self.client.recv(4096).decode('utf-8')
                if data:
                    self.buffer += data
                    # Procesar mensajes completos en el buffer
                    while '\n' in self.buffer:
                        message, self.buffer = self.buffer.split('\n', 1)
                        try:
                            game_data = json.loads(message)
                            self.players = game_data["players"]
                            self.bullets = game_data["bullets"]
                            self.pickups = game_data["pickups"]
                        except json.JSONDecodeError as e:
                            print(f"Error al procesar mensaje JSON: {e}")
                else:
                    print("El servidor ha cerrado la conexión.")
                    break
            except Exception as e:
                print(f"Error al recibir datos: {e}")
                break

    def send_data(self):
        try:
            # Serializar y enviar datos del jugador
            json_data = json.dumps(self.player_info).encode('utf-8') + b'\n'
            self.client.send(json_data)
        except Exception as e:
            print(f"Error al enviar datos: {e}")

    def check_pickup_collisions(self):
        for pickup in self.pickups:
            if pickup["active"]:
                pickup_rect = pygame.Rect(pickup["x"], pickup["y"], 32, 32)
                player_rect = pygame.Rect(self.player_info["x"], self.player_info["y"], 32, 32)
                if player_rect.colliderect(pickup_rect):
                    # Enviar datos de la colisión al servidor
                    collision_data = {
                        "pickup_collected": pickup["weapon_type"],
                        "pickup_position": (pickup["x"], pickup["y"])
                    }
                    try:
                        self.client.send(json.dumps(collision_data).encode('utf-8') + b'\n')
                    except Exception as e:
                        print(f"Error al enviar datos de colisión: {e}")
                    pickup["active"] = False


# Función principal del juego
def Main():
    # Crear el mundo y la cámara
    world = World(1920, 1200)
    camera = Camera(world.width, world.height)

    # Ejecutar el menú de selección de nave
    ship_type = Menu()

    # Crear el jugador según el tipo de nave
    if ship_type == "Fighter":
        Player = Fighter(Settings.Width // 2, Settings.Height // 2)
    elif ship_type == "Tank":
        Player = Tank(Settings.Width // 2, Settings.Height // 2)
    elif ship_type == "Scout":
        Player = Scout(Settings.Width // 2, Settings.Height // 2)

    # Crear el cliente
    client = Client()

    # Iniciar el hilo para recibir datos
    threading.Thread(target=client.receive_data, daemon=True).start()
    
    health_display = HealthDisplay()

    # Bucle principal
    while True:

        # Eventos
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
            
        camera.update(Player)

        # Acción con el ratón
        Mouse = pygame.mouse.get_pressed()
        shot_fired = False
        if Mouse[0]:
            angle = Player.lookAtMouse(camera)
            if Player.weapon.shoot(angle):
                shot_fired = True
                
        # Actualizar la información del jugador y verificar daño
        for player_info in client.players:
            if player_info["id"] == client.id:
                health_display.draw_health(Screen, player_info["health"], 
                                        camera.apply_pos((Player.x, Player.y))[0],
                                        camera.apply_pos((Player.x, Player.y))[1])
                Player.current_health = player_info["health"]
                Player.is_alive = player_info["is_alive"]
                if not Player.is_alive:
                    Player.die()

        # Actualizar la información del jugador
        client.player_info = {
            "id": client.id,
            "x": Player.x,
            "y": Player.y,
            "angle": Player.angle,
            "health": Player.current_health,
            "ammo": Player.weapon.current_ammo,
            "ship_type": ship_type,
            "shot_fired": shot_fired,
            "is_alive": Player.is_alive
        }
        

                    
        client.send_data()

        # Mover y rotar el jugador
        Player.movement(dx, dy)
        Player.lookAtMouse(camera)
        Player.update()

        # Dibujar fondo, jugador y otros elementos
        Screen.blit(world.background, camera.apply(world))
        Player.draw(Screen, camera)
        Player.weapon.DrawAmmo(Screen)
        
        
        # Dibujar la salud del jugador local
        client.health_display.draw_health(
            Screen, 
            Player.current_health,
            camera.apply_pos((Player.x, Player.y))[0],
            camera.apply_pos((Player.x, Player.y))[1],
            ship_type
        )

        # Dibujar jugadores remotos
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
                    visual_angle = remote_player.angle - 90
                    remote_player.update_frame()
                    remote_player.image = pygame.transform.rotate(remote_player.scaled_image, visual_angle)
                    remote_player.rect = remote_player.image.get_rect(center=(remote_player.x, remote_player.y))
                    remote_player.draw(Screen, camera)
                    
                    # Dibujar la salud del jugador remoto con su tipo específico
                    client.health_display.draw_health(
                        Screen,
                        player_info["health"],
                        camera.apply_pos((remote_player.x, remote_player.y))[0],
                        camera.apply_pos((remote_player.x, remote_player.y))[1],
                        player_info["ship_type"]
                    )
        # Dibujar balas
        for bullet in client.bullets:
            pygame.draw.circle(
                Screen, 
                bullet["color"],  # Usar el color específico del tipo de bala
                camera.apply_pos((bullet["x"], bullet["y"])), 
                bullet["size"]    # Usar el tamaño específico del tipo de bala
            )

        # Dibujar pickups y verificar colisiones
        for pickup in client.pickups:
            if pickup["active"]:
                weapon_type = pickup["weapon_type"]
                pickup_image = None

                # Asignar la imagen correspondiente según el tipo de arma
                if weapon_type == "LaserGun":
                    pickup_image = pygame.image.load("assets/Sprites/Boosters/2.png").convert_alpha()
                elif weapon_type == "MachineGun":
                    pickup_image = pygame.image.load("assets/Sprites/Boosters/0.png").convert_alpha()
                elif weapon_type == "RocketLauncher":
                    pickup_image = pygame.image.load("assets/Sprites/Boosters/1.png").convert_alpha()

                if pickup_image:
                    # Obtener posición ajustada por la cámara
                    pickup_pos = camera.apply_pos((pickup["x"], pickup["y"]))
                    pickup_rect = pickup_image.get_rect(center=pickup_pos)
                    Screen.blit(pickup_image, pickup_rect)
        # Verificar colisiones con pickups
        client.check_pickup_collisions()

        pygame.display.flip()
        Clock.tick(Settings.Fps)


if __name__ == "__main__":
    Main()
