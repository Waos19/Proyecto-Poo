import pygame
import sys
from Button import Buttons  
from Button import CircularButton
from volumen_bar import VolumeBar
import Settings
from World import World
from Character import Character
from Camera import Camera
from Tank import Tank  
from Scout import Scout  
from Fighter import Fighter
from WeaponsPickupManager import WeaponPickupsManager

Clock = pygame.time.Clock()

# Inicializar Pygame
pygame.mixer.init()

# Cargar fondos
def cargar_fondos():
    background_load = pygame.image.load("Imagenes/background/background.png")
    background = pygame.transform.scale(background_load, (800, 600))

    background_load_2 = pygame.image.load("Imagenes/background/background_4.jpg")
    background_2 = pygame.transform.scale(background_load_2, (800, 600))

    background_load_3 = pygame.image.load("Imagenes/background/background_3.jpg")
    background_3 = pygame.transform.scale(background_load_3, (800, 600))

    return background, background_2, background_3

# Configurar la música
def configurar_musica():
    load_clic_button = "Sonido/sonidos_ocasionales/clic_boton.wav"
    clic_boton = pygame.mixer.Sound(load_clic_button)
    pygame.mixer.music.load("Sonido/musica_fondo/supernova.mp3")
    pygame.mixer.music.set_volume(0.5)
    #pygame.mixer.music.play(-1)
    return clic_boton

# Crear los botones
def crear_botones():
    button_width = 220
    button_height = 50
    sign_witdh = 150
    sign_height = 400

    button_start = Buttons("Imagenes/buttons/boton_start.png", "Imagenes/buttons/boton_start_presionado.png", 300, 270, button_width, button_height)
    button_opcion = Buttons("Imagenes/buttons/boton_opcion.png", "Imagenes/buttons/boton_opcion_presionado.png", 300, 330, button_width, button_height)
    button_salir = Buttons("Imagenes/buttons/boton_salir.png", "Imagenes/buttons/boton_salir_presionado.png", 300, 390, button_width, button_height)
    button_credits = Buttons("Imagenes/buttons/button_credits.png", "Imagenes/buttons/button_credits_pressed.png", 300, 330, button_width, button_height)
    button_play = Buttons("Imagenes/buttons/button_play.png", "Imagenes/buttons/button_play_pressed.png", 330, 500, button_width, button_height)

    ship_1 = Buttons("Imagenes/tipo_naves/Nave1.png", "Imagenes/tipo_naves/Nave1.png", 120, 60, sign_witdh, sign_height)
    ship_2 = Buttons("Imagenes/tipo_naves/Nave2.png", "Imagenes/tipo_naves/Nave2.png", 360, 60, sign_witdh, sign_height)
    ship_3 = Buttons("Imagenes/tipo_naves/Nave3_pressed.png", "Imagenes/tipo_naves/Nave3_pressed.png", 600, 60, sign_witdh, sign_height)

    # Botones circulares
    button_back = CircularButton("Imagenes/buttons/button_back.png", "Imagenes/buttons/button_back.png", 40, 40, 40)
    button_mute = CircularButton("Imagenes/buttons/boton_q_silencio.png", "Imagenes/buttons/boton_q_silencio.png", 400, 240, 40)
    button_unmute = CircularButton("Imagenes/buttons/boton_silencio.png", "Imagenes/buttons/boton_silencio.png", 400, 240, 40)

    return (button_start, button_opcion, button_salir, button_credits, button_play, 
            ship_1, ship_2, ship_3, button_back, button_mute, button_unmute)

# Función para manejar la selección de naves
def seleccionar_nave(screen, button_back, ship_1, ship_2, ship_3, button_play, clic_boton):
    select_ship_1 = select_ship_2 = select_ship_3 = False
    background, background_2, background_3 = cargar_fondos()
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
                    return False, False, False

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
                    return select_ship_1, select_ship_2, select_ship_3
        # Dibujar el fondo y los botones
        screen.blit(background_3, (0, 0))
        button_back.draw(screen, posicion_mouse)
        ship_1.draw(screen, posicion_mouse)
        ship_2.draw(screen, posicion_mouse)
        ship_3.draw(screen, posicion_mouse)

        if select_ship_1 or select_ship_2 or select_ship_3:
            button_play.draw(screen, posicion_mouse)

        pygame.display.flip()


# Función para manejar las opciones

# Función principal del menú
def Menu():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("ShipShooter")

    background, background_2, background_3 = cargar_fondos()
    clic_boton = configurar_musica()
    volume_bar = VolumeBar(250, 280, 300, 20)
    button_start, button_opcion, button_salir, button_credits, button_play, ship_1, ship_2, ship_3, button_back, button_mute, button_unmute = crear_botones()

    muted = False

    while True:
        volver_menu = False
        posicion_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_start.is_clicked(mouse_pos):
                    clic_boton.play()
                    select_ship_1, select_ship_2, select_ship_3 = seleccionar_nave(screen, button_back, ship_1, ship_2, ship_3, button_play, clic_boton)
                    
                    # Devuelve el tipo de nave seleccionado en forma de texto
                    if select_ship_1:
                        return "Scout"
                    if select_ship_2:
                        return "Tank"
                    if select_ship_3:
                        return "Fighter"

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
                                    volver_menu = True

                                if muted == False:
                                    if button_mute.is_clicked(mouse_pos):
                                        muted = True
                                        pygame.mixer.music.pause()
                                else:
                                    if button_unmute.is_clicked(mouse_pos):
                                        muted = False
                                        pygame.mixer.music.unpause()

                        screen.blit(background_2, (0, 0))
                        button_credits.draw(screen, posicion_mouse)
                        button_back.draw(screen, posicion_mouse)
                        volume_bar.draw(screen)
                        if volver_menu:
                            break
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
        button_start.draw(screen, posicion_mouse)
        button_opcion.draw(screen, posicion_mouse)
        button_salir.draw(screen, posicion_mouse)

        # Actualizar la pantalla
        pygame.display.flip()
        Clock.tick(Settings.Fps)



