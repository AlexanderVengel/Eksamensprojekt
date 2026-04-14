import pygame
pygame.init()
pygame.font.init()
import sys
import pygame as pg
from movement import Player
from projectiles import Arrow
from barrier import Barrier
from enemy import enemy

pygame.init()

WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooter")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)

arrows = []
enemy_arrows = []
barriers = []
enemies = []

frame_counter = 0

# barrier
barrier = Barrier(x=100, y=100)
barriers.append(barrier)

# enemies
enemy1 = enemy(900, 200)
enemy2 = enemy(850, 500)
enemies.append(enemy1)
enemies.append(enemy2)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouse_pos = pygame.mouse.get_pos()

                arrow = Arrow(
                    player.position.x + player.size / 2,
                    player.position.y + player.size / 2,
                    speed=12,
                    size=5,
                    target_pos=mouse_pos
                )

                arrows.append(arrow)

    player.handle_input()
    player.constrain_to_screen(WIDTH, HEIGHT)

    # opdater spillerens pile
    for arrow in arrows[:]:
        arrow.update(WIDTH, HEIGHT)

        # pil rammer barriers
        for barrier in barriers:
            if arrow.hitbox.colliderect(barrier.hitbox):
                barrier.take_damage(arrow.damage)
                arrow.alive = False

        # pil rammer enemies
        for enemy in enemies:
            if arrow.hitbox.colliderect(enemy.hitbox):
                enemy.take_damage(arrow.damage)
                arrow.alive = False

        if not arrow.alive and arrow in arrows:
            arrows.remove(arrow)

    # fjern døde barriers
    for barrier in barriers[:]:
        if not barrier.alive:
            barriers.remove(barrier)

    # opdater enemies
    for enemy in enemies[:]:
        enemy.update(player, barriers, enemy_arrows, WIDTH, HEIGHT)

        if not enemy.alive:
            enemies.remove(enemy)

    # opdater enemy arrows
    for enemy_arrow in enemy_arrows[:]:
        enemy_arrow.update(WIDTH, HEIGHT)

        # enemy arrow rammer barrier
        for barrier in barriers:
            if enemy_arrow.hitbox.colliderect(barrier.hitbox):
                barrier.take_damage(enemy_arrow.damage)
                enemy_arrow.alive = False

        # enemy arrow rammer player
        player_rect = pygame.Rect(
            player.position.x,
            player.position.y,
            player.size,
            player.size
        )

        if enemy_arrow.hitbox.colliderect(player_rect):
            print("Player hit")
            enemy_arrow.alive = False

        if not enemy_arrow.alive and enemy_arrow in enemy_arrows:
            enemy_arrows.remove(enemy_arrow)

    screen.fill((255, 255, 255))

    for arrow in arrows:
        arrow.draw(screen)

    for enemy_arrow in enemy_arrows:
        enemy_arrow.draw(screen)

    for barrier in barriers:
        barrier.draw(screen, barrier.font)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    pygame.display.flip()
    frame_counter += 1

pygame.quit()
sys.exit()