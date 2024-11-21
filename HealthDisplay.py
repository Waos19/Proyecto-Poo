import pygame

class HealthDisplay:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.max_healths = {
            "Tank": 200,    # Tanque tiene más vida
            "Fighter": 100,  # Luchador tiene vida estándar
            "Scout": 75     # Explorador tiene menos vida pero más velocidad
        }

    def draw_health(self, screen, health, x, y, ship_type="Fighter"):
        max_health = self.max_healths.get(ship_type, 100)
        health_bar_length = 100
        health_ratio = max_health / health_bar_length
        
        # Calcular el porcentaje de vida actual
        health_percentage = (health / max_health) * 100
        remaining_health = (health / health_ratio)
        
        # Dibujar barra de fondo (roja)
        health_bar_rect = pygame.Rect(x - health_bar_length//2, y - 50, health_bar_length, 10)
        pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
        
        # Determinar el color basado en el porcentaje de vida
        if health_percentage > 70:
            color = (0, 255, 0)  # Verde
        elif health_percentage > 30:
            color = (255, 255, 0)  # Amarillo
        else:
            color = (255, 165, 0)  # Naranja
        
        # Dibujar barra de salud actual
        if remaining_health > 0:
            health_rect = pygame.Rect(x - health_bar_length//2, y - 50, remaining_health, 10)
            pygame.draw.rect(screen, color, health_rect)
        
        # Dibujar texto de salud
        health_text = self.font.render(f"{int(health)}/{max_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x, y - 70))
        screen.blit(health_text, text_rect)