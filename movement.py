#Movement kode
import pygame

class Player:
    def __init__(self, x, y, size=40, speed=5):
        self.size = size
        self.speed = speed
        self.position = pygame.Vector2(x, y)

    def handle_input(self): # Laver movement ud fra key-input til længder på en vektor
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1
       

        # Normaliser diagonal bevægelse
        if movement.length() > 0:
            movement = movement.normalize()

        self.position += movement * self.speed # gør vektorene større eller mindre baseret på speed

    def constrain_to_screen(self, width, height): # begrænser positionen baseret på størrelsen af vinduet
        self.position.x = max(0, min(width - self.size, self.position.x)) 
        self.position.y = max(0, min(height - self.size, self.position.y))

    def draw(self, surface): #tegner objektet
        pygame.draw.rect(surface, (50, 100, 255),
                         (self.position.x, self.position.y,
                          self.size, self.size))
