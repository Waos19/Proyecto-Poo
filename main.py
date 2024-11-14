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

# Tipos de armas
weapon_types = ["LaserGun", "MachineGun", "RocketLauncher"]
weapon_pickups_manager = WeaponPickupsManager(weapon_types, spawn_interval=5000, max_pickups=5)

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
            "angle": 0,  # Inicializamos el ángulo
            "health": 100,
            "ammo": 10,
            "ship_type": "Fighter"  # Valor por defecto
        }
        self.players = []  # Lista para almacenar la información de los jugadores remotos

    def send_data(self):
        try:
            data = pickle.dumps(self.player_info)
            self.client.send(data)
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"Error al enviar datos: {e}")
            self.client.close()

    def receive_data(self):
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    self.players = pickle.loads(data)
                else:
                    print("El servidor ha cerrado la conexión.")
                    break
            except Exception as e:
                print(f"Error al recibir datos: {e}")
                break

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
        if Mouse[0]:  # Si el botón izquierdo del ratón está presionado
            angle = Player.lookAtMouse(camera)  # Calcula el ángulo para rotar hacia el mouse
            Player.weapon.shoot(angle)  # Dispara según la dirección calculada

        # Mover al jugador
        Player.movement(dx, dy)

        # Rotar el personaje hacia el ratón
        Player.lookAtMouse(camera)

        # Actualizar los métodos del jugador
        Player.update()
        camera.update(Player)
        weapon_pickups_manager.update(delta_time)
        weapon_pickups_manager.handle_collision(Player)

        # Actualizar información del jugador local
        client.player_info = {
            "id": client.id,
            "x": Player.x,
            "y": Player.y,
            "angle": Player.angle,  # Enviar el ángulo calculado
            "health": Player.current_health,
            "ammo": Player.weapon.current_ammo,
            "ship_type": ship_type  # Enviar el tipo de nave seleccionado
        }
        client.send_data()  # Enviar la información actualizada al servidor

        # Dibujar en pantalla
        Screen.blit(world.background, camera.apply(world))
        Player.draw(Screen, camera)  # Dibuja el jugador local
        Player.draw_health(Screen)  # Dibuja la barra de salud
        Player.weapon.draw_bullets(Screen, camera)  # Dibuja las balas disparadas
        Player.weapon.DrawAmmo(Screen)  # Dibuja la cantidad de munición restante
        weapon_pickups_manager.draw(Screen, camera)  # Dibuja los pickups de armas

        # Dibujar a los demás jugadores remotos
        for player_info in client.players:
            if player_info["id"] != client.id:  # Ignorar al jugador local basado en el ID único
                # Crear un objeto Character temporal para el jugador remoto
                if player_info["ship_type"] == "Fighter":
                    remote_player = Fighter(player_info["x"], player_info["y"])
                elif player_info["ship_type"] == "Tank":
                    remote_player = Tank(player_info["x"], player_info["y"])
                elif player_info["ship_type"] == "Scout":
                    remote_player = Scout(player_info["x"], player_info["y"])

                # Actualizar el ángulo del jugador remoto
                remote_player.angle = player_info["angle"]  # Usar el ángulo recibido del servidor

                # Rotar la imagen del jugador remoto según el ángulo
                visual_angle = remote_player.angle - 90
                remote_player.image = pygame.transform.rotate(remote_player.scaled_image, visual_angle)
                remote_player.rect = remote_player.image.get_rect(center=(remote_player.x, remote_player.y))

                # Dibujar el jugador remoto
                remote_player.draw(Screen, camera)

        pygame.display.flip()
        Clock.tick(Settings.Fps)

if __name__ == "__main__":
    Main()
