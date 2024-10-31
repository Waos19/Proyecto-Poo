import pygame
import sys
import Settings
from World import World
from Camera import Camera
from Tank import Tank  # Asegúrate de importar tu clase Tank
from Scout import Scout  # Asegúrate de importar tu clase Scout
from Fighter import Fighter  # Asegúrate de importar tu clase Fighter

# Inicializar pygame
pygame.init()

# Configuración de la ventana principal
Screen = pygame.display.set_mode((Settings.Width, Settings.Heigth))
pygame.display.set_caption("Selección de nave")

# Variables globales
Clock = pygame.time.Clock()
Font = pygame.font.Font(None, 36)  # Fuente para texto

# Función para el menú de selección de naves
def ShipSelectionMenu():
    while True:
        Screen.fill((0, 0, 0))  # Fondo negro

        # Texto del menú
        title_text = Font.render("Selecciona tu nave:", True, (255, 255, 255))
        tank_text = Font.render("1 - Tank (Alta vida, baja velocidad)", True, (255, 0, 0))
        scout_text = Font.render("2 - Scout (Baja vida, alta velocidad)", True, (0, 255, 0))
        fighter_text = Font.render("3 - Fighter (Equilibrado)", True, (0, 0, 255))

        # Dibujar el texto en pantalla
        Screen.blit(title_text, (Settings.Width // 2 - title_text.get_width() // 2, 100))
        Screen.blit(tank_text, (Settings.Width // 2 - tank_text.get_width() // 2, 200))
        Screen.blit(scout_text, (Settings.Width // 2 - scout_text.get_width() // 2, 300))
        Screen.blit(fighter_text, (Settings.Width // 2 - fighter_text.get_width() // 2, 400))

        pygame.display.flip()

        # Eventos para seleccionar nave
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return Tank(Settings.Width // 2, Settings.Heigth // 2)
                elif event.key == pygame.K_2:
                    return Scout(Settings.Width // 2, Settings.Heigth // 2)
                elif event.key == pygame.K_3:
                    return Fighter(Settings.Width // 2, Settings.Heigth // 2)

# Función principal del juego
def Main():
    # Instancia el mundo y la cámara
    world = World(1920, 1200)
    camera = Camera(world.width, world.height)
    
    # Ejecuta el menú de selección de naves
    Player = ShipSelectionMenu()
    
    # Ciclo principal del juego
    while True:
        # Eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Variables de movimiento
        dx, dy = 0, 0
        
        # Inputs de movimiento
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx -= Player.speed  # Usa la velocidad del Player
        if keys[pygame.K_d]:
            dx += Player.speed
        if keys[pygame.K_w]:
            dy -= Player.speed
        if keys[pygame.K_s]:
            dy += Player.speed
        if keys[pygame.K_r]:  
            Player.Reload()  
        
        # Inputs de acciones
        Mouse = pygame.mouse.get_pressed()
        
        if Mouse[0]:
            angle = Player.LookAtMouse(camera)
            Player.Shoot(angle)
        
        # Mover al jugador
        Player.Movement(dx, dy)

        # Rotar el personaje hacia el mouse
        Player.LookAtMouse(camera)
        
        # Métodos update
        Player.Update()
        camera.update(Player)
        
        # Actualizar balas y colisiones
        for bullet in list(Player.bullets):
            bullet.update()
            if bullet.is_off_screen():
                Player.bullets.remove(bullet)
            else:
                for other_player in [Player]:  # Aquí puedes añadir más jugadores si los tienes
                    if other_player != bullet.shooter:
                        bullet.check_collision(other_player)
        
        # Métodos Draw
        Screen.blit(world.background, camera.apply(world))
        Player.Draw(Screen, camera)
        Player.DrawAmmo(Screen)
        Player.draw_health(Screen)

        # Actualizar la pantalla
        pygame.display.flip()
        Clock.tick(Settings.Fps)

if __name__ == "__main__":
    Main()
