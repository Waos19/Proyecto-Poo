import socket
import threading
import json
import random
import time
import math
import Settings

class Server:
    def __init__(self, host='26.128.187.2', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.clients = []
        self.player_data = []
        self.bullets = []
        self.pickups = []
        self.running = True
        self.id_counter = 0
        self.weapon_types = ["LaserGun", "MachineGun", "RocketLauncher"]
        self.spawn_interval = 3000  # Tiempo en milisegundos
        self.last_spawn_time = time.time()

    def start(self):
        self.server.listen()
        print("Servidor iniciado y esperando conexiones...")
        while self.running:
            client, addr = self.server.accept()
            print(f"Conectado a {addr}")
            player_id = self.id_counter
            self.id_counter += 1
            client.send(json.dumps({"id": player_id}).encode('utf-8'))
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client, player_id)).start()

    def update_pickups(self):
        # Crear nuevos pickups periódicamente
        if time.time() - self.last_spawn_time > self.spawn_interval / 1000:
            if len(self.pickups) < 1000:
                pos = (random.randint(0, Settings.world_width), random.randint(0, Settings.world_height))
                weapon_type = random.choice(self.weapon_types)
                pickup = {
                    "weapon_type": weapon_type,
                    "x": pos[0],
                    "y": pos[1],
                    "active": True
                }
                self.pickups.append(pickup)
                self.last_spawn_time = time.time()

    def handle_client(self, client, player_id):
        self.player_data.append({
            "id": player_id,
            "x": 0,
            "y": 0,
            "angle": 0,
            "health": 100,
            "ammo": 20,
            "ship_type": "Fighter",
            "is_alive": True
        })
        
        buffer = ""
        while self.running:
            try:
                data = client.recv(4096).decode('utf-8')
                if not data:
                    break

                buffer += data
                
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    try:
                        received_data = json.loads(message)
                        
                        if "pickup_collected" in received_data:
                            weapon_type = received_data["pickup_collected"]
                            pickup_position = received_data["pickup_position"]
                            for pickup in self.pickups:
                                if pickup["active"] and (pickup["x"], pickup["y"]) == pickup_position:
                                    pickup["active"] = False
                                    print(f"Pickup {weapon_type} recogido por el jugador {player_id}")
                                    break

                        # Actualizar datos del jugador directamente
                        for i, player in enumerate(self.player_data):
                            if player["id"] == player_id:
                                # Actualizar todos los campos del jugador
                                self.player_data[i] = {
                                    **player,  # Mantener datos existentes
                                    "x": received_data.get("x", player["x"]),
                                    "y": received_data.get("y", player["y"]),
                                    "angle": received_data.get("angle", player["angle"]),
                                    "health": received_data.get("health", player["health"]),
                                    "ammo": received_data.get("ammo", player["ammo"]),
                                    "ship_type": received_data.get("ship_type", player["ship_type"]),
                                    "is_alive": received_data.get("is_alive", player["is_alive"])
                                }
                                if self.player_data[i]["health"] <= 0:
                                    self.player_data[i]["is_alive"] = False
                                    self.player_data[i]["health"] = 0
                                break

                        if "shot_fired" in received_data and received_data["shot_fired"]:
                            new_bullet = {
                                "x": received_data["x"],
                                "y": received_data["y"],
                                "angle": received_data["angle"],
                                "shooter_id": player_id,
                                "creation_time": time.time(),
                                "speed": 15,
                                "damage": 25,
                                "active": True
                            }
                            self.bullets.append(new_bullet)

                    except json.JSONDecodeError as e:
                        print(f"Error decodificando JSON: {e}")
                        continue

                self.update_bullets()
                self.update_pickups()
                self.handle_pickup_collision()

                game_state = {
                    "players": self.player_data,
                    "bullets": self.bullets,
                    "pickups": self.pickups
                }
                self.broadcast(game_state)

            except Exception as e:
                print(f"Error handling client: {e}")
                break

        self.player_data = [p for p in self.player_data if p["id"] != player_id]
        if client in self.clients:
            self.clients.remove(client)

    def update_bullets(self):
        current_time = time.time()
        updated_bullets = []

        for bullet in self.bullets:
            if current_time - bullet["creation_time"] > 2.0:
                continue

            bullet["x"] += math.cos(math.radians(bullet["angle"])) * bullet["speed"]
            bullet["y"] -= math.sin(math.radians(bullet["angle"])) * bullet["speed"]

            hit_detected = False
            for i, player in enumerate(self.player_data):
                if player["id"] != bullet["shooter_id"] and player["is_alive"]:
                    dx = player["x"] - bullet["x"]
                    dy = player["y"] - bullet["y"]
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance < 20:  # Radio de colisión
                        self.player_data[i]["health"] -= bullet["damage"]
                        if self.player_data[i]["health"] <= 0:
                            self.player_data[i]["is_alive"] = False
                            self.player_data[i]["health"] = 0
                        print(f"Jugador {player['id']} impactado. Salud: {self.player_data[i]['health']}")
                        hit_detected = True
                        break

            if not hit_detected:
                updated_bullets.append(bullet)

        self.bullets = updated_bullets

    def broadcast(self, data):
        message = json.dumps(data) + '\n'
        dead_clients = []
        
        for client in self.clients:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                dead_clients.append(client)
                print(f"Error al enviar datos a un cliente")
        
        for client in dead_clients:
            if client in self.clients:
                self.clients.remove(client)

    def handle_pickup_collision(self):
        for player in self.player_data:
            if player["is_alive"]:
                for pickup in self.pickups:
                    if pickup["active"]:
                        dx = player["x"] - pickup["x"]
                        dy = player["y"] - pickup["y"]
                        distance = math.sqrt(dx ** 2 + dy ** 2)

                        if distance < 40:
                            player["weapon_type"] = pickup["weapon_type"]
                            pickup["active"] = False
                            print(f"Player {player['id']} recogió {pickup['weapon_type']}")
                            break

if __name__ == "__main__":
    server = Server()
    server.start()