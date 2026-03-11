import pygame
pygame.init()
pygame.font.init()



class Barrier:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.max_health = 80
        self.health = self.max_health
        self.alive = True

        #lav font til tekst
        self.font = pygame.font.SysFont(None, 24)

        # hitbox
        self.hitbox = pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def draw(self, screen, font):
        
        pygame.draw.rect(screen, (139, 69, 19), self.hitbox)

        #health bar
        health_ratio = self.health / self.max_health
        bar_width = self.size
        bar_height = 6
        bar_x = self.hitbox.left
        bar_y = self.hitbox.top - 12

        #rød dle
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        #grøn del
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        #health tekst
        text_surface = font.render(str(self.health), True, (0, 0, 0))
        text_x = self.hitbox.centerx - text_surface.get_width() // 2
        text_y = bar_y - 16
        screen.blit(text_surface, (text_x, text_y))