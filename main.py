import pygame
import sys
import Settings
from World import World
from Character import Character
from Camera import Camera

# Iniciando pygame
pygame.init()

# Ventana principal
Screen = pygame.display.set_mode((Settings.Width, Settings.Heigth))
pygame.display.set_caption("Primeros pasos")

# Variables
Clock = pygame.time.Clock()

# Función main
def Main():
    # Instanciando objetos
    world = World(1920,1200)
    Player = Character(Settings.Width // 2, Settings.Heigth // 2)
    camera = Camera(world.width, world.height)
    
    # Ciclo principal
    while True:
        # Ciclo que busca eventos y contiene un condicional si el juego es cerrado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Variables de movimiento
        dx = 0
        dy = 0
        
        # Inputs de movimiento
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx -= 5
        if keys[pygame.K_d]:
            dx += 5
        if keys[pygame.K_w]:
            dy -= 5
        if keys[pygame.K_s]:
            dy += 5
        if keys[pygame.K_r]:  
            Player.Reload()  
        
        # Inputs de acciones
        Mouse = pygame.mouse.get_pressed()
        
        if Mouse[0]:
            angle = Player.LookAtMouse(camera)
            Player.Shoot(angle)
        
        # Mover al jugador
        Player.Movement(dx, dy)

        # Hacer que el personaje mire al mouse
        Player.LookAtMouse(camera)
        
        # Metodos update
        Player.Update()
        camera.update(Player)
        
        # Actualizar y comprobar colisiones de las balas
        for bullet in list(Player.bullets):
            bullet.update()
            if bullet.is_off_screen():
                Player.bullets.remove(bullet)
            else:
                for other_player in [Player]:  # Aquí puedes añadir más jugadores si los tienes
                    if other_player != bullet.shooter:
                        bullet.check_collision(other_player)
        
        # Metodos Draw
        Screen.blit(world.background, camera.apply(world))
        Player.Draw(Screen, camera)
        Player.DrawAmmo(Screen)
        Player.draw_health(Screen)

        # Actualizar la pantalla
        pygame.display.flip()
        Clock.tick(Settings.Fps)

if __name__ == "__main__":
    Main()