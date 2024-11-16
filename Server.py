import socket
import threading
import pickle
import random
import time
import math

class Server:
    def __init__(self, host='26.128.187.2', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.clients = []
        self.player_data = []
        self.bullets = []  # Lista de balas activas
        self.running = True
        self.id_counter = 0
        self.previous_time = time.time()

    def start(self):
        self.server.listen()
        print("Servidor iniciado y esperando conexiones...")
        while self.running:
            client, addr = self.server.accept()
            print(f"Conectado a {addr}")
            player_id = self.id_counter
            self.id_counter += 1

            initial_info = {
                "id": player_id,
                "x": random.randint(100, 900),
                "y": random.randint(100, 600),
                "angle": 0,
                "health": 100,
                "ammo": 20,
                "ship_type": "Fighter"
            }
            client.send(pickle.dumps({"id": player_id}))
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client, player_id)).start()

    def handle_client(self, client, player_id):
        player_index = len(self.player_data)
        self.player_data.append({
            "id": player_id,
            "x": 0,
            "y": 0,
            "angle": 0,
            "health": 100,
            "ammo": 20,
            "ship_type": "Fighter"
        })
        
        while self.running:
            try:
                data = client.recv(4096)
                if not data:
                    break

                received_data = pickle.loads(data)
                
                # Actualizar datos del jugador
                self.player_data[player_index].update(received_data)
                
                # Si el jugador disparó, crear una nueva bala
                if "shot_fired" in received_data and received_data["shot_fired"]:
                    new_bullet = {
                        "x": received_data["x"],
                        "y": received_data["y"],
                        "angle": received_data["angle"],
                        "shooter_id": player_id,
                        "creation_time": time.time(),
                        "speed": 10,
                        "active": True
                    }
                    self.bullets.append(new_bullet)
                
                # Actualizar posiciones de balas
                self.update_bullets()
                
                # Enviar estado actualizado a todos los clientes
                game_state = {
                    "players": self.player_data,
                    "bullets": self.bullets,
                    "pickups": []  # Mantener la estructura existente
                }
                self.broadcast(game_state)
                
            except Exception as e:
                print(f"Error handling client: {e}")
                break

        self.clients.remove(client)
        del self.player_data[player_index]
        client.close()

    def update_bullets(self):
        current_time = time.time()
        updated_bullets = []
        
        for bullet in self.bullets:
            if current_time - bullet["creation_time"] > 3.0:  # 3 segundos de vida
                continue
                
            # Actualizar posición de la bala
            bullet["x"] += math.cos(math.radians(bullet["angle"])) * bullet["speed"]
            bullet["y"] -= math.sin(math.radians(bullet["angle"])) * bullet["speed"]
            
            # Verificar colisiones con jugadores
            for player in self.player_data:
                if player["id"] != bullet["shooter_id"]:
                    # Colisión simple basada en distancia
                    dx = player["x"] - bullet["x"]
                    dy = player["y"] - bullet["y"]
                    distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance < 30:  # Radio de colisión
                        player["health"] -= 10  # Daño de la bala
                        continue
            
            updated_bullets.append(bullet)
        
        self.bullets = updated_bullets

    def broadcast(self, data):
        dead_clients = []
        for client in self.clients:
            try:
                client.send(pickle.dumps(data))
            except:
                dead_clients.append(client)
        
        for client in dead_clients:
            self.clients.remove(client)

if __name__ == "__main__":
    server = Server()
    server.start()