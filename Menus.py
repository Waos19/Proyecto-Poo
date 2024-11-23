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

# Initialize Pygame
pygame.mixer.init()

# Load backgrounds
def load_backgrounds():
    background_load = pygame.image.load("image_menu/background/background.png")
    background = pygame.transform.scale(background_load, (800, 600))

    background_load_2 = pygame.image.load("image_menu/background/background_config.jpg")
    background_2 = pygame.transform.scale(background_load_2, (800, 600))

    background_load_3 = pygame.image.load("image_menu/background/background_3.jpg")
    background_3 = pygame.transform.scale(background_load_3, (800, 600))

    return background, background_2, background_3

# Set up the music
def setup_music():
    load_clic_button = "sound/ocassional_sound/clic_boton.wav"
    clic_boton = pygame.mixer.Sound(load_clic_button)
    pygame.mixer.music.load("sound/music_background/supernova.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    return clic_boton

# Create buttons
def create_buttons():
    button_width = 220
    button_height = 50
    sign_witdh = 150
    sign_height = 400

    button_start = Buttons("image_menu/buttons/boton_start.png", "image_menu/buttons/boton_start_presionado.png", 300, 270, button_width, button_height)
    button_option = Buttons("image_menu/buttons/boton_opcion.png", "image_menu/buttons/boton_opcion_presionado.png", 300, 330, button_width, button_height)
    button_exit = Buttons("image_menu/buttons/boton_salir.png", "image_menu/buttons/boton_salir_presionado.png", 300, 390, button_width, button_height)
    button_credits = Buttons("image_menu/buttons/button_credits.png", "image_menu/buttons/button_credits_pressed.png", 300, 330, button_width, button_height)
    button_play = Buttons("image_menu/buttons/button_play.png", "image_menu/buttons/button_play_pressed.png", 330, 500, button_width, button_height)

    ship_1 = Buttons("image_menu/ships/Nave1.png", "image_menu/ships/Nave1.png", 120, 60, sign_witdh, sign_height)
    ship_2 = Buttons("image_menu/ships/Nave2.png", "image_menu/ships/Nave2.png", 360, 60, sign_witdh, sign_height)
    ship_3 = Buttons("image_menu/ships/Nave3.png", "image_menu/ships/Nave3.png", 600, 60, sign_witdh, sign_height)

    # Circular buttons
    button_back = CircularButton("image_menu/buttons/button_back.png", "image_menu/buttons/button_back.png", 40, 40, 40)
    button_mute = CircularButton("image_menu/buttons/boton_q_silencio.png", "image_menu/buttons/boton_q_silencio.png", 400, 240, 40)
    button_unmute = CircularButton("image_menu/buttons/boton_silencio.png", "image_menu/buttons/boton_silencio.png", 400, 240, 40)

    return (button_start, button_option, button_exit, button_play, 
            ship_1, ship_2, ship_3, button_back, button_mute, button_unmute)

# Function to handle ship selection
def select_ship(screen, button_back, ship_1, ship_2, ship_3, button_play, clic_boton):
    select_ship_1 = select_ship_2 = select_ship_3 = False
    background, background_2, background_3 = load_backgrounds()
    while True:
        mouse_position = pygame.mouse.get_pos()
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
        # Draw background and buttons
        screen.blit(background_3, (0, 0))
        button_back.draw(screen, mouse_position)
        ship_1.draw(screen, mouse_position)
        ship_2.draw(screen, mouse_position)
        ship_3.draw(screen, mouse_position)

        if select_ship_1 or select_ship_2 or select_ship_3:
            button_play.draw(screen, mouse_position)

        pygame.display.flip()


# Function to handle options

# Main menu function
def Menu():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("ShipShooter")

    background, background_2, background_3 = load_backgrounds()
    clic_boton = setup_music()
    volume_bar = VolumeBar(250, 280, 300, 20)
    button_start, button_option, button_exit, button_play, ship_1, ship_2, ship_3, button_back, button_mute, button_unmute = create_buttons()

    muted = False

    while True:
        back_to_menu = False
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_start.is_clicked(mouse_pos):
                    clic_boton.play()
                    select_ship_1, select_ship_2, select_ship_3 = select_ship(screen, button_back, ship_1, ship_2, ship_3, button_play, clic_boton)
                    
                    # Return the selected ship type as text
                    if select_ship_1:
                        return "Scout"
                    if select_ship_2:
                        return "Tank"
                    if select_ship_3:
                        return "Fighter"

                if button_option.is_clicked(mouse_pos):
                    clic_boton.play()
                    while True:
                        mouse_position = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if volume_bar.is_clicked(mouse_pos):
                                    volume_bar.handle_click(mouse_pos)

                                if button_back.is_clicked(mouse_pos):
                                    clic_boton.play()
                                    back_to_menu = True

                                if muted == False:
                                    if button_mute.is_clicked(mouse_pos):
                                        muted = True
                                        pygame.mixer.music.pause()
                                else:
                                    if button_unmute.is_clicked(mouse_pos):
                                        muted = False
                                        pygame.mixer.music.unpause()

                        screen.blit(background_2, (0, 0))
                        button_back.draw(screen, mouse_position)
                        volume_bar.draw(screen)
                        if back_to_menu:
                            break
                        if muted:
                            button_unmute.draw(screen, mouse_position)
                        else:
                            button_mute.draw(screen, mouse_position)

                        pygame.display.flip()
                if button_exit.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Draw background and buttons
        screen.blit(background, (0, 0))
        button_start.draw(screen, mouse_position)
        button_option.draw(screen, mouse_position)
        button_exit.draw(screen, mouse_position)

        # Update the screen
        pygame.display.flip()
        Clock.tick(Settings.Fps)

