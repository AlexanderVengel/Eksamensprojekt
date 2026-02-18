import pygame

class Arrow():
    def __init__(self, x, y, speed, size, damage, target_pos):
        self.size = size
        self.speed = speed
        self.damage = damage
        self.position = pygame.Vector2(x, y)

        
        direction = pygame.Vector2(target_pos) - self.position
        if direction.length() != 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        self.alive = True

    def update(self, screen_width, screen_height):
        self.position += self.direction * self.speed

        
        if (self.position.x < 0 or self.position.x > screen_width or # fjerner objektet når pilen er ude for skærmen
            self.position.y < 0 or self.position.y > screen_height):
            self.alive = False

    def draw(self, screen): # tegner objektet på skærmen
        pygame.draw.circle(screen, (139, 69, 19), # sætter pilen til at ligne en cirkel
                           (int(self.position.x), int(self.position.y)), 
                           self.size)

    
