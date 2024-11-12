import pygame
import sys
from Button import Buttons  
from Button import CircularButton
from volumen_bar import VolumeBar
import Settings
from World import World
from Character import Character
from Camera import Camera
from main import Main
from Tank import Tank  
from Scout import Scout  
from Fighter import Fighter
from WeaponsPickupManager import WeaponPickupsManager

Clock = pygame.time.Clock()

def Menu():
    # Inicializar Pygame
    pygame.init()

    #Cargar fondo 
    background_load = pygame.image.load("Imagenes/background/background.png")
    background = pygame.transform.scale(background_load,(800,600))

    background_load_2 = pygame.image.load("Imagenes/background/background_4.jpg")
    background_2 = pygame.transform.scale(background_load_2,(800,600))

    background_load_3 = pygame.image.load("Imagenes/background/background_3.jpg")
    background_3 = pygame.transform.scale(background_load_3,(800,600))
    # Cargar sonidos ocasionales
    load_clic_button = "Sonido/sonidos_ocasionales/clic_boton.wav"
    clic_boton = pygame.mixer.Sound(load_clic_button)

    #Cargar musica 
    pygame.mixer.music.load("Sonido/musica_fondo/supernova.mp3")
    pygame.mixer.music.set_volume(0.5)
    #pygame.mixer.music.play(-1)

    #Crear barra de volumen 
    volume_bar = VolumeBar(250, 280, 300, 20)

    # Configuración de la pantalla
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Prueba menu")

    #Bool para button back
    salir_menu_principal = False

    #Bool para eleccion de jugador 
    select_ship_1 = False
    select_ship_2 = False
    select_ship_3 = False

    #Bool para musica
    muted= False 

    #Medidas para botones y carteles de personajes
    button_width = 220
    button_height = 50
    sign_witdh = 150
    sign_height = 400

    # Crear instancias de botones con imágenes
    button_start = Buttons("Imagenes/buttons/boton_start.png","Imagenes/buttons/boton_start_presionado.png",300, 270, button_width, button_height)
    button_opcion = Buttons("Imagenes/buttons/boton_opcion.png","Imagenes/buttons/boton_opcion_presionado.png", 300, 330, button_width, button_height)
    button_salir = Buttons("Imagenes/buttons/boton_salir.png", "Imagenes/buttons/boton_salir_presionado.png",300,390, button_width, button_height)
    button_credits = Buttons("Imagenes/buttons/button_credits.png", "Imagenes/buttons/button_credits_pressed.png",300,330,button_width, button_height)
    button_play = Buttons("Imagenes/buttons/button_play.png", "Imagenes/buttons/button_play_pressed.png",330,500,button_width, button_height)

    ship_1 = Buttons("Imagenes/tipo_naves/Nave1.png", "Imagenes/tipo_naves/Nave1.png", 120, 60,sign_witdh,sign_height)
    ship_2 = Buttons("Imagenes/tipo_naves/Nave2.png", "Imagenes/tipo_naves/Nave2.png", 360, 60,sign_witdh,sign_height)
    ship_3 = Buttons("Imagenes/tipo_naves/Nave3_pressed.png", "Imagenes/tipo_naves/Nave3_pressed.png", 600, 60,sign_witdh,sign_height)

    # Crear botones circulares 
    button_back = CircularButton("Imagenes/buttons/button_back.png", "Imagenes/buttons/button_back.png", 40, 40, 40)
    button_mute = CircularButton("Imagenes/buttons/boton_q_silencio.png", "Imagenes/buttons/boton_q_silencio.png", 400, 240, 40)
    button_unmute = CircularButton("Imagenes/buttons/boton_silencio.png", "Imagenes/buttons/boton_silencio.png", 400, 240, 40)

    weapon_types = ["LaserGun", "MachineGun", "RocketLauncher"]
    weapon_pickups_manager = WeaponPickupsManager(weapon_types, spawn_interval=5000, max_pickups=5)
    # Bucle principal
    while True:
        posicion_mouse = pygame.mouse.get_pos()
        salir_menu_principal = False 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos           
                if button_start.is_clicked(mouse_pos):
                    clic_boton.play()
                    #Empezar bucle para cargar la pantalla de crear servidor
                    while True:
                        posicion_mouse = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if button_back.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    salir_menu_principal = True
                                if ship_1.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    select_ship_1 = True
                                    select_ship_2 = False
                                    select_ship_3 = False
                                if ship_2.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    select_ship_1 = False
                                    select_ship_2 = True
                                    select_ship_3 = False
                                if ship_3.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    select_ship_1 = False
                                    select_ship_2 = False
                                    select_ship_3 = True
                                if button_play.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    world = World(1920, 1200)
                                    camera = Camera(world.width, world.height)
                                    if select_ship_1:
                                        Player = Scout(Settings.Width // 2, Settings.Height // 2)
                                    if select_ship_2:
                                        Player = Tank(Settings.Width // 2, Settings.Height // 2)
                                    if select_ship_3:
                                        Player = Fighter(Settings.Width // 2, Settings.Height // 2)
                                    while True:
                                        
                                        delta_time = Clock.tick(Settings.Fps)
                                        
                                        # Game events
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                        
                                        # Movement variables
                                        dx, dy = 0, 0
                                        
                                        # Movement inputs
                                        keys = pygame.key.get_pressed()
                                        if keys[pygame.K_a]:
                                            dx -= Player.speed  # Use the player's speed
                                        if keys[pygame.K_d]:
                                            dx += Player.speed
                                        if keys[pygame.K_w]:
                                            dy -= Player.speed
                                        if keys[pygame.K_s]:
                                            dy += Player.speed
                                        if keys[pygame.K_r]:  
                                            Player.weapon.reload()  
                                        
                                        # Action inputs
                                        Mouse = pygame.mouse.get_pressed()
                                        
                                        if Mouse[0]:  # If the left mouse button is pressed
                                            angle = Player.lookAtMouse(camera)
                                            Player.weapon.shoot(angle)
                                        
                                        # Move the player
                                        Player.movement(dx, dy)

                                        # Rotate the character towards the mouse
                                        Player.lookAtMouse(camera)
                                        
                                        # Update methods
                                        Player.update()
                                        camera.update(Player)
                                        weapon_pickups_manager.update(delta_time)
                                        weapon_pickups_manager.handle_collision(Player)
                                        
                                        # Draw methods
                                        screen.blit(world.background, camera.apply(world))
                                        Player.draw(screen, camera)
                                        Player.draw_health(screen)
                                        Player.weapon.draw_bullets(screen, camera)
                                        Player.weapon.DrawAmmo(screen)
                                        weapon_pickups_manager.draw(screen, camera)
                                        

                                        # Update the screen
                                        pygame.display.flip()
                                        Clock.tick(Settings.Fps)
                        if salir_menu_principal:
                            select_ship_1 = False
                            select_ship_2 = False
                            select_ship_3 = False
                            break
                        # Dibujar el fondo y los botones
                        screen.blit(background_3, (0, 0))
                        button_back.draw(screen, posicion_mouse)
                        ship_1.draw(screen, posicion_mouse)
                        ship_2.draw(screen, posicion_mouse)
                        ship_3.draw(screen, posicion_mouse)
                        if select_ship_1 == True or select_ship_2 == True or select_ship_3 == True:
                            button_play.draw(screen, posicion_mouse)
                        pygame.display.flip()    
                if button_opcion.is_clicked(mouse_pos):
                    clic_boton.play()
                    while True:
                        posicion_mouse = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if volume_bar.is_clicked(mouse_pos):
                                    volume_bar.handle_click(mouse_pos)
                                if button_credits.is_clicked(mouse_pos):
                                    clic_boton.play()   
                                if button_back.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    salir_menu_principal = True
                                if muted == False:
                                    if button_mute.is_clicked(mouse_pos):
                                        muted = True
                                        pygame.mixer.music.pause()
                                else:
                                    if button_unmute.is_clicked(mouse_pos):
                                        muted = False
                                        pygame.mixer.music.unpause()
                        if salir_menu_principal:
                            break
                        screen.blit(background_2, (0, 0))
                        button_credits.draw(screen,posicion_mouse)
                        button_back.draw(screen, posicion_mouse)
                        volume_bar.draw(screen)
                        if muted:
                            button_unmute.draw(screen, posicion_mouse)
                        else:
                            button_mute.draw(screen, posicion_mouse)
                        pygame.display.flip()
                if button_salir.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
        # Dibujar el fondo y los botones
        screen.blit(background, (0, 0))
        button_start.draw(screen,posicion_mouse)
        button_opcion.draw(screen,posicion_mouse)
        button_salir.draw(screen, posicion_mouse)
        # Actualizar la pantalla
        pygame.display.flip()

Menu()