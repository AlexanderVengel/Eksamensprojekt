import pygame
import sys
from movement import Player

pygame.init()

WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooter")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.handle_input()
    player.constrain_to_screen(WIDTH, HEIGHT)

    # Draw
    screen.fill((255, 255, 255))
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
