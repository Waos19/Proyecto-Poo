import pygame
import sys
import Settings
from World import World
from Camera import Camera
from Tank import Tank  
from Scout import Scout  
from Fighter import Fighter
from WeaponsPickupManager import WeaponPickupsManager

# Initialize pygame
pygame.init()

# Set up the main window
Screen = pygame.display.set_mode((Settings.Width, Settings.Height))
pygame.display.set_caption("Selección de nave")

# Global variables
Clock = pygame.time.Clock()
Font = pygame.font.Font(None, 36)  # Font for text

# Function for the ship selection menu
def ShipSelectionMenu():
    while True:
        Screen.fill((0, 0, 0))  # Black background

        # Menu text
        title_text = Font.render("Selecciona tu nave:", True, (255, 255, 255))
        tank_text = Font.render("1 - Tank (Alta vida, baja velocidad)", True, (255, 0, 0))
        scout_text = Font.render("2 - Scout (Baja vida, alta velocidad)", True, (0, 255, 0))
        fighter_text = Font.render("3 - Fighter (Equilibrado)", True, (0, 0, 255))

        # Draw the text on the screen
        Screen.blit(title_text, (Settings.Width // 2 - title_text.get_width() // 2, 100))
        Screen.blit(tank_text, (Settings.Width // 2 - tank_text.get_width() // 2, 200))
        Screen.blit(scout_text, (Settings.Width // 2 - scout_text.get_width() // 2, 300))
        Screen.blit(fighter_text, (Settings.Width // 2 - fighter_text.get_width() // 2, 400))

        pygame.display.flip()

        # Events for selecting the ship
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return Tank(Settings.Width // 2, Settings.Height // 2)
                elif event.key == pygame.K_2:
                    return Scout(Settings.Width // 2, Settings.Height // 2)
                elif event.key == pygame.K_3:
                    return Fighter(Settings.Width // 2, Settings.Height // 2)

weapon_types = ["LaserGun", "MachineGun", "RocketLauncher"]
weapon_pickups_manager = WeaponPickupsManager(weapon_types, spawn_interval=5000, max_pickups=5)


# Main game function
def Main():
    # Create the world and camera
    world = World(1920, 1200)
    camera = Camera(world.width, world.height)
    
    # Run the ship selection menu
    Player = ShipSelectionMenu()
    
    # Main game loop
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
        Player.Movement(dx, dy)

        # Rotate the character towards the mouse
        Player.lookAtMouse(camera)
        
        # Update methods
        Player.update()
        camera.update(Player)
        weapon_pickups_manager.update(delta_time)
        weapon_pickups_manager.handle_collision(Player)
        
        # Draw methods
        Screen.blit(world.background, camera.apply(world))
        Player.draw(Screen, camera)
        Player.draw_health(Screen)
        Player.weapon.draw_bullets(Screen, camera)
        Player.weapon.DrawAmmo(Screen)
        weapon_pickups_manager.draw(Screen, camera)
        

        # Update the screen
        pygame.display.flip()
        Clock.tick(Settings.Fps)

if __name__ == "__main__":
    Main()
