import socket
import threading
import pickle

class Server:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.clients = []
        self.player_data = []  
        self.running = True
        self.id_counter = 0  # Contador para asignar IDs únicos

    def start(self):
        self.server.listen()
        print("Servidor iniciado y esperando conexiones...")
        while self.running:
            client, addr = self.server.accept()
            print(f"Conectado a {addr}")
            player_id = self.id_counter  # Asigna el ID único actual
            self.id_counter += 1  # Incrementa el contador para el próximo jugador
            
            # Aquí se puede enviar el tipo de nave por defecto o personalizado
            player_info = {
                "id": player_id,
                "x": 0,
                "y": 0,
                "angle": 0,  # El ángulo inicial
                "health": 100,
                "ammo": 20,
                "ship_type": "Fighter"  # Aquí se envía el tipo de nave
            }
            client.send(pickle.dumps(player_info))
            
            # Añadir cliente a la lista y empezar a manejarlo en un hilo
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client, player_id)).start()

    def handle_client(self, client, player_id):
        player_index = len(self.player_data)
        self.player_data.append({
            "id": player_id,
            "x": 0,
            "y": 0,
            "angle": 0,  # Inicializamos el ángulo
            "health": 100,
            "ammo": 20,
            "ship_type": "Fighter"  # Asignamos tipo de nave por defecto
        })
        
        while self.running:
            try:
                data = client.recv(4096)
                if not data:
                    break

                player_info = pickle.loads(data)
                player_info["id"] = player_id  # Añade el ID a los datos recibidos
                
                # Actualiza los datos del jugador en la lista
                self.player_data[player_index] = player_info
                
                # Envía los datos actualizados a todos los clientes
                self.broadcast()
            except Exception as e:
                print(f"Error al manejar el cliente: {e}")
                break

        # Cuando el cliente se desconecta
        self.clients.remove(client)
        del self.player_data[player_index]
        client.close()

    def broadcast(self):
        # Envía toda la data de los jugadores a cada cliente
        data = pickle.dumps(self.player_data)
        for client in self.clients:
            try:
                client.send(data)
            except Exception as e:
                print(f"Error al enviar datos a un cliente: {e}")

if __name__ == "__main__":
    server = Server()
    server.start()
